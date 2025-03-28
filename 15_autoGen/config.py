'''在这里设置OPENAI_API_KEY'''
from dotenv import load_dotenv
import os
load_dotenv()
openai_api_key=os.getenv("OPENAI_API_KEY")

'''在这里配置大模型'''
llm_config={
"config_list":[{
    "model":"gpt-4o",
    "api_key":openai_api_key
}]
}

'''
在这里模拟鲜花销售表和鲜花库存表
'''
inventory_table = """
| 鲜花种类       | 当前库存数量 |
|----------------|--------------|
| 玫瑰           | 120          |
| 百合           | 80           |
| 康乃馨         | 150          |
| 郁金香         | 60           |
| 向日葵         | 90           |
| 满天星         | 200          |
"""

sales_table = """
| 鲜花种类       | 销售数量     |
|----------------|--------------|
| 玫瑰           | 150          |
| 百合           | 100          |
| 康乃馨         | 120          |
| 郁金香         | 70           |
| 向日葵         | 80           |
| 满天星         | 180          |
"""

'''在这里定义任务'''
#关于库存方面的任务
inventory_tasks=[
    f"""查看当前库存中各种鲜花的数量，并报告哪些鲜花库存不足\n
    鲜花库存表:{inventory_table}""",
    f"""根据过去一个月的销售数量，预测接下来一个月哪些鲜花的需求量会增加\n
    鲜花销售表:{sales_table}"""
]
#关于市场方面的任务
market_research_tasks=[
    """分析市场趋势，找出当前最受欢迎的饿鲜花种类及其可能的原因"""
]
#内容生成方面的任务
content_creation_tasks=[
    """利用提供的信息，撰写一篇吸引人的博客文章，介绍最受欢迎的鲜花及选购技巧"""
]

import autogen

'''在这里定义Assistant Agent的角色'''
inventory_assistant=autogen.AssistantAgent(
    name="inventory_assistant",
    llm_config=llm_config
)
market_research_assistant=autogen.AssistantAgent(
    name="market_research_assistant",
    llm_config=llm_config
)
content_creator=autogen.AssistantAgent(
    name="content_creator",
    llm_config=llm_config,
    system_message="""
    你是一名专业的撰稿人，以洞察力强和文章引人入胜著称。
    你能将复杂的概念转化为引人入胜的叙述。
    当一切完成后，请回复"结束"。
"""
)

'''在这里创建User Agent'''
user_proxy_auto=autogen.UserProxyAgent(
    name="user_proxy_auto",
    human_input_mode="NEVER",
    #这里定义一个匿名函数，用于判断传入的参数content字段在去掉末尾空白之后是否以“结束”两字结尾
    is_termination_msg=lambda x:x.get("content", "").rstrip().endswith("结束"),
    code_execution_config={
        "last_n_messages":1,
        "work_dir":"tasks",
        "use_docker":False
    }
)

user_proxy=autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    #这里定义一个匿名函数，用于判断传入的参数content字段在去掉末尾空白之后是否以“结束”两字结尾
    is_termination_msg=lambda x:x.get("content", "").rstrip().endswith("结束"),
    code_execution_config={
        "last_n_messages":1,
        "work_dir":"tasks",
        "use_docker":False
    }
)
