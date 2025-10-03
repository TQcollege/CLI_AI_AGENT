import os
from google.genai import types
from .config import MAX_CHARS

schema_get_file_contents = types.FunctionDeclaration(
    name="get_file_contents",
    description="Returns the contents of a file up to 10000 characters. If a file contains more than 10000 characters it is truncated.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative to the working directory. This is the file to read the contents of.",
            ),
        },
    ),
)




def get_file_contents(working_directory, file_path):
	contents = None
	base_path = os.path.abspath(working_directory)
	full_path = os.path.abspath(os.path.join(working_directory, file_path))
	if not full_path.startswith(base_path):
		return f'Error: Cannot read "{full_path} as it is outside the permitted working directory'
	if not os.path.isfile(full_path):
		return f'Error: File not found or is not a regular file: "{full_path}"'
	
	try:
		with open(full_path,"r") as file:
			contents = file.read(MAX_CHARS + 1)
			if len(contents) > MAX_CHARS:
				contents += f'"{full_path}" truncated at {MAX_CHARS} characters'

	except FileNotFoundError:
		return f'Error: File not found or is not a regular file: "{full_path}"'
	return contents
