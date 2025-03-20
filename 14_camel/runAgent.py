from camelAgent import CamelAgent
from langchain_openai import ChatOpenAI
from systemMessageGen import SystemMessageGenerator
from langchain.schema import HumanMessage
from config import chat_turn_limit,user_role_name,assistant_role_name,task
from specifier import SpecifierAgent

#获取assistant和user的系统消息
sys_msg_generator=SystemMessageGenerator()
assistant_sys_msg,user_sys_msg=sys_msg_generator.get_sys_msgs()

#创建AI助手和AI用户的Camel Agent实例
assistant_agent=CamelAgent(
    model=ChatOpenAI(model="gpt-4o",temperature=1.0),
    system_message=assistant_sys_msg
)

user_agent=CamelAgent(
    model=ChatOpenAI(model="gpt-4o",temperature=1.0),
    system_message=user_sys_msg
)

#重置两个agent
assistant_agent.reset()
user_agent.reset()

#细化任务
specifier=SpecifierAgent()
task,specified_task_content=specifier.specified()
print(f"Original Task:{task}")
print(f"Specified Task:{specified_task_content}")

print("------------------------Begin!!!!------------------------")

#初始化对话交互
assistant_msg=HumanMessage(
    content=(
        f"现在我是{user_role_name}"
        f"下面开始我们的任务{task}"
        f"这是细化后的任务安排{specified_task_content}"
        "现在开始逐一给我介绍"
    )
)

#下面模拟对话交互
n=0 # 当前交互次数
while n<chat_turn_limit:
    n+=1
    user_ai_msg=assistant_agent.step(input_message=assistant_msg)
    user_msg=HumanMessage(content=user_ai_msg.content)
    print(f"AI Assistant Role:{assistant_role_name}")
    print(f"AI Assistant Message:{user_msg.content}")
    
    print("------------------------Next Turn------------------------")

    assistant_ai_msg=user_agent.step(input_message=user_msg)
    assistant_msg=HumanMessage(content=assistant_ai_msg.content)
    print(f"AI User Role:{user_role_name}")
    print(f"AI User Message:{assistant_msg.content}")
    print("\n")

    if "<CAMEL_TASK_DONE>" in assistant_msg.content:
        break