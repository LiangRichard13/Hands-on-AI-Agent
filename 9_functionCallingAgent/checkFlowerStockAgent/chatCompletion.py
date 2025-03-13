from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client=OpenAI()

#设定超时时间 稍微延长
client.timeout=10

#定义消息列表
messages=[{"role":"user","content":"北京、上海和深圳的鲜花库存是多少?"}]
print("message:",messages)

from tool import tools,get_flower_inventory
tools_list=tools

#第一次对话响应
first_response=client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    tools=tools_list,
    tool_choice="auto"
)

#打印响应内容
print("First Response",first_response)
response_message=first_response.choices[0].message
print("Frist Reponse Message",response_message)
'''
first_response.choices[0].finish_reason='tool_call'表示对话的原因是需要执行工具
这次输出只是利用大模型返回工具调用，而不是最终的结果，大模型并没有提供具体的回答内容，
而是生成了工具调用请求

first_response.choices[0].message中可以看到在进行function calling时
会强制大模型生成json模式的函数调用信息
'''

import json

#如果这次的回答内容是针对function calling的那么response.choices[0].message.tool_calls就不会为None
tool_calls=response_message.tool_calls
#如果需要调用工具，调用工具并添加库存查询结果，并且将调用工具后的结果添加到对话历史messages中
'''
tool_calls=[ChatCompletionMessageToolCall(id='call_cXM8CZtt6K8lCdEAWqHGmkHS', function=Function(arguments='{"city": "北京"}', name='get_flower_inventory'), type='function'), ChatCompletionMessageToolCall(id='call_AFTwShrOUC4wdXgN5Esrph4e', function=Function(arguments='{"city": "上海"}', name='get_flower_inventory'), type='function'), ChatCompletionMessageToolCall(id='call_q3qMHwcAIDvI1uFQWBnIythX', function=Function(arguments='{"city": "深圳"}', name='get_flower_inventory'), type='function')], annotations=[]))]
'''
if tool_calls:
    messages.append(response_message)
    for tool_call in tool_calls:
        function_name=tool_call.function.name
        function_args=json.loads(tool_call.function.arguments)
        function_response=get_flower_inventory(**function_args)
        messages.append(
            {
                "tool_call_id":tool_call.id,
                "role":"tool",
                "name":function_name,
                "content":function_response
            }
        )
print("messages:",messages)

#现在第二次调用大模型，将之前的调用工具产生的结果输入
second_response=client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages #将更新后的消息列表传入
)

final_response=second_response.choices[0].message.content
print("Final Response:",final_response)

'''
Final Response: 北京的鲜花库存是：玫瑰: 100, 马蹄金香: 150
上海的鲜花库存是：百合: 80, 康乃馨: 120
深圳的鲜花库存是：向日葵: 200, 玉兰: 90
'''