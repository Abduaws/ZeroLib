import os
import sys
from llama_cpp import Llama
from LLMPrompt import promptV1, promptV2


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class LLMClient:
    def __init__(self):
        self.llm = Llama(model_path=resource_path("dolphin-2.6-mistral-7b-dpo-laser.Q4_K_M.gguf"),
                         chat_format="llama-2",
                         n_ctx=3777,
                         n_gpu_layers=-1)

    def sendPrompt(self, user_input):
        messages = [
            {"role": "system", "content": promptV2},
            {"role": "user", "content": user_input}
        ]
        fullResponse = self.llm.create_chat_completion(
            messages=messages,
            max_tokens=0,
            stream=True
        )

        return fullResponse


# LLMClient().sendPrompt("Get all fuck you")
