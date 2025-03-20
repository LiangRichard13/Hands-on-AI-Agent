from config import assistant_inception_prompt,user_inception_prompt,assistant_role_name,user_role_name,task
from langchain.prompts import SystemMessagePromptTemplate
from langchain.schema import SystemMessage
from typing import Tuple


class SystemMessageGenerator:
    def __init__(self):
        self.assistant_inception_prompt=assistant_inception_prompt
        self.user_inception_prompt=user_inception_prompt
        self.assistant_role_name=assistant_role_name
        self.user_role_name=user_role_name

    def get_sys_msgs(self)->Tuple[SystemMessage,SystemMessage]:
        assistant_sys_template=SystemMessagePromptTemplate.from_template(
            template=self.assistant_inception_prompt
        )
        assistant_sys_msg=assistant_sys_template.format_messages(
            assistant_role_name=self.assistant_role_name,
            user_role_name=self.user_role_name,
            task=task
        )[0]
        user_sys_template=SystemMessagePromptTemplate.from_template(
            template=self.user_inception_prompt
        )
        user_sys_msg=user_sys_template.format_messages(
            assistant_role_name=self.assistant_role_name,
            user_role_name=self.user_role_name,
            task=task
        )[0]

        return assistant_sys_msg,user_sys_msg

# sys_mgs_generator=SystemMessageGenerator()
# assistant_sys_msg,user_sys_msg=sys_mgs_generator.get_sys_msgs()
# print(assistant_sys_msg.content)