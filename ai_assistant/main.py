
import json
import os
from time import sleep
from openai import OpenAI
from tabulate import tabulate
from openai.types.beta.assistant import Assistant

from assistant_info import AssistantInfo
import manager.assistants_manager as as_manager
import assistant_info as as_info
import utils.ui_util as ui_util

client = OpenAI()

assistant_infos: list[AssistantInfo] = as_info.init_assistant_local()

index = ui_util.choose_assistants(assistant_infos)

if index == "add":
    assistant: Assistant = client.beta.assistants.create(
        name="Personal Assistant",
        description='你是一名新人视频up主，一切重新开始，你的目标是成为一名大神级的up主，你将实现这个目标。',
        model="gpt-4-1106-preview"
        # tools=[{"type": "code_interpreter"}]
    )
    thread = client.beta.threads.create()
    assistant_info: AssistantInfo = AssistantInfo(assistant.id, thread.id, None, assistant.description)
    as_info.save_assistant_local(assistant_info)
    query = assistant.description
else:
    assistant_info = assistant_infos[int(index)]
    messages = as_manager.retrive_message(client, assistant_info)
    ui_util.print_message(messages)
    query = input(">>> ")

while query != "exit":
    messages = as_manager.process_message(client, assistant_info, query)
    ui_util.print_message(messages)
    query = input(">>> ")
    