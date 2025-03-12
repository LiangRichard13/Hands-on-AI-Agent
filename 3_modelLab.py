#导入dotenv包，用于加载环境变量
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

#这里还需要COHERE_API_KEY和HUGGINGFACEHUB_API_TOKEN

#导入dotenv包，用于加载环境变量
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入langchain_openai库中的OpenAI类
from langchain_openai import OpenAI

# 导入langchain_community.llms中的Cohere和HuggingFaceHub类
from langchain_community.llms.huggingface_hub import HuggingFaceHub
from langchain_community.llms.cohere import Cohere

# 初始化大模型的实例，并设置temperature参数（控制生成文本的创新性）
openai = OpenAI(temperature=0.1)
cohere = Cohere(model="command", temperature=0.1)
huggingface = HuggingFaceHub(repo_id="tiuae/falcon-7b", model_kwargs={'temperature': 0.1})

# 导入ModelLaboratory类，用于创建和管理多个大模型
from langchain.model_laboratory import ModelLaboratory

# 创建一个模型实验室实例，整合OpenAI、Cohere和HuggingFace的模型
model_lab = ModelLaboratory.from_llms([openai, cohere, huggingface])

# 使用模型实验室比较不同模型对同一个问题的回答
model_lab.compare("百合花源自哪个国家?")