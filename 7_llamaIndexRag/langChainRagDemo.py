#DirectoryLoader用于加载目录下的文档，用于从指定目录中加载所有支持的文件(如.txt、.pdf等)
from langchain_community.document_loaders import DirectoryLoader
#CharacterTextSplitter用于文档切分，确保文档被切成适合嵌入和检索的大小
from langchain.text_splitter import CharacterTextSplitter

#加载embedding模型

#从hugging face导入嵌入模型embedding model
# from langchain.embeddings.huggingface import HuggingFaceEmbeddings

#从openai导入嵌入模型embedding model
from langchain.embeddings import OpenAIEmbeddings

#引入Chroma向量库，Chroma是一个轻量级的向量存储库，用于保存和检索向量
from langchain.vectorstores import Chroma

#加载环境变量如API密钥
from dotenv import load_dotenv
load_dotenv()

#导入PromptTemplate类，用于定义提示词prompt模板，结合检索结果生成回答
from langchain.prompts import PromptTemplate

#导入openai类，用于调用openai的语言模型
from langchain_openai import OpenAI


def load_documents(directory):
    '''
    用于加载和分块文档
    参数: directory 用于rag的文档目录路径
    返回: 分块后的文档列表
    '''
    print('开始加载')
    
    #实例化一个loader通过load()方法加载目录中的文件，返回一个Document对象列表
    loader = DirectoryLoader(path=directory)
    documents = loader.load()
    print("文档数量:",len(documents))
    print("加载的第一个document对象:\n",documents[0])

    print('加载完成，开始切分')

    # 设置切分的大小和切分的重叠部分,块之间重叠 64 个字符，避免信息断裂保持语义连贯性
    text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=64)
    split_docs = text_splitter.split_documents(documents)

    #检查分块数量
    print(f"分块后的文档快数量: {len(split_docs)}")

    print("检查所有文档块")
    for doc in split_docs[:5]:  # 检查前5个文档
        print(f"文档内容: {doc.page_content[:100]}")  # 打印前100个字符
        print(f"文档元数据: {doc.metadata}")
    return split_docs

def load_embedding_model(model='text-embedding-ada-002'):
    '''
    用于加载来自openai的embedding model
    返回一个OpenAIEmbeddings的实例
    '''
    return OpenAIEmbeddings(model=model)

def store_chroma(docs,embeddings,persist_directory='D:/Code Projects/AI Agent Learning/7_llamaIndexRag/LangChainVectorStore'):
    '''
    1.将分块后的文本数据通过embedding model进行嵌入生成向量
    2.将向量数据持久化到磁盘
    3.返回Chroma数据库对象以供后续使用
    '''
    db = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=persist_directory)
    db.persist()
    #这里的向量数据应该和分块后的文档块数量一致
    print(f"数据库中的向量数据: {db._collection.count()}")
    return db


# 引入embedding模型
embeddings=load_embedding_model()
print("embedding模型测试：",embeddings.embed_query("测试文本"))

# 切分文档块
chunks=load_documents(directory="D:/Code Projects/AI Agent Learning/7_llamaIndexRag/ragData")
#做嵌入后存储到向量数据库,返回db对象
db=store_chroma(chunks,embeddings)
print("向量数据库构建完毕")

#从磁盘中加载chroma数据库，并指定相同的embedding model
db=Chroma(persist_directory="D:/Code Projects/AI Agent Learning/7_llamaIndexRag/LangChainVectorStore",embedding_function=embeddings)
#将数据库转换为检索器用于查询相关文档
retriever=db.as_retriever()

query = "在花语秘境中有多少种角色？"
#返回与query语义最接近的文档块列表
results = retriever.get_relevant_documents(query)

# 打印查询结果
print("查询到的文档块:")
for i, result in enumerate(results, 1):
    print(f"结果 {i}:")
    print("内容:", result.page_content[:200])  # 显示前200个字符的内容
    print("元数据:", result.metadata)
    print("\n")

#提取检索结果的内容，这整理为列表
results_set=[result.page_content for result in results]
print("查询到的结果")
print(results_set)

#定义prompt模板
prompt_template="""
用户问题{query},
这是你可以参考的资料{rag_info},
请你回答用户的问题:
"""

#创建PromptTemplate实例,template指定定义的模板,input_variables指定模板中的变量
prompt=PromptTemplate(
    template=prompt_template,
    input_variables=['query','rag_info']
)

#填充prompt模板形成最终提示
message=prompt.format(query=query,rag_info=str(results_set))

llm=OpenAI()

response=llm.invoke(query)
print('******************************************************************')
print("没有通过rag的响应:\n",response)

response=llm.invoke(message)
print("通过rag的响应:\n",response)