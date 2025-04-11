from ollama import chat, ChatResponse
from prompter import PromptBuilder

CONTEXT_DIR = "../pdi-txt"
msg = PromptBuilder(f"{CONTEXT_DIR}/pdi-fpso-p-32.txt").make_prompt()

response: ChatResponse = chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": msg,
        },
    ],
)
print(response.message.content)
