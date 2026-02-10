import requests
import json

def get_60s_news():
    """获取60秒读懂世界新闻"""
    url = "https://60s.viki.moe/v2/60s"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("code") == 200:
            news_list = data["data"]["news"]
            date = data["data"]["date"]
            # 格式化新闻内容
            content = f"📅 {date} 今日新闻简报：\n\n"
            content += "\n".join(news_list)
            return content
    except Exception as e:
        print(f"获取新闻失败: {e}")
    return None

def send_to_qq(content):
    """通过 QMsg 推送到 QQ"""
    # 这里我们稍后通过 GitHub Secret 注入 KEY，不要直接写死
    import os
    qmsg_key = os.getenv("QMSG_KEY")
    
    if not qmsg_key:
        print("未配置 QMSG_KEY")
        return

    url = f"https://qmsg.zendee.cn/send/{qmsg_key}"
    data = {"msg": content}
    
    try:
        res = requests.post(url, data=data)
        print(f"推送结果: {res.text}")
    except Exception as e:
        print(f"推送失败: {e}")

if __name__ == "__main__":
    news = get_60s_news()
    if news:
        send_to_qq(news)