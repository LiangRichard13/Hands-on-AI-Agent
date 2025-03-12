from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client=OpenAI()

def create_thread(file,user_content):
    #创建对话线程,可以先创建线程在调用threads.message添加消息，也可以在创建的时候就添加好消息
    thread=client.beta.threads.create(
    messages=[
        {
            "role":"user",
            "content":user_content,
            "attachments":[
                {
                    "file_id":file.id,
                    "tools":[
                        {"type":"code_interpreter"}
                    ]
                }
            ],
        }
    ]
    )
    # 打印创建好的线程
    print("已成功创建线程\n",thread)
    return thread