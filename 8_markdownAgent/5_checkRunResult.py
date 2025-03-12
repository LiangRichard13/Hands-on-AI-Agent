'''
可以通过轮询run.retrieve API定期检查run状态
如果状态变为completed就可以读取Assistant的返回结果

最开始创建的assistant的ID：asst_aZ4Fnd0hTD7WU1GNkAy19PRO
刚才创建的thread的ID：thread_pAu680jm70SrpJc3KcQBILCZ
刚才执行完的run的ID：run_TebKRthn1HQmQt0pIicd3nYP
'''
#导入环境变量
from dotenv import load_dotenv
load_dotenv()

#创建client
from openai import OpenAI
client=OpenAI()


thread_id='thread_pAu680jm70SrpJc3KcQBILCZ'
run_id='run_TebKRthn1HQmQt0pIicd3nYP'

#定义轮询时间
polling_interval=5 # 将轮询时间设为5s

#开始轮询run的状态
import time
while True:
    run=client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
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
elif run_status=='failed' or run_status=='expired':
    print("RUN FAILED OR EXPIRED")


'''
打印结果：

RUN STATUS:completed
RUN COMPLETED SUCCESSFULLY
'''
