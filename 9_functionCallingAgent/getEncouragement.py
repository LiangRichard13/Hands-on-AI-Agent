'''
get_encouragement接收两个参数，用户的名字和心情，
根据用户的心情，从预设的消息中选择一句合适的鼓励语并返回
'''

def get_encouragement(name,mood):
    #基础鼓励消息
    messages={
        "开心":"看到你这么阳光真好！保持这份积极！",
        "伤心":"记得，每片乌云背后都有阳光。",
        "疲倦":"你做得足够好，现在是时候休息一下了。",
        "压力大":"深呼吸，慢慢呼出，一切都会好起来。"
    }

    #获取对应心情的鼓励消息
    if name:
        message=f"亲爱的{name}，"+messages.get(mood.lower(),"你今天感觉如何？我总是在这里支持你！")
    else:
         message=messages.get(mood.lower(),"你今天感觉如何？我总是在这里支持你！")
    #返回定制化的鼓励消息
    return message