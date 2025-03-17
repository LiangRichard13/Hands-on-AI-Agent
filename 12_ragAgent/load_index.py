from llama_index.core import StorageContext,load_index_from_storage

#从持久化的数据中读取向量数据
try:
    storage_context=StorageContext.from_defaults(
        persist_dir="./news_embeddings_storage"
    )

    index=load_index_from_storage(storage_context=storage_context)
    index_loaded=True
except:
    index_loaded=False

#创建查询引擎
engine=index.as_query_engine(similarity_top_k=5)
#配置查询工具
from llama_index.core.tools import QueryEngineTool,ToolMetadata

query_engine_tool=QueryEngineTool(
    query_engine=engine,
    metadata=ToolMetadata(
        name="news_rag",
        description="用于提供上个世纪中国主流报刊新闻信息"
    )
)
