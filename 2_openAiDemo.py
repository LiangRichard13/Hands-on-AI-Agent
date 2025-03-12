#导入dotenv包，用于加载环境变量
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

#导入openai库
from openai import OpenAI
#创建client
'''
client作为实例名称：
1.OpenAI类的实例充当客户端，用于向OpenAI公司的服务器发送API请求并接收响应
2.API交互，client这个词通常用于指代一个应用程序或应用程序的组成部分，与外部服务器进行交互
'''
client=OpenAI()


#OpenAI API聊天程序
#调用chat.completions.create方法得到响应
response=client.chat.completions.create(
    model="gpt-4-turbo-preview",
    response_format={"type":"json_object"},
    messages=[
        {"role":"system","content":"你是一个帮助用户了解鲜花信息的智能助手并能够输出json格式的内容"},
        {"role":"user","content":"生日送什么花好？"}
        ]
)
print(response.choices[0].message.content)

#OpenAI 文生图
#请求Dalle生成图片
response=client.images.generate(
    model="dall-e-3",
    prompt="电商花语秘境的新春玫瑰花宣传海报并配上文案",
    size="1024x1024",
    quality="standard",
    n=1,
)

#获取图片url
image_url=response.data[0].url
#读取图片
import requests
image_data=requests.get(image_url).content
# 显示图片

from PIL import Image
from io import BytesIO

image = Image.open(BytesIO(image_data))
image.show()
