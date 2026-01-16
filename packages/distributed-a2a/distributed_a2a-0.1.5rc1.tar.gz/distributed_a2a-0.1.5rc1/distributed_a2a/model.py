from typing import List

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from pydantic import BaseModel


class SkillConfig(BaseModel):
    id: str
    name: str
    description: str
    tags: List[str]


class LLMConfig(BaseModel):
    base_url: str
    model: str
    api_key_env: str
    reasoning_effort: str
    system_prompt: str


class CardConfig(BaseModel):
    name: str
    version: str
    default_input_modes: List[str]
    default_output_modes: List[str]
    preferred_transport_protocol: str
    url: str
    description: str
    skills: List[SkillConfig]


class AgentItem(BaseModel):
    card: CardConfig
    llm: LLMConfig


class AgentConfig(BaseModel):
    agent: AgentItem



def get_model(api_key: str, model: str, base_url: str, reasoning_effort: str) -> BaseChatModel:
    return ChatOpenAI(
        model=model,
        base_url=base_url,
        api_key=lambda: api_key,
        reasoning_effort=reasoning_effort
    )
