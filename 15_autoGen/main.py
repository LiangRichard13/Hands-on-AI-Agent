#禁用缓存
import os
os.environ["AUTOGEN_USE_CACHE"] = "false"

# 导入autoGen包
import autogen

#导入配置信息
#导入用户代理
from config import (
    user_proxy_auto,
    user_proxy
)
#导入助手角色
from config import (
    inventory_assistant,
    market_research_assistant,
    content_creator
)
#导入任务
from config import (
    inventory_tasks,
    market_research_tasks,
    content_creation_tasks
)

#发起对话
chat_results=autogen.initiate_chats(
    [
        {
            "sender":user_proxy_auto,
            "recipient":inventory_assistant,
            "message":inventory_tasks[0],
            "clear_history":True,
            "silent":False,
            "summary_method":"last_msg"
        },
        {
            "sender":user_proxy_auto,
            "recipient":market_research_assistant,
            "message":market_research_tasks[0],
            "max_turns":2,
            "summary_method":"reflection_with_llm"
        },
        {
            "sender":user_proxy,
            "recipient":content_creator,
            "message":content_creation_tasks[0],
            "carryover":"我希望在博客文章中包含一张数据表格或图"
        }
    ]
)
