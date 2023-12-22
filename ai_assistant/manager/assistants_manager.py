from time import sleep
from openai import OpenAI
from openai.pagination import SyncCursorPage
from openai.types.beta.threads.thread_message import ThreadMessage
from assistant_info import AssistantInfo
import assistant_info as as_info


def process_message(client:OpenAI, assistant_info:AssistantInfo, query) -> SyncCursorPage[ThreadMessage]:
    client.beta.threads.messages.create(
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
    return retrive_message(client, assistant_info)

    

def retrive_message(client:OpenAI, assistant_info:AssistantInfo) -> SyncCursorPage[ThreadMessage]:
    run = None
    while run == None or run.status != "completed":
        sleep(2)
        run = client.beta.threads.runs.retrieve(
            thread_id=assistant_info.thread_id,
            run_id=assistant_info.run_id
        )
        print(run.status)
        if run.status == "expired":
            return process_message(client, assistant_info, "继续")

    return client.beta.threads.messages.list(
        thread_id=assistant_info.thread_id
    )