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
from functions.remove_file import *

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
        schema_remove_file
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
    

    # Build argv list without the --verbose flag so positional prompt detection works
    argv_args = [a for a in sys.argv[1:] if a != "--verbose"]
    if "--verbose" in sys.argv:
        verbose_flag = True

    # conversation history is kept in messages so the agent has context across prompts
    messages = []

    def handle_conversation_rounds(messages_list, verbose: bool):
        """Run the agent's internal loop (function-calls -> tool results -> final text)

        Appends intermediate contents/tool results to messages_list and prints the
        final text response when the model stops with no function calls.
        """
        MAX_ITERS = 20
        for _ in range(MAX_ITERS):
            response = client.models.generate_content(
                model=model,
                contents=messages_list,
                config=config,
            )

            if verbose:
                try:
                    last_text = messages_list[-1].parts[0].text
                except Exception:
                    last_text = "<unknown>"
                print(f"User prompt: {last_text}")
                print(response.text)
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print("Response tokens:", response.usage_metadata.candidates_token_count)

            if response.candidates:
                for candidate in response.candidates:
                    if candidate is None or candidate.content is None:
                        continue
                    messages_list.append(candidate.content)

            if response.function_calls:
                for part in response.function_calls:
                    result = call_function(part, verbose)
                    messages_list.append(result)
                # Continue the loop so the model can consume the tool results
                continue
            else:
                # Final text answer from the model
                print(response.text)
                return

    # If a prompt was provided on the command line, use it as the first message
    if len(argv_args) >= 1:
        # Join remaining argv parts so multi-word prompts work without extra quoting
        initial_prompt = " ".join(argv_args)
        messages.append(types.Content(role="user", parts=[types.Part(text=initial_prompt)]))
        handle_conversation_rounds(messages, verbose_flag)

    # Enter interactive REPL so the user can continue asking until they quit
    while True:
        try:
            user_input = input("\nEnter prompt (or type 'quit' to exit): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not user_input:
            # ignore empty input
            continue

        if user_input.lower() in ("quit", "exit"):
            print("Goodbye.")
            break

        messages.append(types.Content(role="user", parts=[types.Part(text=user_input)]))
        handle_conversation_rounds(messages, verbose_flag)


if __name__ == "__main__":
    main()

