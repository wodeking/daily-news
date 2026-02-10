import requests
import json
import os

def sensitive_word_filter(text):
    """
    敏感词处理逻辑：将敏感词中间插入空格
    """
    keywords = ["人民", "人民币", "伊朗", "公开信", "出台", "购房"]
    
    filtered_text = text
    for word in keywords:
        if word in filtered_text:
            # 将 '人民' 变为 '人 民'
            spaced_word = " ".join(list(word))
            filtered_text = filtered_text.replace(word, spaced_word)
            
    return filtered_text

def get_60s_news():
    """获取60秒读懂世界新闻并格式化"""
    url = "https://60s.viki.moe/v2/60s"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("code") == 200:
            news_list = data["data"]["news"]
            date = data["data"]["date"]
            
            # 1. 过滤敏感词
            # 2. 加上数字序号并分行
            formatted_news = []
            for index, item in enumerate(news_list, start=1):
                clean_item = sensitive_word_filter(item)
                formatted_news.append(f"{index}. {clean_item}")
            
            # 拼接最终内容
            content = f"📅 {date} 今日新闻简报：\n\n"
            content += "\n".join(formatted_news)
            
            # 最后加上 API 默认的尾注（如果有）
            if "tip" in data["data"]:
                content += f"\n\n💡 {data['data']['tip']}"
                
            return content
    except Exception as e:
        print(f"获取新闻失败: {e}")
    return None

def send_to_qmsg(content):
    """通过 QMsg 推送到 QQ"""
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
        send_to_qmsg(news)