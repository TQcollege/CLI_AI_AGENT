import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types
from functions.get_files_info import *
from functions.get_file_contents import *
from functions.run_python_file import *
from functions.write_file import *
from functions.call_function import *

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_contents,
        schema_run_python_file,
        schema_write_file,
        # schema_call_function
    ]
)

config = types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model = "gemini-2.0-flash-001"


def main():
    verbose_flag = False
    prompt = None
    if len(sys.argv) >= 2:
        prompt = sys.argv[1]
        if "--verbose" in sys.argv:
            verbose_flag = True
    else:
        print("No prompt given")
        sys.exit(1)

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    MAX_ITERS = 20
    for i in range(0, MAX_ITERS):

        response = client.models.generate_content(
            model=model,
            contents=messages,
            config=config,
        )

        if verbose_flag is True:
            print(f"User prompt: {prompt}")
            print(response.text)
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                # Append the candidate's content instead of undefined result
                messages.append(candidate.content)

        if response.function_calls:
            for part in response.function_calls:
                result = call_function(part, verbose_flag)
                messages.append(result)
        else:
            print(response.text)
            return


if __name__ == "__main__":
    main()

