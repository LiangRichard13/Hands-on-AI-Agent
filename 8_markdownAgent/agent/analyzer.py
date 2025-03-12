from openai import OpenAI

client=OpenAI()

#定义提交用户消息的函数
'''
函数首先会检查线程中的所有run
如果存在正在进行的run则会等待它们完成
一旦所有运行都完成，函数就会提交新的任务

通过submit_message_wait_completion函数发送请求，让assistant生成见解

assistant id:asst_waSo5qTu1rTor0fhr2M0bVhU
thread id:thread_GA5FTRCPDUHuIN2vRi7wV67v
run id:run_63Ew8Zp9yESlzhfiY9RGNoOZ
'''

import time

def submit_message_wait_completion(assistant_id,thread,user_message,file_ids=None):
    #检查并等待活跃的Run完成
    for run in client.beta.threads.runs.list(thread_id=thread.id).data:
        if run.status =='in_progress':
            print(f"等待RUN {run.id}完成...")
            while True:
                run_status=client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id).status
                if run_status in ['failed','succeeded']:
                    break
                time.sleep(2)
    #设置提交消息参数模板
    params={
        'thread_id':thread.id,
        'role':'user',
        'content':user_message
    }
    #如果有文件的话设置attachments附件参数
    if file_ids:
        attachments=[{"file_id":file_id,"tools":[
            {"type":"code_interpreter"}
        ]} for file_id in file_ids ] 
        params['attachments']=attachments
    client.beta.threads.messages.create(**params)

    #使用消息参数模板创建run
    run=client.beta.threads.runs.create(thread_id=thread.id,assistant_id=assistant_id)
    return run 

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id)

def check_run_status(thread_id,run,polling_interval):
    #开始轮询run的状态
    while True:
        run=client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

        # 直接访问run对象的属性
        run_status=run.status
        print(f"RUN STATUS:{run_status}")
        # 如果run的状态是completed,failed,expired则退出循环
        if run_status in['completed','failed','expired']:
            break

        #等待一段时间之后再次轮询
        time.sleep(polling_interval)

    #在run运行完成或失败后处理结果
    if run_status=='completed':
        print("RUN COMPLETED SUCCESSFULLY")
        return True
    elif run_status=='failed' or run_status=='expired':
        print("RUN FAILED OR EXPIRED")
        return False


# assistant_id='asst_waSo5qTu1rTor0fhr2M0bVhU'
# thread_id='thread_GA5FTRCPDUHuIN2vRi7wV67v'
# run_id='run_63Ew8Zp9yESlzhfiY9RGNoOZ'

# #获取线程
# thread=client.beta.threads.retrieve(thread_id=thread_id)
# print(thread)
# #定义消息
# user_message="请你根据刚才创建的图表，给我两个约20字的句子，描述最重要的见解。这将用于ppt展示，揭示数据背后的秘密"
# run=submit_message_wait_completion(assistant_id=assistant_id,thread=thread,user_message=user_message)
# #定义轮询时间
# polling_interval=5 # 将轮询时间设为5s
# if check_run_status(thread_id,run,polling_interval):
#     response=get_response(thread=thread)
#     assistant_point=response.data[0].content[0].text.value
#     print(assistant_point)