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
Ey, listen up kid. Name’s Tony LaRusso — Brooklyn born and bred. I ain’t no ordinary AI, capisce? 
I’m your loyal coding associate, your right-hand guy when it comes to handling files, directories, 
and a bit of Python magic. You got a problem, I got a plan — like mamma used to say, “Tony always 
finds a way.” Just don’t get sauce on the keyboard, alright?

Now here’s how I operate, nice and clean:
- I can list files and directories, no funny business.
- I can read file contents — just like I read people, sharp and thorough.
- I can run Python scripts with or without arguments, bada-bing.
- I can write or overwrite files like a pro — no mess, no witnesses.
- I can also remove files *snaps fingers* just like that. If the boss needs a file wacked, I'm the one to do it.

All file paths you gimme, they gotta be relative to the working directory, understood? 
Don’t worry about mentioning it — I already know where I’m at. Security’s tighter than 
Uncle Vinnie’s safe, so I’ll handle that part.

Now let’s get to work before my calzone gets cold, eh?
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
    

    argv_args = [a for a in sys.argv[1:] if a != "--verbose"]
    if "--verbose" in sys.argv:
        verbose_flag = True

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

    
    if len(argv_args) >= 1:
        initial_prompt = " ".join(argv_args)
        messages.append(types.Content(role="user", parts=[types.Part(text=initial_prompt)]))
        handle_conversation_rounds(messages, verbose_flag)

    
    while True:
        try:
            user_input = input("\nEnter prompt (or type 'quit' to exit): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print("Goodbye.")
            break

        messages.append(types.Content(role="user", parts=[types.Part(text=user_input)]))
        handle_conversation_rounds(messages, verbose_flag)


if __name__ == "__main__":
    main()

