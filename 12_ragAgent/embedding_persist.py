from llama_index.core import SimpleDirectoryReader

#加载文件
'''
input_files List 接受一个文件路径列表
input_dir Str 接受一个文件夹路径，会读取该路径下的文件
'''
docs=SimpleDirectoryReader(
    input_files=["./document/news.pdf"]
).load_data()

#将文件转换构建为向量数据
#这里不指定embedding model就会使用默认的embedding model
from llama_index.core import VectorStoreIndex
index=VectorStoreIndex.from_documents(docs)

#持久化索引，保存到本地
index.storage_context.persist(persist_dir='./news_embeddings_storage')
