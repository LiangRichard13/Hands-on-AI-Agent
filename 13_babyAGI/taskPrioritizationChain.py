from langchain.llms import BaseLLM
from langchain.prompts import PromptTemplate

#定义任务优先级链
class TaskPrioritizationChain:
    '''
    负责任务优先级排序的链
    这个链负责重新按任务的优先级排序。给定一个任务列表，它会返回一个新的按优先级排序的任务列表
    '''
    @staticmethod
    def from_llm(llm:BaseLLM):
        """从大模型获取响应解析器"""
        task_prioritization_template=(
        "You are a task prioritization AI tasked with cleaning the formatting of the reprioritizing"
        "the following tasks:{task_name}."
        "Consider the ultiamte objective of your team:{objective}."
        "Do not remove or add any tasks. Return the result as a numbered list, like:"
        "#.First task"
        "#.Second task"
        "Start the task list with number{next_task_id}."
        )
        prompt=PromptTemplate(
            template=task_prioritization_template,
            input_variables=["task_name","objective","next_task_id"]
        )
        chain= prompt | llm

        return chain