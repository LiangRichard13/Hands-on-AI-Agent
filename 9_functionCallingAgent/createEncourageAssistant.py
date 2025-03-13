# from getEncouragement import get_encouragement
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
#实例化client
client=OpenAI()

'''
刚刚创建的encourageAssistant
ID:asst_m7r3SjFoJ7a4s5OcL1WtzgVX
'''

assistant_id="asst_m7r3SjFoJ7a4s5OcL1WtzgVX"
#通过assistant_id获取到刚刚创建的assistant对象
assistant=client.beta.assistants.retrieve(assistant_id=assistant_id)
print("Encourage Assistant",assistant)


#如果要创建新的assistant
def create_encourage_assistant(function_description):
    assistant=client.beta.assistants.create(
        name='Encourage Assistant',
        instructions="You are a very encouraging assistant",
        model="gpt-4o",
        tools=[
            {"type":"function","function":function_description}
        ]
    )
    return assistant


function_description={
  "name": "get_encouragement",
  "description": "Returns a personalized encouragement message based on the user's name and mood",
  "strict": True,
  "parameters": {
    "type": "object",
    "required": [
      "name",
      "mood"
    ],
    "properties": {
      "name": {
        "type": "string",
        "description": "The name of the person to whom the encouragement is addressed"
      },
      "mood": {
        "type": "string",
        "description": "The current mood of the person which determines the type of encouragement message"
      }
    },
    "additionalProperties": False
  }
}


new_encourage_assistant=create_encourage_assistant(function_description=function_description)
print("New Encourage Assistant",new_encourage_assistant)
