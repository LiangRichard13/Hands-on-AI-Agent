'''
thread_id=thread_LFOvoOLa1GGtGKivguh5h6M7
'''

from openai import OpenAI

client=OpenAI()
thread_id="thread_LFOvoOLa1GGtGKivguh5h6M7"
message=client.beta.threads.messages.list(thread_id=thread_id)
print(message.data[0])