# 导入OpenAI库，创建client
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client=OpenAI()

'''
1.导入文件并使用client.files.create创建文件
2.使用client.beta.assistants.create创建assistant
3.使用client.beta.threads.create创建对话线程
4.使用client.beta.threads.runs.create来创建run来运行和assistant的对话
5.通过轮询检查并等待可视化完成
6.将assistant输出的文件转换为png格式

7.根据图表让assistant生成见解
8.让assistant创建页面标题
9.让dalle生成配图
10.创建文档
'''
#创建assistant
from createAssistant import create_assistant
file_path='sales_data.csv'
assistant,file=create_assistant(file_path=file_path)

#创建对话线程,可以先创建线程在调用threads.message添加消息，也可以在创建的时候就添加好消息
from createThread import create_thread
user_content="我上传了一个csv文件，请计算从2022年到2025年每个季度的总销售额，并通过不同的产品将其可视化为折线图，产品线条分别为红，蓝，绿, 图表上的文字请使用英文"
thread=create_thread(file=file,user_content=user_content)


#创建run来运行assistant的对话
from createRun import create_run
run=create_run(thread=thread,assistant=assistant)

from checkPlotCompleted import check_plot
messages=check_plot(thread=thread)


#将输出文件转换为png格式
from convert_file_to_png import convert_file_to_png
try:
    plot_file_id=messages.data[0].content[0].image_file.file_id
    image_path="图书销售.png"
    convert_file_to_png(plot_file_id,image_path)
    #上传图表
    plot_file=client.files.create(file=open(image_path,"rb"),purpose='assistants')
except Exception as e:
    print("折线图没有正常生成...")


'''
以上是图表创建的过程，下面是根据图表让agent生成相关的见解
'''
from analyzer import submit_message_wait_completion,check_run_status,get_response
user_message="请你根据刚才创建的图表，给我两个约20字的句子，描述最重要的见解。这将用于文档，揭示数据背后的秘密"

#submit_message_wait_completion的作用是等待图表创建的run完成，然后创建新的run用于提交见解生成指令
run=submit_message_wait_completion(assistant_id=assistant.id,thread=thread,user_message=user_message)
if check_run_status(thread.id,run,5):#检查见解生成run是否完成
    #获取见解响应
    response=get_response(thread=thread)
    assistant_point=response.data[0].content[0].text.value
    print(assistant_point)
else:
    assistant_point="Error Occurred"

'''
以上是图表创建和见解生成的过程，下面让assistant生成标题
'''
user_message="根据你创建的情节和要点，想一个非常简短的标题，反映你得出的主要见解"
run=submit_message_wait_completion(assistant_id=assistant.id,thread=thread,user_message=user_message)
if check_run_status(thread.id,run,5):
    #获取标题响应
    response=get_response(thread=thread)
    assistant_title=response.data[0].content[0].text.value
    print(assistant_title)
else:
    assistant_title="Error Occurred"


'''
使用DALLE3模型为首页配图
'''
company_summary="虽然我们是初创网络鲜花批发商，但是我们董事长也写IT图书"

#调用DALLE3模型生成图片
response=client.images.generate(
    model='dall-e-3',
    prompt=f"根据这家公司的简介{company_summary},创建一张展示花语秘境公司共同成长和前进道路的启发性照片。这将用于季度销售规划会议",
    size="1024x1024",
    quality="hd",
    n=1
)
image_url=response.data[0].url
#通过url获取生成的图片
import requests
dalle_img_path="封面海报.png"
img=requests.get(image_url)
#将图片保存到本地
with open(dalle_img_path,'wb') as file:
    file.write(img.content)
print("封面已生成！")
#将上传的图片作为素材之一
dalle_file=client.files.create(
    file=open(dalle_img_path,'rb'),
    purpose='assistants'
)

'''
最后一步完成文档的创作
'''

title_text="花语秘境"
subtitle_text="2025年销售大会"
user_message=f"""
你的任务是根据之前生成的信息创建一个markdown文档。具体构建顺序要求如下：\n
1.markdown文档的主标题为{title_text}\n
2.markdown文档的副标题为{subtitle_text}\n
3.在markdown文档中插入之前生成的配图，配图的插入路径为{dalle_img_path}\n
4.在markdown文档中插入之前的生成的折线图，折线图的插入路径为{image_path}\n
5.在markdown文档中插入折线图标题，具体为{assistant_title}\n
6.在markdown文档中插入折线图配文，具体为{assistant_point}\n
7.确保输出为md格式的文件
"""

submit_message_wait_completion(assistant_id=assistant.id,user_message=user_message,thread=thread,file_ids=[dalle_file.id,plot_file.id])

import time
#等待助手完成文档创建的任务

"""
消息列表中最近的一条消息如下：

Message(id='msg_HzpWx6zJDMinaq1SDD98oDTL', 
assistant_id='asst_DIjgLmsBLeJ3zhHqRP6J68PK', 
attachments=[Attachment(file_id='file-JrFj1yfixjEnTESLc8CJRe', 
tools=[CodeInterpreterTool(type='code_interpreter')])], 
completed_at=None, 
content=[TextContentBlock(text=Text(annotations=[FilePathAnnotation(end_index=92, 
file_path=FilePath(file_id='file-JrFj1yfixjEnTESLc8CJRe'), 
start_index=50, 
text='sandbox:/mnt/data/Sales_Conference_2025.md', 
type='file_path')], 
value='已创建markdown文档，可从以下位置下载：
[Sales_Conference_2025.md](sandbox:/mnt/data/Sales_Conference_2025.md)。'), type='text')], 
created_at=1741746590, 
incomplete_at=None, 
incomplete_details=None, 
metadata={}, 
object='thread.message', 
role='assistant', 
run_id='run_IkeLWUsCWZQiwGvKPl7iUeiR', 
status=None, 
thread_id='thread_LFOvoOLa1GGtGKivguh5h6M7')
"""
while True:
    try:
        response=get_response(thread=thread)
        md_id=response.data[0].content[0].text.annotations[0].file_path.file_id
        print("成功检索到md_id",md_id)
        break
    except Exception as e:
        print("您的助手正在努力制作文档")
        print(str(e))
        print("当前消息",response.data[0])
        time.sleep(5)

import io

md_id=response.data[0].content[0].text.annotations[0].file_path.file_id
md_file=client.files.content(md_id)
file_obj=io.BytesIO(md_file.read())
with open("花语秘境.md",'wb') as f:
    f.write(file_obj.getbuffer())