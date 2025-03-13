# Function Calling
### 什么是Function Calling?
Function Calling是openai提供的功能，这个功能允许开发者用JSON Schema描述函数，大模型可以智能地输出一个包含用于调用一个或多个函数的**参数**的JSON对象

调用的步骤如下：
1. 定义好要做的事情的函数和元数据（JSON Schema），把JSON Schema交给大模型
2. 用户提出请求，如“获取当前天气”或“发送电子邮件给客户”
3. 大模型根据查询确定是否需要调用函数并构造一个字符串化的JSON对象。这个JSON对象包含函数调用的所需参数
4. 开发者将这个字符串解析回JSON对象，并实际调用相应的函数，如get_current_weath或sand_email
5. 函数执行并返回结果，这些结果被传递回大模型
6. 大模型接收函数执行的结果，并将相关信息整合到回复中，以自然语言的形式返回给用户

### Function定义示例
| 使用场景       | Function 定义的示例                          | 功能描述                           |
| -------------- | -------------------------------------------- | ---------------------------------- |
| 查询客户信息   | `get_customers(min_revenue: int, created_before: string, limit: int)` | 根据收入、创建日期等条件查询客户信息 |
| 提取数据       | `extract_data(name: string, birthday: string)`  | 从文本中提取特定的人名和生日数据   |
| 执行 SQL 查询  | `sql_query(query: string)`                     | 执行一个 SQL 查询并返回结果         |

### 在Playground中定义Function

1. 添加用于描述Function的Json Schema

```json
{
  "name": "get_encouragement",
  "description": "Returns a personalized encouragement message based on the user's name and mood",
  "strict": true,
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
    "additionalProperties": false
  }
}
```

2. 运行assistant

![image-20250312135258012](./../../../markDownNotes/markdownPics/image-20250312135258012.png)

此时assistant并没有生成鼓励的话语，而是一行合规的函数调用代码