'''
创建一个线程

什么是线程？
一个线程就代表和OpenAI公司大模型的一次对话
'''

#使用openai创建client
from openai import OpenAI
client=OpenAI()

#创建一个线程
thread=client.beta.threads.create()
#打印线程
print(thread)

'''
线程创建好后，线程将在后台一直运行

和assistant的关系？
1.线程thread和assistant是两个独立的组件
2.助手就是assistant,指的是提供服务的AI模型，负责处理用户的请求、生成回复等
3.线程就是Tread，用来表示一系列的交互或对话。一个线程可能包含一个或多个由用户和助手之间的交互组成的连续对话
4.assistant负责处理具体的请求，而线程主要关注对话的组织和管理
5.一个线程可以有多个助手一个助手可以有多个线程
'''
