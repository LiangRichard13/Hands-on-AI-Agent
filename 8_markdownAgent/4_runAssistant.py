'''
刚刚我们往创建的线程中添加了消息
现在我们创建一个run
在run的创建过程中我们需要指定线程和助手
让指定的助手去读取指定线程中的消息

thread_id:thread_pAu680jm70SrpJc3KcQBILCZ
assistant_id:asst_aZ4Fnd0hTD7WU1GNkAy19PRO
'''
thread_id="thread_pAu680jm70SrpJc3KcQBILCZ"
assistant_id="asst_aZ4Fnd0hTD7WU1GNkAy19PRO"

#实例化一个client对象
from openai import OpenAI
client=OpenAI()

#创建一个run
run=client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    timeout=30 #加长超时时间
)
#打印run  此时的run处于queued等待状态
print("第一次获取到run的状态:\n",run)
#获取到刚刚创建的run的ID
print("RUN ID:",run.id) # run id:run_TebKRthn1HQmQt0pIicd3nYP

#再次获取run的状态
run=client.beta.threads.runs.retrieve(
    thread_id=thread_id,
    run_id="run_TebKRthn1HQmQt0pIicd3nYP",
    timeout=30 #加长超时时间
    )
print("第二次获取到run的状态:\n",run)

'''
第一次获取到run状态：
status='queued'
第二次获取到run状态：
status='in_progress'
第三次获取到run状态：
status='completed'
'''

'''
run状态说明

1.queued：当创建run或者调用retrieve获取状态后，run状态会转变为queued,
正常情况下run状态很快就会转变为in_progress
2.in_progress：表示run正在执行，可以调用run.step来查看具体执行过程
3.completed：表示run执行成功，可以获取Assistant返回的消息，也可以继续向助手提问
4.requires_action：如果assistant需要执行函数调用，就会转到这个状态，此时需要按给定的参数调用的方法，之后run才可以继续执行
5.expired：当没有在expires_at之前提交函数调用输出或在expires_at之前获取输出，run的状态就会标记为expired
6.cancelling：调用client.beta.threads.runs.cancel后，run的状态就会变为cancelling，取消成功后就会转为cancelled
7.cancelled：表示已成功取消run
8.failed：表示运行失败，可以通过run中的last_error查看失败原因
'''



