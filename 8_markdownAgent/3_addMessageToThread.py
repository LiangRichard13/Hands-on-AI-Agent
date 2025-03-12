'''
Thread(id='thread_pAu680jm70SrpJc3KcQBILCZ', 
created_at=1741327293, 
metadata={}, 
object='thread', 
tool_resources=ToolResources(code_interpreter=None, file_search=None))

以上是我们刚刚创建的线程
下面我们向线程中添加消息
'''

#创建client实例
from openai import OpenAI
client=OpenAI()

#添加消息
message=client.beta.threads.messages.create(
thread_id="thread_pAu680jm70SrpJc3KcQBILCZ",
role="user",
content="我把每束花定价为进价的基础上加价20%，当我的进价为80元，我的售价为多少？"
)

#获取消息列表
message_list=client.beta.threads.messages.list(
    thread_id='thread_pAu680jm70SrpJc3KcQBILCZ'
)
#打印消息
print(message_list)

'''
SyncCursorPage[Message](data=[Message(id='msg_0EO5RyiX5XMKze3VQoGrGPLE',
 assistant_id=None, 
 attachments=[], 
 completed_at=None, 
 content=[TextContentBlock(text=Text(annotations=[], 
 value='我把每束花定价为进价的基础上加价20%，当我的进价为80元，我的售价为多少？'), 
 type='text')], 
 created_at=1741327903, 
 incomplete_at=None, 
 incomplete_details=None, 
 metadata={}, 
 object='thread.message', 
 role='user', 
 run_id=None, 
 status=None, 
 thread_id='thread_pAu680jm70SrpJc3KcQBILCZ')], 
 has_more=False, 
 object='list', 
 first_id='msg_0EO5RyiX5XMKze3VQoGrGPLE', 
 last_id='msg_0EO5RyiX5XMKze3VQoGrGPLE')
'''
