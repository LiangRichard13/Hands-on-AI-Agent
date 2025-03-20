from pydantic import BaseModel,Field,ConfigDict
from collections import deque
from langchain_core.runnables import RunnableSequence
from taskCreationChain import TaskCreationChain
from taskPrioritizationChain import TaskPrioritizationChain
from taskExecutionChain import ExecutionChain
from langchain.vectorstores.base import VectorStore
from typing import Dict,List,Optional,Any
from taskManage import TaskManage
from langchain.llms import BaseLLM

#BabyAGI主类
class BabyAGI(BaseModel):
    model_config=ConfigDict(arbitrary_types_allowed=True)
    """
    Baby AGI Agent的控制器模型
    """

    task_list: deque = Field(default_factory=deque, description="任务队列，用于存储待处理的任务")
    task_creation_chain: RunnableSequence = Field(..., description="任务生成链，用于创建新任务") #Filed(...)表示不指定初始值但必填
    task_prioritization_chain: RunnableSequence = Field(..., description="任务优先级链，用于重新排序任务")
    execution_chain: RunnableSequence = Field(..., description="执行链，用于执行任务")
    task_id_counter: int = Field(default=1, description="任务ID计数器，用于生成唯一的任务ID")
    vectorstore: VectorStore = Field(init=False, description="向量存储工具，用于存储和检索任务相关的向量数据") #init=False 表示该字段不会出现在构造函数中,初始化时不能直接进行赋值
    max_iterations: Optional[int] = Field(default=None, description="最大迭代次数，用于控制 BabyAGI 的执行循环") #Optional[int] 相当于 Union[int, None]
    
    def add_task(self,task:Dict):
        self.task_list.append(task) #往任务队列中添加新任务
    
    def print_task_list(self):
        print("********************TASK LIST********************\n")
        for t in self.task_list:
            print(str(t["task_id"])+":"+t["task_name"])
    
    def print_next_task(self,task:Dict):
        print("********************Next TASK********************\n")
        print(str(task["task_id"])+":"+task["task_name"])
    
    def print_task_result(self,result:str):
        print("********************TASK RESULT********************\n")
        print(result)
    
    @property
    def input_keys(self)->List[str]:
        return ["objective"]
    
    @property
    def output_keys(self)->List[str]:
        return []
    
    def call(self,inputs:Dict[str,Any]):
        """Run The Agent"""
        objective=inputs["objective"]
        first_task=inputs.get("first_task","Make a todo list") #从inputs字典中获取键为first_task的值如果没有的话就返回默认值Make a todo list
        self.add_task({"task_id":1,"task_name":first_task})
        num_iters=0
        while True:
            if self.task_list:
                self.print_task_list()

            #第1步：获取第一个任务
            task=self.task_list.popleft() #从双端队列中的左端移除并返回一个元素
            self.print_next_task(task)

            #第2步：执行任务
            result=TaskManage.execute_task(
                vectorstore=self.vectorstore,
                execution_chain=self.execution_chain,
                objective=objective,
                task=task["task_name"]
            )
            this_task_id=int(task["task_id"])
            self.print_task_result(result)

            #第3步：将结果存储到向量数据库中
            result_id=f"result_{task["task_id"]}_{num_iters}"
            self.vectorstore.add_texts(
                texts=[result],
                metadatas=[{"task":task["task_name"]}],
                ids={result_id}
            )

            #第4步：根据上一个任务的描述和结果创建新任务并重新根据优先级排到任务列表中
            new_tasks=TaskManage.get_next_task(
                task_creation_chain=self.task_creation_chain,
                result=result,
                task_description=task["task_name"],
                task_list=[t["task_name"] for t in self.task_list],
                objective=objective
            )
            for new_task in new_tasks:
                self.task_id_counter+=1
                #朝每个new_task中添加一个新的键值对即task_id
                new_task.update({"task_id":self.task_id_counter})
                self.add_task(new_task)
            self.task_list=deque(
                TaskManage.prioritize_tasks(
                    task_prioritization_chain=self.task_prioritization_chain,
                    this_task_id=this_task_id,
                    task_list=list(self.task_list),
                    objective=objective
                )
            )
            num_iters+=1

            if self.max_iterations is not None and num_iters==self.max_iterations:
                 print("********************TASK ENDING********************\n")
                 break
        return
    
    @classmethod
    def create_controller(cls,llm:BaseLLM,vectorstore:VectorStore,max_iterations)->"BabyAGI":
        """
        Initialize the BabyAGI Controller
        
        初始化BabyAGI Controller的本质是创建各种用于管理任务的chain,这种chain在langchain中属于RunnableSequence类
        在本项目中它建立了prompt模板预定义到llm调用的pipline
        (当然还包括一个基于FAISS的向量存取工具vectorstore和指定的最大迭代循环次数max_iterations)

        这里只是创建了它们,真正的调用需要通过invoke进行调用
        """
        task_creation_chain=TaskCreationChain.from_llm(llm=llm)
        task_prioritization_chain=TaskPrioritizationChain.from_llm(llm=llm)
        execution_chain=ExecutionChain.from_llm(llm=llm)
        return cls(
            task_creation_chain=task_creation_chain,
            task_prioritization_chain=task_prioritization_chain,
            execution_chain=execution_chain,
            vectorstore=vectorstore,
            max_iterations=max_iterations
        )