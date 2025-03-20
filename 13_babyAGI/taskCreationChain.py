from langchain.llms import BaseLLM
from langchain.prompts import PromptTemplate

'''
类方法classmethod是绑定到类而不是实例的 
可以直接通过类名调用而不需要创建类的实例
比如：task_creation_chain=TaskCreationChain.from_llm(llm,verbose=True)

而from_llm实际上是一个工厂方法，用于创建TaskCreationChain的实例
'''

#定义任务生成链
class TaskCreationChain:
    '''
    负责生成任务的链
    基于给定的条件，这个链可以创建新的任务，例如，根据最后一个完成的任务的结果来生成新任务
    '''    
    @staticmethod
    def from_llm(llm:BaseLLM):
        '''从大模型获取响应解析器'''
        task_creation_tamplate=(
            "You are a task creation AI that uses the result fo an execution agent"
            "to create a new tasks with the following objective:{objective},"
            "The last completed task has the result:{result}."
            "This result was based on this task desciption:{task_description}."
            "These are incomplete task:{incomplete_tasks}."
            "Based on the result, create new tasks to be completed"
            "by the AI system that do not overlab with incomplete tasks."
            "Return the tasks as an array."
        )
        prompt=PromptTemplate(
            template=task_creation_tamplate,
            input_variables=[
                "result",
                "task_description",
                "incomplete_tasks",
                "objective"
            ]
        )
        chain=prompt | llm
        return chain
