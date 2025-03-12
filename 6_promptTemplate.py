'''
在langchain中，ChatPromptTemplate和PromptTempalte是两种不同的提示模板类，
主要的区别在于适用场景和输入格式
1.PromptTemplate
适用场景：适用于单轮对话或单次输入输出的任务，比如文本生成、文本补全、翻译等
输入格式：接受一个简单的字符串模板，通常是一个完整的提示prompt，用于生成模型的输入
2.ChatPromptTemplate
适用场景：适用于多轮对话任务，比如聊天机器人、对话系统等。它能够处理对话历史并生成模型的输入
输入格式：接受一个消息列表，每条消息可以是一个系统消息、用户消息或助手消息，这些消息共同构成了对话的上下文
'''

#加载环境
from dotenv import load_dotenv
load_dotenv()

#引入chatopenai实例用于多轮对话，接收一个消息列表
from langchain_openai import ChatOpenAI
chat_gpt=ChatOpenAI(model="gpt-3.5-turbo")

#引入openai实例，接收一个字符串
from langchain_openai import OpenAI
gpt=OpenAI()

'''
ChatPromptTemplate示例
'''
from langchain.prompts import ChatPromptTemplate,HumanMessagePromptTemplate,SystemMessagePromptTemplate

#定义系统消息和用户消息模板
system_template="你是一个专业的助手，擅长用简洁的语言回答问题"
user_template="告诉我关于{topic}的信息"

#创建ChatPromptTemplate消息列表
chat_prompt=ChatPromptTemplate.from_messages(
[SystemMessagePromptTemplate.from_template(system_template),
HumanMessagePromptTemplate.from_template(user_template)]
)

#生成提示
prompt=chat_prompt.format_prompt(topic="人工智能的未来").to_messages()
#进行聊天
response=chat_gpt.invoke(prompt)
print(response.content)


'''
PromptTemplate示例
'''


from langchain.prompts import PromptTemplate

#定义消息模板
prompt_template=PromptTemplate(
    input_variables=['topic'],
    template="写一篇关于{topic}的短文"
)

prompt=prompt_template.format(topic="人工智能的发展趋势")
response=gpt.invoke(prompt)
print(response)

