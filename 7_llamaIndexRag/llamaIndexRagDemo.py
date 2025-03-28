#在python中，环境变量通常用于存储敏感信息，如API密钥，通过.env文件管理,避免直接将密钥写在代码中
#load_dotenv()是一个工具函数，用于从.env文件中读取环境变量并加载到python的环境变量中
from dotenv import load_dotenv
load_dotenv()

'''
1.SimpleDirectoryReader:用于从指定目录读取文件并加载为文件对象
2.VectorStoreIndex:用于创建基于向量的索引，方便语义搜索
3.Setting:全局设置类，用于配置LLM和嵌入模型
4.load_index_from_storage：从本地存储加载已保存的索引
5.StorageContext：管理索引的存储上下文
'''
from llama_index.core import SimpleDirectoryReader,VectorStoreIndex,Settings,load_index_from_storage,StorageContext
#导入OpenAI的嵌入模型用于将文本转换为向量
from llama_index.embeddings.openai import OpenAIEmbedding
#导入OpenAI的llm接口，后续会用作回答生成的核心组件
from llama_index.llms.openai import OpenAI

#导入外部知识文档，加载数据，生成文档对象列表，documents是一个列表，每个元素是一个Document对象
documents=SimpleDirectoryReader("D:/Code Projects/AI Agent Learning/7_llamaIndexRag/ragData",encoding="utf-8").load_data()
print("The length of documents_list:",len(documents))
print(documents)

# 设置 LLM
llm = OpenAI(model="gpt-4o")
#Settings是llama_index的全局配置对象，这一设置确保后续所有操作都使用这个llm
Settings.llm = llm

#设置使用的嵌入模型：将文字转换为向量
embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
#确保后续的索引和查询都使用这个嵌入模型
Settings.embed_model = embed_model
print("完成llm和embedding model的全局设置")

'''
创建索引,在这一步会使用openai的text-embedding-ada-002作为embedding model进行语义嵌入

有了索引之后，会使用向量相似性运算，迅速找到与问题最匹配的文档片段

这里没有显式指定分块策略，llamaindex在内部会使用一个默认的文本分块器
默认的chunk_size是1024个token，chunk_overlab是200个token(即前后块之间有少量重叠，避免断句)
'''
index=VectorStoreIndex.from_documents(documents)
print("已创建索引！")

'''
索引持久化，将索引保存到本地目录
storage_context用于管理保存和加载索引的存储上下文
'''
index.storage_context.persist(persist_dir="D:/Code Projects/AI Agent Learning/7_llamaIndexRag/rag_index_storage_vector")
print("已将索引持久化")

#创建存储上下文，从指定目录加载数据
storage_context_vector= StorageContext.from_defaults(persist_dir="D:/Code Projects/AI Agent Learning/7_llamaIndexRag/rag_index_storage_vector")
#从存储上下文加载索引
index=load_index_from_storage(storage_context=storage_context_vector)
print("已加载索引")

'''
创建查询引擎，将向量索引转为查询引起
查询引擎的工作流程是:输入问题->检索相关文档->基于语义相似度返回n个候选片段给llm->调用LLM生成回答
'''
query_engine=index.as_query_engine()

question_a="在花语秘境中有多少种角色？"
question_b="花语秘境中的智能体叫做什么？"

# 两个查询示例
'''
llamaindex的query_engine.query已经形成了一套rag工作流：检索->返回检索结果给大模型->大模型生成回答
而不需要像langchain一样手动定义消息模板
'''
response_with_rag = query_engine.query(question_a)
print("Question",question_a)
print("Response with Rag:",response_with_rag)

response_with_rag = query_engine.query(question_b)
print("Question",question_b)
print("Response with Rag:",response_with_rag)


print('******************************************************************')

response_without_rag=llm.complete(question_a)
print("Question",question_b)
print("Response without Rag",response_without_rag)

response_without_rag=llm.complete(question_b)
print("Question",question_b)
print("Response without Rag",response_without_rag)