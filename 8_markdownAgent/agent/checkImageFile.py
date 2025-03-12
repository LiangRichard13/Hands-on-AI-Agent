from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client=OpenAI()

thread_id="thread_71cGx1GR5yQsbBFecLkFYYVI"

#读取线程消息
messages=client.beta.threads.messages.list(thread_id=thread_id)

#打印消息,展示助手的思考过程

for message in messages.data:
    print('消息ID:',message.id)
    print('助手ID:',message.assistant_id)
    print('消息内容:',message.content[0])
    print('创建时间:',message.created_at)
    print('角色:',message.role)
    print('----------------------------------------------------')

plot_file_id=messages.data[0].content[0].image_file.file_id
print(plot_file_id)


#将输出文件转换为png格式
def convert_file_to_png(file_id,write_path):
    data=client.files.content(file_id)
    data_bytes=data.read()
    with open(write_path,'wb') as file:
        file.write(data_bytes)
image_path="图书销售.png"
convert_file_to_png(plot_file_id,image_path)
#上传图表
plot_file=client.files.create(file=open(image_path,"rb"),purpose='assistants')
