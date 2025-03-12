from dotenv import load_dotenv
load_dotenv()

'''
一旦assistant运行完成，也就是run的状态为completed
我们就可以查看当前线程的最新情况，方法是列出线程中的消息

最新消息是run完成时添加到线程中的，它是assistant给我们的响应
这个响应就代表这轮对话的完成结果
'''

#创建client
from openai import OpenAI
client=OpenAI()

#刚才创建的Thread的ID
thread_id='thread_pAu680jm70SrpJc3KcQBILCZ'

#读取线程消息
messages=client.beta.threads.messages.list(thread_id=thread_id)

#打印消息

print('消息ID:',messages.data[1].id)
print('助手ID:',messages.data[1].assistant_id)
print('消息内容:',messages.data[1].content[0].text.value)
print('创建时间:',messages.data[1].created_at)
print('角色:',messages.data[1].role)
print('----------------------------------------------------')
print('消息ID:',messages.data[0].id)
print('助手ID:',messages.data[0].assistant_id)
print('消息内容:',messages.data[0].content[0].text.value)
print('创建时间:',messages.data[0].created_at)
print('角色:',messages.data[0].role)