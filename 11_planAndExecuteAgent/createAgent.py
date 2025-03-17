'''
LangChain中的Plan and Execute Agent框架中包含计划者planner和执行者executor

1.计划者planner是一个大模型，利用语言模型的推理能力来规划要做的事情，以及可能遇到的边缘情况，一旦planner生成整个计划
这个计划将通过一个输出解析器进行处理。这个解析器的作用是将模型的原始输出转化为一个清晰的步骤列表，其中每个字符串代表
计划中的一个步骤
2.执行者executor也是一个大模型，在LangChain的实现中，执行者本身就是一个ReAct Agent，这允许执行者接受一个目标并使用工具
通过单个步骤或者多个步骤来实现该目标

这种方法的好处是允许一个大模型专注规划，另一个专注执行
'''

#加载环境 
from dotenv import load_dotenv
load_dotenv()

#导入LangChain工具
from langchain.tools import tool
'''
函数可以通过@tool装饰器标记成为LangChain中的工具 
'''
#库存查询
@tool
def check_inventory(flower_type:str)->int:
    '''
    check_inventory
    用于查询指定鲜花种类的库存数量
    参数：flower_type鲜花类型
    返回：库存数量
    '''
    return 100 #假设每种花都有100个单位

#价格查询
@tool
def check_price(flower_type:str)->int:
    '''
    check_price
    用于查询指定鲜花种类的基础价格
    参数：flower_type鲜花类型
    返回：返回基础价格
    '''
    return 10 #假设每种花都有100个单位

#定价函数
@tool
def calculate_price(base_price:float,markup:float)->float:
    '''
    calculate_price
    用于计算在基础价格加价后的价格
    参数：base_price基础价格，markup加价百分比(比如0.2代表20%)
    返回：最终价格
    '''
    return base_price*(1+markup)

#调度函数
@tool
def schedule_delivery(order_id:int,delivery_date:str):
    '''
    schedule_delivery
    用于安排配送
    参数：order_id订单编号，delliver_date配送日期
    返回：配送状态或确认信息
    '''
    #在实际应用中这里应该是对接配送系统的过程
    return f"订单{order_id}已安排在{delivery_date}配送"

tools=[check_inventory,calculate_price,check_price,schedule_delivery]

'''
创建Plan-and-Execute Agent并尝试完成一个配送任务'
'''
#设置大模型
from langchain_openai import ChatOpenAI
llm=ChatOpenAI(temperature=0)

#设置计划者和执行者
#导入planner和executor:
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
planner=load_chat_planner(llm=llm)
#设置verboese=True 使得执行者在执行过程中可以输出详细的日志信息
executor=load_agent_executor(llm=llm,tools=tools,verbose=True)

#初始化Plan-and-Execute Agent
agent=PlanAndExecute(planner=planner,executor=executor,verbose=True)
#运行Agent
agent.run("查看玫瑰的库存，并按照加价15%的价格进行配送")

"""
1.ReAct
(1)ReAct框架强调的是“观察-思考-行动”的循环，特别关注如何让大模型更好地理解环境、生成轨迹并采取行动
(2)这个框架特别适用于那些需要大模型与外部环境交互的任务，如信息检索、环境探索等
(3)ReAct框架通过详细记录每一步的推理过程，提高了大模型的可解释性和可靠性

2.Plan-and-Execute
(1)Plan-and-Execute主要关注提升大模型在复杂场景下的性能，引入Plan-and-Execute策略来分解和执行复杂任务
(2)首先，将整个任务分解为更小、更容易管理的子任务、然后波通过更详细的指示，提高生成推理步骤的质量和准确性。
Plan-and-Execute框架优势如下
- 任务分解：通过将大任务分解为小任务，可以有效管理和解决复杂问题
- 详细指导：通过提供详细的指示来改善推理步骤的质量和准确性
- 适应性：可以根据不同类型的任务进行调整，在各种复杂问题中表现出色

"""


