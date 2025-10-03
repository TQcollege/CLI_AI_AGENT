import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file with the python3 interpreter. Accepts additional CLI args as an optional array",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
	    "file_path": types.Schema(
		type=types.Type.STRING,
		description="the file to run. file_path is relative to the working_directory",
	    ),
	    "args": types.Schema(
		type=types.Type.ARRAY,
		items=types.Schema(
			type=types.Type.STRING,
			description="An optional array of string arguments to pass to the python file",
            	    ),
		description="Optional arguments to pass to the python file",
	    ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
	base_path = os.path.abspath(working_directory)
	full_path = os.path.abspath(os.path.join(base_path, file_path))
	if not full_path.startswith(base_path):
		return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
	if not os.path.exists(full_path):
		return f'Error: File "{file_path}" not found.'
	if not full_path.endswith(".py"):
		return f'Error: "{file_path}" is not a python file.'
	try:
		cmd = ["python3",full_path]
		if args:
			cmd.extend(args)
	
		result = subprocess.run(
			cmd,
			capture_output=True,
			timeout=30,
			cwd=working_directory,
			text=True)
	
		output_parts = []

		if result.stdout:
			output_parts.append(f"STDOUT:\n{result.stdout}")
		if result.stderr:
			output_parts.append(f"STDERR:\n{result.stderr}")
		if result.returncode != 0:
			output_parts.append(f"Process exited with code {result.returncode}")
		if not output_parts:
			return "no output produced."

		return "\n".join(output_parts)

	except Exception as e:
		return f'Error: executing Python file: {e}'
	
