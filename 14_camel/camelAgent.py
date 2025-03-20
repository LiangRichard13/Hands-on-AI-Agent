from typing import List
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage,HumanMessage,SystemMessage,BaseMessage

#定义Camel Agent类
class CamelAgent:
    def __init__(self,system_message:SystemMessage,model:ChatOpenAI)->None:
        self.system_message=system_message
        self.model=model
        self.init_messages()
    
    def reset(self)->None:
        """
        重置对话消息
        
        将将stored_messages置为空列表并只添加最初的系统消息
        返回处理后的stored_messages
        """
        self.init_messages()
        return self.stored_messages
    
    def init_messages(self)->None:
        """
        初始化对话消息

        将stored_messages置为空列表并只添加最初的系统消息
        """
        self.stored_messages=[self.system_message]

    def update_message(self,message:BaseMessage)->List[BaseMessage]:
        """
        更新对话消息列表
        
        将新消息加入到stored_messages中
        """
        self.stored_messages.append(message)
        return self.stored_messages
    
    def step(self,input_message:HumanMessage)->AIMessage:
        """
        与大模型进行交互
        
        中间会将输入和输出存入到stored_messages中
        最后返回大模型的输出
        """
        messages=self.update_message(input_message)
        output_message=self.model.invoke(messages)
        self.update_message(output_message)
        return output_message