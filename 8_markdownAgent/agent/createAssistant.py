from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client=OpenAI()

#导入数据文件并显示前几行
import pandas as pd

def create_assistant(file_path):
    sales_data=pd.read_csv(file_path)

    print(sales_data)

    #创建文件
    file=client.files.create(file=open(file_path,'rb'),purpose='assistants')
    print("成功创建文件")
    #创建一个包含该文件的助手
    assistant=client.beta.assistants.create(
        name="数据可视化助手",
        instructions='作为一名数据科学助理，当给定数据和一个查询时，你能编写适当的代码并创建适当的可视化',
        model='gpt-4o',
        tools=[
            {"type":"code_interpreter"}
        ],
        tool_resources={
            "code_interpreter":{
                "file_ids":[file.id]
            }
        }
    )

    print("已成功创建助手\n",assistant)
    return assistant,file