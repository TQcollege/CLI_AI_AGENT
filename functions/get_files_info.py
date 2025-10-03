import os
from google.genai import types

#Shema defines the function, defines the function arguments, and argument types for the model to call return a string that our agent can work with to call the function

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)



def get_files_info(working_directory, directory="."):
	try:
		base_path = os.path.abspath(working_directory)
		full_path = os.path.abspath(os.path.join(working_directory, directory))
		if not full_path.startswith(base_path):	
			return f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
		if not os.path.isdir(full_path):
			return f'    Error: "{directory}" is not a directory'
		with os.scandir(full_path) as entries:
			lines = []
			for entry in entries:
				lines.append(f'    - {entry.name}: file_size={os.path.getsize(entry.path)} bytes, is_dir={entry.is_dir()}')
			return "\n".join(lines)
	except Exception as e:
		return f"Error: {e}"
