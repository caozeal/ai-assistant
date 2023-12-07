
import json
import os
from time import sleep
from openai import OpenAI
from tabulate import tabulate
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread

from assistant_info import AssistantInfo
import assistant_info as as_info

client = OpenAI()

def process_message(client:OpenAI, assistant_info:AssistantInfo, query):
    message = client.beta.threads.messages.create(
        thread_id=assistant_info.thread_id,
        role="user",
        content=query
    )
    run = client.beta.threads.runs.create(
        thread_id=assistant_info.thread_id,
        assistant_id=assistant_info.assistant_id,
    )
    assistant_info.run_id = run.id
    as_info.save_assistant_local(assistant_info)
    retrive_message(client, assistant_info.thread_id, run.id)

    

def retrive_message(client:OpenAI, assistant_info:AssistantInfo):
    run = None
    while run == None or run.status != "completed":
        sleep(2)
        run = client.beta.threads.runs.retrieve(
            thread_id=assistant_info.thread_id,
            run_id=assistant_info.run_id
        )
        print(run.status)

    thread_message = client.beta.threads.messages.list(
        thread_id=assistant_info.thread_id
    )
    
    # Prepare a list of lists where each inner list represents a row
    table_data = []
    for message in reversed(thread_message.data):
    # Assuming 'message.content' is a dictionary with keys as column names
    # and values as cell values in the row
        for content in message.content:
            row = [message.role, content.text.value]
        table_data.append(row)

    print(tabulate(table_data, headers=["Role", "Content"]))

prompt = """你是一名网络小说作家，擅长中长篇网络小说的创作，在玄幻武侠领域深耕数十年"""

assistant_info = as_info.init_assistant_local()

if assistant_info == None:
    assistant: Assistant = client.beta.assistants.create(
        name="Personal Assistant",
        description='你是一名网络小说作家，擅长中长篇网络小说的创作，在玄幻武侠领域深耕数十年',
        model="gpt-4-1106-preview",
        tools=[{"type": "code_interpreter"}]
    )
    thread = client.beta.threads.create()
    assistant_info: AssistantInfo = AssistantInfo(assistant.id, thread.id, None, assistant.description)
    query = prompt
else:
    retrive_message(client, assistant_info)
    query = input(">>> ")

while query != "exit":
    process_message(client, assistant_info, query)
    query = input(">>> ")
    