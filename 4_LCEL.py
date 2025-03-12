'''
LangChain Expression Language简称LCEL
它是一种声明式语言，可以使得LangChain中的各个组件组合变得简单且直观
特点：
1.流式处理：在大模型交互的过程中尽可能快地输出首个Token，同时确保数据的连续性和不断输出
2.异步操作：能够在同一台服务器上处理多个并发请求，意味着相同的代码可以从原型系统直接移植到生产系统
3.自动并行执行可以并行的步骤，实现尽可能低的延迟
4.允许配置重试和后备选项，使得链在规模上可靠
5.允许访问复杂链的中间结果，并与LangSmith跟踪和LangServe部署无缝集成
'''

#设置openai的apikey
#导入dotenv包，用于加载环境变量
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

#下面导入所需的库
from langchain_core.output_parsers import StrOutputParser #用于将输出结果解析为字符串
from langchain_core.prompts import ChatPromptTemplate #用于创建聊天提示模板
from langchain_openai import ChatOpenAI #用于调用OpenAI公司的GPT模型  问题：这和from langchain_openai import OpenAI的区别？
'''
ChatOpenAI:用于对话式任务，支持多轮对话，使用对话优化模型如gpt-3.5-turbo,实例化的对象能够接受消息列表(可以通过ChatPromptTemplate创建)
OpenAI:用于单次输入输出的文本生成任务，使用基础GPT模型，实例化的对象能够接受字符串(可以通过PromptTemplate创建)
'''

#创建一个聊天模板，其中{topic}是占位符，用于后续插入具体的话题
prompt=ChatPromptTemplate.from_template("请将一个关于{topic}的故事")

#初始化ChatOpenAI对象，指定使用的模型为gpt-4
model=ChatOpenAI(model="gpt-4")

#初始化一个输出解析器，用于将模型的输出解析为字符串
output_parser=StrOutputParser()

'''
通过管道操作符“|”连接各个处理步骤以创建一个处理链
prompt用于生成具体的提示文本
model用于根据提示文本生成回应
output_parser用于处理回应并将其转换为字符串
'''

#通过串联不同的组件(输入处理、模型调用、输出解析等)来构建复杂的语言处理任务的基本流程
chain=prompt|model|output_parser
message=chain.invoke({"topic":"水仙花"})
#打印链的输出结果
print(message)
