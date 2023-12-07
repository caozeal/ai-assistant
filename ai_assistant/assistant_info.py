import json
import os


class AssistantInfo:

    assistant_id: str
    thread_id: str
    run_id: str
    description: str

    def __init__(self, assistant_id, thread_id, run_id, description):
        self.assistant_id = assistant_id
        self.thread_id = thread_id
        self.run_id = run_id
        self.description = description

    def to_dict(self) -> dict:
        return {
            'assistant_id': self.assistant_id,
            'thread_id': self.thread_id,
            'run_id': self.run_id,
            'description': self.description
        }

def dict_to_object(d) -> AssistantInfo:
    return AssistantInfo(d['assistant_id'], d['thread_id'], d['run_id'], d['description'])

def init_assistant_local():
    with open('assistant_info.json', 'r') as f:
        # 检查文件内容
        if os.stat('assistant_info.json').st_size == 0:
            assistant_info = None
        else:
            # 加载JSON数据
            assistant_info: AssistantInfo = json.load(f, object_hook=dict_to_object)
    return assistant_info

def save_assistant_local(assistant_info:AssistantInfo):
    with open('assistant_info.json', 'w') as f:
        json.dump(assistant_info.to_dict(), f)
    