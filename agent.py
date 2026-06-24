import os
import json
from groq import Groq
from dotenv import load_dotenv
from github_fetch import get_pr_diff
from tools import run_flake8, run_pylint

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "run_flake8",
            "description": "Run flake8 style checker on Python code.",
            "parameters": {
                "type": "object",
                "properties": {"code": {"type": "string"}},
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_pylint",
            "description": "Run pylint quality checker on Python code.",
            "parameters": {
                "type": "object",
                "properties": {"code": {"type": "string"}},
                "required": ["code"]
            }
        }
    }
]

available_functions = {"run_flake8": run_flake8, "run_pylint": run_pylint}

def run_agent(pr_url):
    diff_text = get_pr_diff(pr_url)
    messages = [
        {"role": "system", "content": "You are an expert code reviewer. Use the tools to check code quality before giving your final review."},
        {"role": "user", "content": f"Review this PR diff:\n\n{diff_text}"}
    ]

    for step in range(5):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        message = response.choices[0].message

        assistant_msg = {"role": "assistant", "content": message.content}
        if message.tool_calls:
            assistant_msg["tool_calls"] = [
                {"id": tc.id, "type": "function",
                 "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in message.tool_calls
            ]
        messages.append(assistant_msg)

        if not message.tool_calls:
            return message.content

        for tool_call in message.tool_calls:
            func = available_functions[tool_call.function.name]
            args = json.loads(tool_call.function.arguments)
            result = func(**args)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.function.name,
                "content": result
            })

    return "Agent stopped after max steps."

if __name__ == "__main__":
    url = input("Paste a GitHub PR URL: ")
    print("\n=== AI CODE REVIEW ===\n")
    print(run_agent(url))