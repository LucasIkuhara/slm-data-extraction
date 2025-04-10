from ollama import chat, ChatResponse


response: ChatResponse = chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "Why is the sky blue?",
        },
    ],
)
print(response.message.content)
