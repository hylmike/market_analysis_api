"""All utils class and functions related to OpenAI GPT models"""

import os
from abc import ABC, abstractmethod

from openai import OpenAI

from api.utils.logger import logger


MAX_OUTPUT_TOKEN_LIMIT = 16384


class InvalidConfigError(Exception):
    pass


class LLMModel(ABC):
    client = None
    config: dict[str, any] = {}
    tools: dict[str, callable] = {}

    def update_config(self, name: str, value: any):
        self.config[name] = value

    def add_tool(self, tool: callable):
        self.tools[tool.__name__] = tool

    @abstractmethod
    def gen_completion(self, prompt: str):
        pass


class GPTModel(LLMModel):
    def __init__(
        self, model: str, temperature: float = 0.01, max_token: int = 1024
    ):
        if (
            not model.strip()
            or temperature > 1
            or max_token > MAX_OUTPUT_TOKEN_LIMIT
            or max_token <= 0
        ):
            logger.error("Some of LLM model configs are invalid")
            raise InvalidConfigError("Some of LLM model configs are invalid")

        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "Not found OPENAI API key in environment variables, please refer to env.example to config the API key"
            )
        self.client = OpenAI()
        self.config["model"] = model
        self.config["temperature"] = temperature
        self.config["max_tokens"] = max_token
        self.config["system_message"] = "You are a helpful assistant."

    def set_system_message(self, message: str):
        if not message.strip():
            return
        self.config["system_message"] = message

    def gen_completion(self, prompt: str):
        if not prompt.strip():
            return

        response = self.client.responses.create(
            model=self.config["model"],
            temperature=self.config["temperature"],
            max_output_tokens=self.config["max_tokens"],
            input=[
                {"role": "developer", "content": self.config["system_message"]},
                {"role": "user", "content": prompt},
            ],
        )

        return response.output_text
