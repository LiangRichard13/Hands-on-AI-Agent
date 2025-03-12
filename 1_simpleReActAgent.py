#导入dotenv包，用于加载环境变量
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

#导入LangChain Hub
from langchain import hub
#从LangChain Hub中获得ReAct的prompt
prompt=hub.pull("hwchase17/react")
print(prompt)

#导入OpenAI
from langchain_openai import OpenAI

#选择要使用的大模型
llm=OpenAI()
#导入SerpAPIWrapper即工具包
from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import Tool

#实例化SerpAPIWrapper
search=SerpAPIWrapper()

#准备工具列表

tools=[
    Tool(
        name="Search",
        func=search.run,
        description="当大模型没有相关知识时，用于搜索知识"
    )
]

#导入create_react_agent
from langchain.agents import create_react_agent
#构建React Agent
agent=create_react_agent(llm,tools,prompt)
#导入AgentExecutor
from langchain.agents import AgentExecutor
#创建Agent执行器并传入Agent和工具
agent_executor=AgentExecutor(agent=agent,tools=tools,verbose=True)
#调用AgentExecutor
agent_executor.invoke({"input":"当前Agent最新研究进展？"})