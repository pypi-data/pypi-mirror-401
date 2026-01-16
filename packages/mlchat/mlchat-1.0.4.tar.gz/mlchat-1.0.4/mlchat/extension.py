from datetime import datetime
from typing import Literal, overload
from openai import AsyncOpenAI
from pydantic import BaseModel, field_validator, Field
from openai.types.chat.chat_completion_chunk import ChoiceDeltaToolCall
from mcp import Tool as _Tool
import json


class TextContent(BaseModel):
    type:str = 'text'
    text:str
    
    def __init__(self, text:str):
        super().__init__(text=text)
    
class ImageUrl(BaseModel):
    url: str = Field(..., description='Either a URL of the image or the base64 encoded image data.')
    detail: Literal["auto", "low", "high"] = 'auto'
    
class ImageContent(BaseModel):
    type:str = 'image_url'
    image_url:ImageUrl
    
    def __init__(self, image_url:ImageUrl|dict|str):
        super().__init__(image_url=ImageUrl(url=image_url) if isinstance(image_url, str) else image_url)

class AudioUrl(BaseModel):
    data: str = Field(..., description='Base64 encoded audio data.')
    format: Literal["wav", "mp3"]
    
class AudioContent(BaseModel):
    type:str = 'input_audio'
    input_audio:AudioUrl
    
    @overload
    def __init__(self, input_audio:AudioUrl|dict):...
    @overload
    def __init__(self, input_audio:str, format: Literal["wav", "mp3"]):...
    
    def __init__(self, input_audio:AudioUrl|dict|str, format: Literal["wav", "mp3"]=None):
        super().__init__(input_audio=AudioContent(data=input_audio, format=format) if isinstance(input_audio, str) else input_audio)
    
class DialogueMessager(BaseModel):
    role: Literal['assistant', 'user']
    content: str|list[TextContent|ImageContent|AudioContent] = ''
    
    @field_validator('content', mode='before')
    def _strip(cls, value, data):
        if isinstance(value, str):
            value = value.strip()
        elif hasattr(value, 'text'):
            setattr(value, 'text', getattr(value, 'text').strip())
        return value

class Messager(DialogueMessager):
    role: Literal['developer', 'system', 'assistant', 'user', 'tool']
    chunk: str|None = None
    name: str|None = None
    args: dict|list|None = None
    tool_call_id: str|None = None
    tool_calls: list[ChoiceDeltaToolCall]|None = None
    is_finish:bool = True
    time:str = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    @property
    def is_tool(self)->bool:
        return self.role == 'tool'
    
    @property
    def is_assistant(self):
        return self.role == 'assistant'
    
    @property
    def is_user(self):
        return self.role == 'user'
    
    @property
    def is_dialogue(self):
        return bool(self.content and self.role in ('assistant','user'))
    
    @property
    def debug_log(self)->str:
        if self.role == 'assistant' and not self.content:
            log = '; '.join(f'{tool.function.name} {tool.function.arguments}'for tool in self.tool_calls)
        else:
            log = self.content.split('\n')
            if len(log)>1 or len(log[0])>100:
                log = log[0][:100]+'...'
            else:
                log = log[0]
        return f"{self.role}: {log}"
    
    @property
    def tool_call_arguments(self)->list[dict]:
        return [json.loads(tool_call.function.arguments) for tool_call in (self.tool_calls or ())]
    
    def to_messager(self)->dict:
        return self.model_dump(exclude_none=True, exclude={'chunk', 'is_finish', 'time'})
    
class ToolCeil(BaseModel):
    name: str
    description: str
    parameters: dict
    strict: bool|None = None
    
    def to_tool(self)->dict:
        return {
                "type": "function",
                "function": {
                    "name":  self.name,
                    "description": self.description,
                    "parameters": self.parameters,
                    'strict': self.strict
                    }
                }
    
    @staticmethod
    def from_mcp_tool(tool:_Tool, strict:bool=None)->'ToolCeil':
        return ToolCeil(name=tool.name, description=tool.description, parameters=tool.inputSchema, strict=strict)

def _get_chat_history_text(messagers:list[DialogueMessager])->str:
    return '\n'.join(f'{messager.role}: {messager.content}' for messager in messagers if messager.content)

async def _get_result(aclient:AsyncOpenAI, model:str, prompt:str)->dict:
    response = await aclient.chat.completions.create(model=model, 
                                                     messages=[{'role': 'user', 'content': prompt}],
                                                     stream=False)
    import json_repair
    return json_repair.loads(response.choices[0].message.content)

_trace_tp = '''### Task:
Suggest {trace_num} relevant follow-up questions or prompts that the user might naturally ask next in this conversation as a **user**, based on the chat history, to help continue or deepen the discussion.
### Guidelines:
- Write all follow-up questions from the user’s point of view, directed to the assistant.
- Make questions concise, clear, and directly related to the discussed topic(s).
- Only suggest follow-ups that make sense given the chat content and do not repeat what was already covered.
- If the conversation is very short or not specific, suggest more general (but relevant) follow-ups the user might ask.
- Use the conversation's primary language; default to English if multilingual.
- Response must be a JSON array of strings, no extra text or formatting.
### Output:
JSON format: {{ "follow_ups": ["Question 1?", "Question 2?", "Question 3?"] }}
### Chat History:
<chat_history>
{chat_history}
</chat_history>'''

async def aget_trace(aclient:AsyncOpenAI, model:str, messagers:list[DialogueMessager], trace_num:int=3)->list[str]:
    """获取根据历史对话生成追问"""
    result = await _get_result(aclient, model, _trace_tp.format(trace_num=trace_num, chat_history=_get_chat_history_text(messagers)))
    return result.get('follow_ups', [])

_title_tp ='''### Task:
Generate a concise, 3-5 word title with an emoji summarizing the chat history.
### Guidelines:
- The title should clearly represent the main theme or subject of the conversation.
- Use emojis that enhance understanding of the topic, but avoid quotation marks or special formatting.
- Write the title in the chat's primary language; default to English if multilingual.
- Prioritize accuracy over excessive creativity; keep it clear and simple.
- Your entire response must consist solely of the JSON object, without any introductory or concluding text.
- The output must be a single, raw JSON object, without any markdown code fences or other encapsulating text.
- Ensure no conversational text, affirmations, or explanations precede or follow the raw JSON output, as this will cause direct parsing failure.
### Output:
JSON format: {{ "title": "your concise title here" }}
### Examples:
- { "title": "📉 Stock Market Trends" },
- { "title": "🍪 Perfect Chocolate Chip Recipe" },
- { "title": "Evolution of Music Streaming" },
- { "title": "Remote Work Productivity Tips" },
- { "title": "Artificial Intelligence in Healthcare" },
- { "title": "🎮 Video Game Development Insights" }
### Chat History:
<chat_history>
{chat_history}
</chat_history>'''

async def aget_title(aclient:AsyncOpenAI, model:str, messagers:list[DialogueMessager])->str:
    """获取根据历史对话生成总结性的标题"""
    result = await _get_result(aclient, model, _title_tp.format(chat_history=_get_chat_history_text(messagers)))
    return result.get('title', '')
