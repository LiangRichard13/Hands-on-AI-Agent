#加载环境
from dotenv import load_dotenv
load_dotenv()

#配置大模型
from llama_index.llms.openai import OpenAI

llm=OpenAI(model="gpt-3.5-turbo")

#创建ReAct Rag Agent
from llama_index.core.agent import ReActAgent
from load_index import query_engine_tool
tools=[query_engine_tool]
agent=ReActAgent.from_tools(tools=tools,llm=llm,verbose=True)
agent.chat("请告诉我关于武汉港黑票活动猖獗问题的背景")