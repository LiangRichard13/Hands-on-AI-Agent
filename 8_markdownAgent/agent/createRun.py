from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client=OpenAI()

def create_run(thread,assistant):
    run=client.beta.threads.runs.create(
        assistant_id=assistant.id,
        thread_id=thread.id
    )

    print("成功创建run\n",run)
    return run