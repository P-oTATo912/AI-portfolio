import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv()

# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=os.getenv("MY_API_KEY"), # 确保 .env 文件里的变量名也是 MY_API_KEY
    base_url="https://api.deepseek.com"
)

# 准备 10 个学科问题
questions = [
    "把字句教学难点有哪些？", "HSK4词汇量要求", "中级作文三段式评语",
    "简述唐朝的科举制度。", "什么是相对论？", "解释一下细胞膜的结构。",
    "如何计算圆的面积？", "什么是通货膨胀？", "元素周期表是谁发明的？",
    "简述第一次世界大战的起因。"
]

total_prompt_tokens = 0
total_completion_tokens = 0

print("开始进行 10 次调用测试...\n")

for i, q in enumerate(questions, 1):
    # 每次都是独立提问，不包含历史记录，方便精确计算单次成本
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": q}]
        )
        
        # 获取 token 消耗
        prompt_t = response.usage.prompt_tokens
        completion_t = response.usage.completion_tokens
        
        total_prompt_tokens += prompt_t
        total_completion_tokens += completion_t
        
        print(f"第 {i:2d} 次调用 | 输入: {prompt_t} tokens | 输出: {completion_t} tokens | 问题: {q[:10]}...")
    except Exception as e:
        print(f"第 {i} 次调用失败: {e}")

# --- 计算费用 ---
# DeepSeek 官方目前的参考计费单价（请以官网实时价格为准，此处仅作演示）
# 输入：0.001 元 / 1K tokens
# 输出：0.002 元 / 1K tokens
input_price_per_1k = 0.001
output_price_per_1k = 0.002

input_cost = (total_prompt_tokens / 1000) * input_price_per_1k
output_cost = (total_completion_tokens / 1000) * output_price_per_1k
total_cost = input_cost + output_cost

print("\n" + "="*40)
print(f"总计输入 Token: {total_prompt_tokens}")
print(f"总计输出 Token: {total_completion_tokens}")
print(f"10次总花费（估算）: ¥ {total_cost:.6f} 元")
print(f"【判断结论】一次备课问答平均成本: ¥ {total_cost / 10:.6f} 元")
print("="*40)