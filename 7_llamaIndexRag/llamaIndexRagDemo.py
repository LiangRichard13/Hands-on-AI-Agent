import sys
print(sys.getdefaultencoding())  # 检查默认编码

#加载环境变量
from dotenv import load_dotenv
load_dotenv()

from llama_index.core import SimpleDirectoryReader,VectorStoreIndex,Settings,load_index_from_storage,StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding


#导入外部知识文档，加载数据
documents=SimpleDirectoryReader("ragData",encoding="utf-8").load_data()
print("The length of documents_list:",len(documents))
print(documents)

# from llama_index.llms.openai import OpenAI
import os
# 设置 LLM
# llm = OpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))
# Settings.llm = llm

#设置使用的嵌入模型
embed_model = OpenAIEmbedding(model="text-embedding-ada-002",api_key=os.getenv("OPENAI_API_KEY"))
Settings.embed_model = embed_model

#创建索引,在这一步会默认使用openai的text-embedding-ada-002作为embedding model进行语义嵌入
index=VectorStoreIndex.from_documents(documents)

#索引持久化
index.storage_context.persist(persist_dir="./rag_index_storage_vector")

#从本地路径获取到查询索引
storage_context_vector= StorageContext.from_defaults(persist_dir="./rag_index_storage_vector")
index=load_index_from_storage(storage_context=storage_context_vector)

#创建查询引擎
query_engine=index.as_query_engine()

# 两个查询示例
response = query_engine.query("How many roles do the employees have in the Flower Language Secret Realm?")
print(response)

response = query_engine.query("What is the name of the Agent in the Flower Language Secret Realm?")
print(response)