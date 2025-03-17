from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAI
llm = OpenAI(temperature=0.1)

from langchain.agents import load_tools
tools = load_tools(["serpapi", "llm-math"], llm)

from langchain.prompts import PromptTemplate

template = (
    'Try your best to answer the following question in Chinese, you can use following tools:\n\n'
    '{tools}\n\n'
    'Use the following format:\n\n'
    'Thought: you should always think about what to do\n\n'
    'Action: the action you take, should be one of [{tool_names}]\n\n'
    'Action Input: the input to the action\n\n'
    'Observation: the result of the action\n\n'
    '...(this Thought/Action/Action Input/Observation can repeat N times)\n\n'
    'Final Answer: the final answer to the original input question\n\n'
    'Begin!\n\n'
    'Question: {input}\n\n'
    'Thought: {agent_scratchpad}\n\n'
)
prompt = PromptTemplate.from_template(template)

from langchain.agents import create_react_agent
agent = create_react_agent(llm=llm, tools=tools,prompt=prompt)
# from langchain.agents import initialize_agent
# from langchain.agents import AgentType

# 初始化agent
# agent = initialize_agent(
#     tools,
#     llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True,
#     handle_parsing_errors=True,
# )

from langchain.agents import AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,handle_parsing_errors=True)

agent_executor.invoke(
    {
        "input": """目前市场上玫瑰花一般进货价格是多少？\n
        如果我在此基础上加价5%，应该如何定价？
        """
    }
)
# input="""目前市场上玫瑰花一般进货价格是多少？\n
#          如果我在此基础上加价5%，应该如何定价？"""
# output=agent(input)
# print(output)