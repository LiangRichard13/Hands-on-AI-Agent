from langchain.prompts import HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from camelAgent import CamelAgent
from config import task_specifier_prompt,task_specifier_sys_msg,assistant_role_name,user_role_name,task,word_limit
from typing import Tuple    

class SpecifierAgent(CamelAgent):
    def __init__(self) -> None:
        # 加载任务细化指令的prompt模板
        self.task_specifier_template = HumanMessagePromptTemplate.from_template(template=task_specifier_prompt)
        # 使用CamelAgent作为task_specifier_agent
        super().__init__(system_message=task_specifier_sys_msg, model=ChatOpenAI(model="gpt-4o", temperature=1.0))
        # 填充prompt模板形成完整消息 
        self.task_specifier_msg = self.task_specifier_template.format_messages(
            assistant_role_name=assistant_role_name,
            user_role_name=user_role_name,
            task=task,
            word_limit=word_limit
        )[0]
        # print(type(self.task_specifier_msg))

    def specified(self) -> Tuple[str, str]:
        specified_task_response = self.step(input_message=self.task_specifier_msg)
        specified_task_content = specified_task_response.content   
        return task, specified_task_content
    
# specifier=SpecifierAgent()
# task,specified_task_contente=specifier.specified()
# print(task)
# print(specified_task_contente)