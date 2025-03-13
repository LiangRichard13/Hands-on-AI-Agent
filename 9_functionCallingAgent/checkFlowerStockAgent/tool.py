import json

def get_flower_inventory(city):
    #获取指定地点的鲜花库存
    if "北京" in city:
        return json.dumps({"city":"北京","inventory":"玫瑰:100,郁金香:150"})
    elif "上海" in city:
        return json.dumps({"city":"北京","inventory":"百合:80,康乃馨:120"})
    elif "深圳" in city:
        return json.dumps({"city":"北京","inventory":"向日葵:200,玉兰:90"})
    else:
        return json.dumps({"city":"city","inventory":"未知"})
    
#定义工具列表 即函数的 元数据
tools=[
{
"type":"function",
"function":{
    "name":"get_flower_inventory",
    "description":"获取指定城市的鲜花库存",
    "parameters":{
        "type":"object",
        "properties":{
            "city":{
                "type":"string",
                "description":"城市名称，如北京、上海或深圳"
            }
        },
    "required":["city"]
    }
}
}
]
