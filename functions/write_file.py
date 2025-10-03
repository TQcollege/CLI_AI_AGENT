import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates or overwrites a file with the content provided to the contents argument. Will create parent directories to the file if parent directories do not already exist in the file's file path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
	    "file_path": types.Schema(
		type=types.Type.STRING,
		description="The path of the file relative to the working_directory.",
	    ),
	    "content": types.Schema(
		type=types.Type.STRING,
		description="The content to be written to the file. Such as \"Hi, This text was written to the file via the write_file function",
	    ),
        },
    ),
)


def write_file(working_directory, file_path=".", content=""):
	base_path = os.path.abspath(working_directory)
	full_path = os.path.abspath(os.path.join(working_directory, file_path))
	if not full_path.startswith(base_path):
		return f'Error: Cannot write to "{full_path}" as it is outside the permitted working directory'
	parent_directory = os.path.dirname(full_path)
	if parent_directory:
		os.makedirs(parent_directory, exist_ok=True)

	try:
		with open(full_path, "w") as file:
			file.write(content)
		return f'Successfully wrote to "{full_path}" ({len(content) - 1} characters written)'

	except FileNotFoundError:
		return f'Error: Failed to write to "{full_path}", File not found'
	except Exception as e:
		return f'Error: {e}'
	
