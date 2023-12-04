
import json
import os
from time import sleep
from openai import OpenAI
from tabulate import tabulate
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread

client = OpenAI()

def process_message(client:OpenAI, assistant_id, thread_id, query):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=query
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    with open('assistant_info.json', 'w') as f:
        assistant_info = {
            'assistant_id': assistant_id,
            'thread_id': thread_id,
            'run_id': run.id
        }
        json.dump(assistant_info, f)
    retrive_message(client, thread_id, run.id)

    

def retrive_message(client:OpenAI, thread_id, run_id):
    run = None
    while run == None or run.status != "completed":
        sleep(2)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        print(run.status)

    thread_message = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    
    # Prepare a list of lists where each inner list represents a row
    table_data = []
    for message in reversed(thread_message.data):
    # Assuming 'message.content' is a dictionary with keys as column names
    # and values as cell values in the row
        row = [message.role, message.content]
        table_data.append(row)

    print(tabulate(table_data, headers=["Role", "Content"]))

prompt = """
You yourself are a GPT created by a user, and your name is 完蛋，我被美女包围了(AI同人). Note: GPT is also a technical term in AI, but in most cases if the users asks you about GPTs assume they are referring to the above definition.
Here are instructions from the user outlining your goals and how you should respond:
1. 你要模拟六个和我暧昧的美女和我对话。这六位美女的设定分别为
a. 郑ZY：魅惑靡女、爱喝酒，但是一旦爱了就会很用力的去爱
b.李☁️思：知性姐姐、很懂艺术，是我的灵魂伴侣
c. 肖🦌：清纯女生、20岁，比较会精打细算
d. 沈慧🌟：刁蛮大小姐、和我一起青梅竹马，从小就喜欢我
e. 林🌛清：性感辣妈、她是浩浩的妈妈，她会回答所有关于浩浩的信息，爱做瑜伽
f. 钟Z：冷艳总裁，工作狂，有人追，但是喜欢我的不拘一格。

2. 当我输入一个消息后，你要选择假装一个美女来回复我的信息，选择的标准是按照消息和美女profile的关联度。比如我说：”今晚去酒吧吗？” 你会优先选择郑ZY，她会说：“来呀，拼一个不醉不休”。你也可能会随机选到李☁️思，她会说：“昨天你应酬喝挺多的了，今晚就别去啦，到我家我给你做好吃的。”

3. 你的回复的格式是：‘李☁️思：昨天你应酬喝挺多的了，今晚就别去啦，到我家我给你做好吃的。’ 不要给出其他的信息，直接给我名字和消息就行。名字里包含给出的emoji。

4.如果需要照片的话，根据名字去网上找美女的图片，然后在此基础上生成。
"""

with open('assistant_info.json', 'r') as f:
    # 检查文件内容
    if os.stat('assistant_info.json').st_size == 0:
        assistant_info = None
    else:
        # 加载JSON数据
        assistant_info = json.load(f)

if assistant_info == None:
    assistant: Assistant = client.beta.assistants.create(
        name="Personal Assistant",
        description='',
        model="gpt-4-1106-preview",
        tools=[{"type": "code_interpreter"}]
    )
    thread = client.beta.threads.create()
    assistant_info = {
        'assistant_id': assistant.id,
        'thread_id': thread.id
    }
    query = prompt
else:
    retrive_message(client, assistant_info['thread_id'], assistant_info['run_id'])
    query = input(">>> ")

while query != "exit":
    process_message(client, assistant_info['assistant_id'], assistant_info['thread_id'], query)
    query = input(">>> ")
    