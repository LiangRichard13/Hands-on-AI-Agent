#DirectoryLoader用于加载目录下的文档
from langchain_community.document_loaders import DirectoryLoader
#CharacterTextSplitter用于文档切分
from langchain.text_splitter import CharacterTextSplitter
#加载embedding模型
# from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.embeddings import OpenAIEmbeddings
#引入Chroma向量库
from langchain.vectorstores import Chroma

#加载环境变量
from dotenv import load_dotenv
load_dotenv()

import os
openai_key =os.getenv("OPENAI_API_KEY")

#设置embedding模型的信息
embedding_model_dict = {
    "openai": "text-embedding-ada-002"  # 选择 OpenAI 的 embedding 模型名称
}

def load_documents(directory='./ragData'):
    print('开始加载')
    loader = DirectoryLoader(directory)
    documents = loader.load()
    print('加载完成，开始切分')
    # 设置切分的大小和切分的重叠部分
    text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=64)
    split_docs = text_splitter.split_documents(documents)

    # 检查切分后的第一个文档块
    print("检查切分后的第一个文档块")
    print(split_docs[0], '\n')
    print(f"Number of split documents: {len(split_docs)}")

    print("检查前五个文档")
    for doc in split_docs[:5]:  # 检查前5个文档
        print(f"Document content: {doc.page_content[:100]}")  # 打印前100个字符
        print(f"Document metadata: {doc.metadata}")
    return split_docs

def load_embedding_mode(model_name='openai'):
    # 获取模型名称
    model = embedding_model_dict[model_name]
    return OpenAIEmbeddings(model=model, openai_api_key=openai_key)

def store_chroma(docs,embeddings,persist_directory='LangChainVectorStore'):
    db = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=persist_directory)
    db.persist()
    print(f"Number of vectors in database: {db._collection.count()}")
    return db

# 引入embedding模型
embeddings=load_embedding_mode()
print("embedding模型测试：",embeddings.embed_query("测试文本"))

# #切分文档块
chunks=load_documents()
#做嵌入后存储到向量数据库,返回db对象
db=store_chroma(chunks,embeddings)
print("向量数据库构建完毕")


#直接读取向量数据库
db=Chroma(persist_directory="LangChainVectorStore",embedding_function=embeddings)
retriever=db.as_retriever()

query = "What is the name of the Agent in the Flower Language Secret Realm?"
results = retriever.get_relevant_documents(query)

# 打印查询结果
print("查询到的文档块:")
for i, result in enumerate(results, 1):
    print(f"结果 {i}:")
    print("内容:", result.page_content[:200])  # 显示前200个字符的内容
    print("元数据:", result.metadata)
    print("\n")

results_set=[result.page_content for result in results]
print("查询到的结果")
print(results_set)
print(type(results_set))
