from nonebot.plugin import PluginMetadata
from pydantic import BaseModel
from nonebot import get_bots, logger, get_plugin_config, require
from nonebot.adapters.onebot.v11 import Message

import httpx
import json
import datetime
from pathlib import Path

# -----------------------------
# 插件配置
# -----------------------------
class InternetOutageConfig(BaseModel):
    outage_debug: bool = False
    outage_proxies: str = None
    outage_group_id: list[int | str] = []
    outage_cf_token: str

__plugin_meta__ = PluginMetadata(
    name="全球互联网中断监测",
    description="基于 Cloudflare Radar 的全球断网事件自动推送",
    usage="自动运行",
    type="application",
    homepage="https://github.com/CN171-1/nonebot-plugin-internet-outage",
    supported_adapters={"~onebot.v11"},
    config=InternetOutageConfig,
)

config = get_plugin_config(InternetOutageConfig)

proxy = config.outage_proxies
group_ids = config.outage_group_id
CF_TOKEN = config.outage_cf_token

TRAFFIC_API = "https://api.cloudflare.com/client/v4/radar/traffic_anomalies"
OUTAGE_API = "https://api.cloudflare.com/client/v4/radar/annotations/outages"

OUTAGE_CAUSE_MAP = {
    "GOVERNMENT_DIRECTED": "政府命令",
    "MILITARY_ACTION": "军事行动影响",
    "CABLE_CUT": "光缆断裂",
    "POWER_OUTAGE": "大规模停电",
    "TECHNICAL_PROBLEM": "重大技术故障",
    "NETWORK_CONGESTION": "网络严重拥塞",
    "UNKNOWN": "原因暂不明确",
    "WEATHER": "自然灾害",
    "MISCONFIGURATION": "配置错误",
    "DNS": "DNS 故障",
}

OUTAGE_TYPE_MAP = {
    "NATIONWIDE": "全国级中断",
    "REGIONAL": "区域级中断",
    "NETWORK": "运营商 / 网络级中断",
    "PLATFORM": "平台级中断",
}

require("nonebot_plugin_localstore")
require("nonebot_plugin_apscheduler")

import nonebot_plugin_localstore as store
from nonebot_plugin_apscheduler import scheduler

class StorageManager:
    def __init__(self):
        self.data_dir = Path(store.get_plugin_data_dir())
        self.data_dir.mkdir(parents=True, exist_ok=True)

    async def get_seen_dict(self, key: str) -> dict:
        file = self.data_dir / f"{key}.json"
        if file.exists():
            try:
                with open(file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    async def save_seen_dict(self, key: str, data: dict):
        file = self.data_dir / f"{key}.json"
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    async def is_first_run(self, key: str) -> bool:
        return not (self.data_dir / f"{key}.json").exists()

storage = StorageManager()

async def get_json(url: str, params: dict = None, timeout: int = 30) -> dict:
    """获取JSON数据"""
    headers = {"Authorization": f"Bearer {CF_TOKEN}"}
    try:
        async with httpx.AsyncClient(timeout=timeout, headers=headers, proxy=proxy) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"请求失败 {url}: {e}")
        return {}

async def fetch_traffic_anomalies():
    params = {"type": "LOCATION", "status": "VERIFIED", "dateRange": "7d"}
    data = await get_json(TRAFFIC_API, params)
    return data.get("result", {}).get("trafficAnomalies", [])

async def fetch_outages():
    params = {"dateRange": "7d"}
    data = await get_json(OUTAGE_API, params)
    return data.get("result", {}).get("annotations", [])

def match_outage(anomaly, outages):
    country = anomaly["locationDetails"]["code"]
    a_start = datetime.datetime.fromisoformat(anomaly["startDate"].replace("Z", "+00:00"))
    for o in outages:
        if country not in o["locations"]:
            continue
        o_start = datetime.datetime.fromisoformat(o["startDate"].replace("Z", "+00:00"))
        if abs((a_start - o_start).total_seconds()) <= 900:
            return o
    return None

