from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client=OpenAI()

#增加超时时间
client.timeout=10

'''
刚刚创建的encourageAssistant
ID:asst_m7r3SjFoJ7a4s5OcL1WtzgVX
'''
assistant_id='asst_m7r3SjFoJ7a4s5OcL1WtzgVX'

#获取到助手
print("正在获取到assistant")
assistant=client.beta.assistants.retrieve(assistant_id=assistant_id)
print("获取到assistant:",assistant)

def create_run(assistant,user_message):
    '''
    参数:assistant对象,user_message用户指令
    返回:创建好的run对象
    '''
    #创建进程
    print("正在创建进程")
    thread=client.beta.threads.create()
    print("创建进程:",thread)

    #向进程中添加消息
    print("正在向进程中添加消息")
    message=client.beta.threads.messages.create(
        thread_id=thread.id,
        role='user',
        content=user_message
    )
    print("添加消息:",message)

    #创建run
    print("正在创建run")
    run=client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
    print("run的初始信息:",run)
    return thread,run

def check_run_and_return_msg(run,thread):
    #通过轮询来检查run的状态
    import time
    n=0
    while True:
        n+=1
        run=client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"run的第{n}次轮询信息:",run)
        print("RUN STATUS:",run.status)
        if run.status in ['requires_action','completed']:
            print("run已完成")
            break
        time.sleep(5)

    if run.status=='completed':
        #获取assistant在thread中的回应
        message=client.beta.threads.messages.list(
            thread_id=thread.id
        )

        for mes in message.data:
            if mes.role=="assistant":
                return mes.content[0].text.value
            
    if run.status=='requires_action':
        return 'run处于requires_action状态'

'''
获取function细节信息
以下是run.required_action:
required_action=RequiredAction
(submit_tool_outputs=RequiredActionSubmitToolOutputs
(tool_calls=
[RequiredActionFunctionToolCall
(id='call_raKTJYv4fP5O6hqJpSOnlaDl', function=Function
(arguments='
{"name":"小雪","mood":"伤心"
}', name='get_encouragement'
), type='function'
)
]
), type='submit_tool_outputs'
)
'''
#获取function信息
def get_function_details(run):
    if run is not None:
        if run.required_action is not None:
            function_name=run.required_action.submit_tool_outputs.tool_calls[0].function.name
            arguments=run.required_action.submit_tool_outputs.tool_calls[0].function.arguments
            function_id=run.required_action.submit_tool_outputs.tool_calls[0].id
            print("function_name:",function_name)
            print("arguments:",arguments)
            print("function_id:",function_id)
            return function_name,arguments,function_id
        else:
            print("检测到run.required_action为None")
    else:
        print("检测到run为None")
    return "None","None","None"

def submit_tool_outputs(run,thread,function_id,function_response):
    #获取提交function response之后的run对象
    run=client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread.id,
        run_id=run.id,
        tool_outputs=[
            {
                "tool_call_id":function_id,
                "output":str(function_response)
            }
        ]
    )
    return run

'''
不调用Function直接运行助手
'''
# user_message="你好，请介绍一下自己。"
# thread,run=create_run(assistant=assistant,user_message=user_message)
# msg=check_run_and_return_msg(run=run,thread=thread)
# print(msg)

'''
尝试助手的function calling

在运行check_run_and_reutrn_msg()的过程中永远等不到run为completed的状态，
因为assistant会一直等待函数调用而处于requires_action函数调用状态
如果在requires_action的状态中跳出轮询循环,run的状态也一直会是requires_action函数调用状态
'''
user_message="你好，请你安慰一下伤心的小雪吧。"
thread,run=create_run(assistant=assistant,user_message=user_message)
msg=check_run_and_return_msg(run=run,thread=thread)
print(msg)
#重要提示：一定要获取最新的run,这时候才是处于requires_function状态的run,才会包含function calling的信息
run=client.beta.threads.runs.retrieve(run_id=run.id,thread_id=thread.id)
function_name,arguments,function_id=get_function_details(run)
'''
function_name: get_encouragement
arguments: {"name":"小雪","mood":"伤心"}
function_id call_bD6caCZnt7EKo13hm695K4xw
'''
import json
from getEncouragement import get_encouragement
#定义可调用函数的字典，和assistant相应的function_name做匹配
available_function={
    "get_encouragement":get_encouragement
}
#下面开始解析参数
'''
注意json.load()和json.loads()的区别
1.json.load():用于从文件对象中读取json数据转换为python字典
2.json.loads():用于将json格式的字符串转换为python字典
'''
arguments_dict=json.loads(arguments)
#获取到要调用的函数
function_to_call=available_function[function_name]
function_result=function_to_call(**arguments_dict)
print(function_result)

'''
但完成本地函数调用之后，run的状态依旧是requires_function状态，直到10min后为过期状态expired
所以我们需要提交调用结果
'''
run=client.beta.threads.runs.retrieve(run_id=run.id,thread_id=thread.id)
print("完成本地函数调用后的run的状态为:",run.status)

#现在提交本地函数调用后的结果
run=submit_tool_outputs(run=run,thread=thread,function_id=function_id,function_response=function_result)
print("提交调用结果后的run信息:",run)
print("提交调用结果后的run状态",run.status)

#轮询获得run的最后消息
message=check_run_and_return_msg(run,thread)
print(message)
