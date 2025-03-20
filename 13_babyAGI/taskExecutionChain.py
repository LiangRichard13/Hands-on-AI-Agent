from langchain_core.language_models import BaseLLM  # 更新导入
from langchain.prompts import PromptTemplate

# 定义任务执行链
class ExecutionChain:
    """
    负责执行任务的链
    这个链负责执行具体的任务，并返回结果
    """
    @staticmethod
    def from_llm( llm: BaseLLM):
        """从大模型获取响应解释器"""
        execution_template = (
            "You are an AI who performs one task based on the following objective: {objective}.\n"
            "Take into account these previously completed tasks: {context}.\n"
            "Your task: {task}.\n"
            "Response:"
        )
        prompt = PromptTemplate(
            template=execution_template,
            input_variables=["objective", "context", "task"]
        )

        chain = prompt | llm  # 使用管道操作符构造链
        return chain