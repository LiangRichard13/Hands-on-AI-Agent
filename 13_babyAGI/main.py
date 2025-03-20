#加载相关环境
from dotenv import load_dotenv
load_dotenv()

#导入所需的库和模块
'''
collections是python标准库中的一个模块，提供了许多有用的数据结构
用于扩展内置的数据类型

其中deque是collection模块中的一个类，全称叫做"double-ended-queue"双端队列
允许再队列的两端即头部和尾部进行高效的插入和删除操作
'''
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import faiss
from langchain.docstore import InMemoryDocstore
from langchain_openai import OpenAI
from controller import BabyAGI

'''
主函数部分
'''

#定义嵌入模型
embeddings_model=OpenAIEmbeddings()

#初始化向量数据库
'''
embedding_size=1536指定了向量的维度为1536，这是OpenAI嵌入模型的默认输出维度
index=faiss.IndexFlatL2(embedding_size)使用Faiss创建一个基于L2(欧氏距离)的暴力搜索索引
这是一种简单的索引类型，适合小规模数据
'''
embedding_size=1536
index=faiss.IndexFlatL2(embedding_size)
'''
创建一个基于Faiss的向量存储，用于管理向量和文档
embeddings_model.embed_query用于指定生成嵌入向量的函数
index指定了IndexFlatL2的向量索引
InMemoryDocstore指定使用内存中的文档存储
'''
vectorstore=FAISS(embeddings_model.embed_query,index,InMemoryDocstore({}),{})

OBJECTIVE="请帮我写一份关于人工智能在中医领域的综述"
llm=OpenAI(temperature=0,model="gpt-3.5-turbo-instruct")
max_iterations=20
baby_agi=BabyAGI.create_controller(llm=llm,vectorstore=vectorstore,max_iterations=max_iterations)
baby_agi.call(inputs={"objective":OBJECTIVE})