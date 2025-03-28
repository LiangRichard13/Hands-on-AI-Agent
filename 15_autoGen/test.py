def is_termination_msg(x):
    return x.get("content", "").rstrip().endswith("结束")

def process_message(message, termination_checker):
    if termination_checker(message):
        print("这是终止消息。")
    else:
        print("这不是终止消息。")

# 定义消息
message1 = {"content": "今天天气真好，结束"}
message2 = {"content": "今天天气真好"}

# 调用 process_message，传入 is_termination_msg 作为参数
process_message(message1, is_termination_msg)  # 输出: 这是终止消息。
process_message(message2, is_termination_msg)  # 输出: 这不是终止消息。