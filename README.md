# CLI AI Agent

This is a CLI AI agent that can help you automate tasks by interacting with files and running Python scripts.

## Getting Started

To get started, your virtual environment must be activated by typing the command source .venv/bin/activate

You can being your interaction with the agent by typing "uv run main.py <text>" 
or by asking questions or giving commands within the REPL once the program is running.

The agent retains the context of the conversation for as long as the CLI program is running. Conversation context
is lost when the program is closed. 

The agent can perform CRUD operations on files within the "calculator" directory of this project much like
cursor or copilot. The agent can create entirely new projects and programs.

The agent has access to the following functions:

*   `get_files_info`: Lists files in a directory.
*   `get_file_contents`: Returns the contents of a file.
*   `run_python_file`: Runs a Python file.
*   `write_file`: Creates or overwrites a file.
*   `remove_file`: Removes a file.

To use these functions, simply describe what you want to do. For example:

*   "List all files in the current directory."
*   "Read the contents of the file 'my_file.txt'."
*   "Run the Python script 'my_script.py' with the arguments 'arg1' and 'arg2'."
*   "Write 'Hello, world!' to the file 'new_file.txt'."
*   "Remove the file 'old_file.txt'."

The agent will then use the appropriate function(s) to perform the task and provide you with the results.
