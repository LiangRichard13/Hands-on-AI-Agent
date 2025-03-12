'''
使用来自openai的AssistantAPI创建一个能够使用code interpreter工具的assistant
'''

#导入环境变量
from dotenv import load_dotenv
load_dotenv()

#使用openai创建client
from openai import OpenAI
client=OpenAI()

#创建assistant
assistant=client.beta.assistants.create(
name="鲜花价格计算器",
instructions="你能够帮我计算鲜花的价格",
tools=[{"type":"code_interpreter"}],
model="gpt-4-turbo-preview"
)

#打印assistant
print(assistant)
"""
以下是打印的Assistant信息：

ID:asst_aZ4Fnd0hTD7WU1GNkAy19PRO

Assistant(id='asst_aZ4Fnd0hTD7WU1GNkAy19PRO', 
created_at=1741325563, 
description=None, 
instructions='你能够帮我计算鲜花的价格', 
metadata={}, 
model='gpt-4-turbo-preview', 
name='鲜花价格计算器', 
object='assistant', 
tools=[CodeInterpreterTool(type='code_interpreter')], 
response_format='auto', 
temperature=1.0, 
tool_resources=ToolResources(code_interpreter=ToolResourcesCodeInterpreter(file_ids=[]), 
file_search=None), 
top_p=1.0, 
reasoning_effort=None)

"""