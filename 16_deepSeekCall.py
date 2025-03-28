from openai import OpenAI
from dotenv import load_dotenv
import os 
load_dotenv()
deepseek_api_key=os.getenv("DEEPSEEK_API_KEY")


'''
这是deepseek-v3的openai api的调用方式
'''
# client = OpenAI(api_key=deepseek_api_key,base_url="https://api.deepseek.com")

# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant"},
#         {"role": "user", "content": "Hello"},
#     ],
#     stream=False
# )

# print(response.choices[0].message.content)

'''
这是使用langchain中内置的ChatOpenAI的调用方式调用deepseek-v3
'''
# from langchain_openai import ChatOpenAI

# model=ChatOpenAI(base_url="https://api.deepseek.com",model="deepseek-chat",api_key=deepseek_api_key)
# response = model.invoke("Hello, Please introduce yourself.")
# print(response.content)

'''
这是使用llama-index调用DeepSeek的方式
'''
# from llama_index.llms.deepseek import DeepSeek

# # 初始化 DeepSeek-V3 模型
# llm = DeepSeek(
#     model="deepseek-chat",  # 指定模型名称
#     api_key=deepseek_api_key  # 替换为你的 API 密钥
# )
# print(llm.complete("Hello, Please introduce yourself."))