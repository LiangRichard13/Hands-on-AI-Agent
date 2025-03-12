from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client=OpenAI()

import time

def check_plot(thread):
    #通过轮询检查run的状态并等待可视化完成
    max_retry_times=20
    retry_time=0
    while True:
        try:
            #检查是否创建了图像
            messages=client.beta.threads.messages.list(thread_id=thread.id)
            if messages.data and messages.data[0].content[0].image_file:
                print("图表已创建！")
            return messages
        except:
            if retry_time==max_retry_times:
                print('已经达到agent最大的尝试次数')
                return
            retry_time+=1
            time.sleep(5)
            print('你的助手正在努力做图表')
            if messages.data and messages.data[0].content:
                print("当前Message",messages.data[0].content[0].text.value)