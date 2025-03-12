from dotenv import load_dotenv
load_dotenv()

#设置提示词模板
from langchain.prompts import PromptTemplate
prompt=PromptTemplate.from_template("{flower}的花语是？")
#设置大模型
from langchain_openai import OpenAI
model=OpenAI()

#设置输出解析器
#这里的导入方式和from langchain_core.output_parsers import StrOutputParser没有区别，都是指向同一类
from langchain.schema.output_parser import StrOutputParser

output_parser=StrOutputParser()
#构建链式处理
chain=prompt|model|output_parser
#执行链并打印结果
result=chain.invoke({"flower":"丁香"})
print(result)