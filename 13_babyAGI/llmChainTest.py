from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

# 初始化语言模型
llm = OpenAI(temperature=0.7)

# 定义提示模板
prompt = PromptTemplate(
    input_variables=["question"],
    template="回答这个问题：{question}"
)

# 创建 RunnableSequence（替代 LLMChain）
chain = prompt | llm  # 使用管道操作符 | 连接 prompt 和 llm

# 使用 invoke 方法运行
response = chain.invoke({"question": "今天的天气怎么样？"})
print(response)