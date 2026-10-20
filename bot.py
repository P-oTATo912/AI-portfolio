import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. 加载 .env 文件中的环境变量
load_dotenv()

# 2. 初始化 DeepSeek 客户端
# api_key 会自动去 .env 里找 DEEPSEEK_API_KEY 的值
client = OpenAI(
    api_key=os.getenv("MY_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 3. 初始化历史记录列表（这就是多轮对话的“记忆”）
messages = [
    {"role": "system", "content": "你是一个乐于助人的备课助手，请用简练的语言回答。"}
]

def chat_with_bot(user_input):
    # 将用户的输入追加到历史记录中
    messages.append({"role": "user", "content": user_input})
    
    try:
        # 发送带有历史记录的 messages 列表
        response = client.chat.completions.create(
            model="deepseek-chat", # DeepSeek 的模型名称
            messages=messages,
            temperature=0.7,       # 控制创造性
            max_tokens=500         # 限制最大回复长度
        )
        
        # 获取 AI 的回答
        ai_reply = response.choices[0].message.content
        
        # 【核心】将 AI 的回答也追加到历史记录中，这样下一轮它就知道自己刚说了什么
        messages.append({"role": "assistant", "content": ai_reply})
        
        return ai_reply
        
    except Exception as e:
        return f"发生错误: {e}"

# --- 测试多轮追问 ---
print("🤖 机器人已启动，输入 '退出' 结束对话。")
while True:
    user_text = input("\n🙋 你: ")
    if user_text == "退出":
        print("👋 再见！")
        break
    
    reply = chat_with_bot(user_text)
    print(f"🤖 AI: {reply}")