"""Agent 工具定义 — 天气查询 / 数学计算 / 时间查询"""

from datetime import datetime, timezone, timedelta


def get_weather(city: str) -> dict:
    """获取指定城市的天气信息

    Args:
        city: 城市名称，如 "北京"、"Beijing"
    """
    weather_data = {
        "北京": {"temperature": "25°C", "condition": "晴", "humidity": "60%", "wind": "北风3级"},
        "Beijing": {"temperature": "25°C", "condition": "Sunny", "humidity": "60%", "wind": "North 3"},
        "上海": {"temperature": "28°C", "condition": "多云", "humidity": "70%", "wind": "东南风2级"},
        "Shanghai": {"temperature": "28°C", "condition": "Cloudy", "humidity": "70%", "wind": "SE 2"},
        "广州": {"temperature": "32°C", "condition": "雷阵雨", "humidity": "85%", "wind": "南风4级"},
        "Guangzhou": {"temperature": "32°C", "condition": "Thunderstorm", "humidity": "85%", "wind": "South 4"},
        "深圳": {"temperature": "31°C", "condition": "阵雨", "humidity": "80%", "wind": "西南风3级"},
        "Shenzhen": {"temperature": "31°C", "condition": "Showers", "humidity": "80%", "wind": "SW 3"},
    }
    return weather_data.get(city, {"temperature": "未知", "condition": "暂无数据", "humidity": "未知", "wind": "未知"})


def calculate(expression: str) -> dict:
    """执行数学计算

    Args:
        expression: 数学表达式，如 "2 + 3 * 4"、"2 ** 10"
    """
    # 只允许安全的数学运算字符
    allowed_chars = set("0123456789+-*/.() ")
    if not all(c in allowed_chars for c in expression):
        return {"error": "不支持的字符，仅允许数字和基本运算符（+ - * / ** .）"}

    try:
        result = eval(expression, {"__builtins__": {}}, {})  # noqa: S307
        return {"expression": expression, "result": str(result)}
    except Exception as e:
        return {"expression": expression, "error": str(e)}


def get_current_time() -> dict:
    """获取当前日期和时间（北京时间 UTC+8）"""
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)
    return {
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "weekday": now.strftime("%A"),
        "timezone": "Asia/Shanghai (UTC+8)",
    }
