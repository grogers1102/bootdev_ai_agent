import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if(api_key == None):
    raise RuntimeError("API Key wasn't found")

client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = api_key,
)
# Expect user prompt on command line
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]
response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions,
    temperature=0,
)
def main():
    if response.usage == None:
        raise RuntimeError("Error: The response's usage property wasn't created")
    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    message = response.choices[0].message
    print(f"Response: \n{message.content}")
    if message.tool_calls != None:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            #print(f"Calling function: {tool_call.function.name}({function_args})")
            result_message = call_function(tool_call, args.verbose)
            if result_message["content"] == None:
                raise Exception(f"Error: Content was empty in the tool message")
            if args.verbose == True:
               print(f"-> {result_message['content']}") 


if __name__ == "__main__":
    main()
