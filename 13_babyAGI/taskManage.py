from typing import Dict,List,Optional,Any

class TaskManage:
    #获取下一个任务
    @staticmethod
    def get_next_task(
            task_creation_chain,
            result:Dict,
            task_description:str,
            task_list:List[str],
            objective:str
    )->List[Dict]:
        """Get the next task."""
        incomplete_tasks=".".join(task_list)
        response=task_creation_chain.invoke(
            {
                "result":result,
                "task_description":task_description,
                "incomplete_tasks":incomplete_tasks,
                "objective":objective
            }
        )
        new_tasks=response.split("\n")
        return [{"task_name":task_name} for task_name in new_tasks if task_name.strip()]
    
    #设置任务优先级
    @staticmethod
    def prioritize_tasks(
            task_prioritization_chain,
            this_task_id:int,
            task_list:List[Dict],
            objective:str
    )->List[Dict]:
        """Prioritize tasks"""
        task_names=[task["task_name"] for task in task_list]
        next_task_id=int(this_task_id)+1
        resposne=task_prioritization_chain.invoke(
            {
                "task_name":task_names,
                "objective":objective,
                "next_task_id":next_task_id,
            }
        )
        new_tasks=resposne.split("\n")
        prioritized_task_list=[]
        for task_string in new_tasks:
            if not task_string.strip():#如果task_string是""则跳过
                continue
            task_parts=task_string.strip().split(".",1)
            if len(task_parts)==2:
                task_id=task_parts[0].strip()
                task_name=task_parts[1].strip()
                prioritized_task_list.append({
                    "task_id":task_id,"task_name":task_name
                })
        return prioritized_task_list
    
    #获取头部任务
    @staticmethod
    def get_top_tasks(vectorstore,query:str,k:int)->List[Dict]:
        """
        Get the top k tasks based on the query.
        """
        #根据query查找与查询最相似的k个任务
        results=vectorstore.similarity_search_with_score(query,k)
        #如果查询结果为空即没有找到任何匹配的任务，则返回一个空列表
        if not results:
            return []
        """
        这里的lambda是python中的匿名函数，用于定义一个简单的函数
        lambda x:x[1]的作用是：
        1.定义一个匿名函数，接受一个参数x
        2.返回x[1],即x的第二个元素

        这里用于sorted()的key参数，指定排序的依据是按照results中每个元组的第二个元素
        比如：
        [
            (task1, 0.9),
            (task2, 0.7),
            (task3, 0.95)
        ]
        排序后的结果为：
        [
            (task3, 0.95),  # 相似度分数最高
            (task1, 0.9),
            (task2, 0.7)    # 相似度分数最低
        ]
        """
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
        return [str(item[0].metadata["task"]) for item in sorted_results]
    
    #执行任务
    @staticmethod
    def execute_task(
        vectorstore,execution_chain,objective:str,task:str,k:int=5
    )->str:
        """
        Execute a task.
        1.通过任务目标找到之前最相关的k个已完成的任务
        2.将这k个已完成的任务作为上下文提供给大模型执行新的下一个任务
        """
        context=TaskManage.get_top_tasks(vectorstore=vectorstore,query=objective,k=k) 
        return execution_chain.invoke(
            {
                "objective":objective, 
                "context":context, 
                "task":task
            }
        )