def build_message(outage):
    loc = outage["locationsDetails"][0]["name"]
    cause = outage["outage"]["outageCause"]
    cause_cn = OUTAGE_CAUSE_MAP.get(cause, cause)
    otype = outage["outage"]["outageType"]
    otype_cn = OUTAGE_TYPE_MAP.get(otype, otype)
    return Message(
        f"🌐 互联网中断事件\n\n"
        f"📍 国家：{loc}\n"
        f"🕒 开始时间：{outage['startDate']} UTC\n"
        f"📡 影响范围：{otype_cn}\n"
        f"⚠️ 原因：{cause_cn}\n\n"
        f"📝 说明：\n{outage['description']}\n\n"
        f"🔗 来源：\n{outage['linkedUrl']}"
    )

def build_message_from_anomaly(anomaly):
    loc = anomaly["locationDetails"]["name"]
    start = anomaly["startDate"]
    return Message(
        f"⚠️ 互联网流量异常\n\n"
        f"📍 国家：{loc}\n"
        f"🕒 开始时间：{start} UTC\n"
        f"💡 备注：该事件为流量异常，尚未确认中断。"
    )

async def broadcast(message: Message):
    bots = get_bots()
    if not bots:
        return
    bot = list(bots.values())[0]
    if not group_ids:
        logger.warning("未配置推送群，跳过")
        return
    for gid in group_ids:
        try:
            await bot.send_group_msg(group_id=int(gid), message=message)
        except Exception as e:
            logger.error(f"推送至群 {gid} 失败: {e}")


@scheduler.scheduled_job(
    "interval",
    minutes=10,
    id="internet_outage_monitor",
    misfire_grace_time=20
)
async def outage_schedule():
    key = "outage_events"
    anomalies = await fetch_traffic_anomalies()
    outages = await fetch_outages()
    seen = await storage.get_seen_dict(key)
    first_run = await storage.is_first_run(key)

    # 先处理 anomalies -> outage 匹配
    for a in anomalies:
        uuid = a["uuid"]
        outage = match_outage(a, outages)

        if uuid not in seen:
            # 新事件
            if outage:
                msg = build_message(outage)
                sent_type = "anomaly + outage"
                if not first_run:
                    await broadcast(msg)
                logger.info(
                    f"发现断网事件（anomaly + outage）：[{a['locationDetails']['code']}] "
                    f"{outage['outage']['outageCause']}"
                )
            else:
                msg = build_message_from_anomaly(a)
                sent_type = "anomaly"
                if not first_run:
                    await broadcast(msg)
                logger.info(
                    f"发现断网事件（仅 anomaly）：[{a['locationDetails']['code']}] UNKNOWN"
                )
            seen[uuid] = {"sent_type": sent_type}

        else:
            # 已存在
            prev_type = seen[uuid]["sent_type"]
            if prev_type == "anomaly" and outage:
                # 升级为 outage
                msg = build_message(outage)
                await broadcast(msg)
                logger.info(
                    f"更新断网事件（anomaly -> outage）：[{a['locationDetails']['code']}] "
                    f"{outage['outage']['outageCause']}"
                )
                seen[uuid]["sent_type"] = "anomaly -> outage"

    # 再处理仅 outages，没有对应 anomaly 的情况
    for o in outages:
        # 找出 location 对应的 anomaly
        found = False
        for a in anomalies:
            if match_outage(a, [o]):
                found = True
                break
        if not found:
            # 仅 outage
            loc_codes = o["locations"]
            uuid = f"outage_{loc_codes[0]}_{o['startDate']}"  # 生成唯一标识
            if uuid not in seen:
                msg = build_message(o)
                if not first_run:
                    await broadcast(msg)
                logger.info(
                    f"发现断网事件（仅 outage）：{loc_codes} {o['outage']['outageCause']}"
                )
                seen[uuid] = {"sent_type": "outage"}

    await storage.save_seen_dict(key, seen)
