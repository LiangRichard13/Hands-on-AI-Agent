#设置embedding模型的信息
from langchain.embeddings import OpenAIEmbeddings

#加载环境变量
from dotenv import load_dotenv
load_dotenv(override=True)

import os
openai_key =os.getenv("OPENAI_API_KEY")


print("OpenAI API 密钥：", openai_key)
embedding_model_dict = {
    "openai": "text-embedding-ada-002"  # 选择 OpenAI 的 embedding 模型名称
}

def load_embedding_mode(model_name='openai'):
    # 获取模型名称
    model = embedding_model_dict[model_name]
    return OpenAIEmbeddings(model=model, openai_api_key=openai_key)

# 引入embedding模型
embeddings=load_embedding_mode()
print("embedding模型测试：",embeddings.embed_query("My name is RichardLiang13"))