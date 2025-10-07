import os
from google.genai import types

schema_remove_file = types.FunctionDeclaration(
    name="remove_file",
    description="removes a file and its contents from a directory.",
	parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file relative to the working_directory.",
            ),
        },
    ),
)


def remove_file(working_directory, file_path="."):
        base_path = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not full_path.startswith(base_path):
                return f'Error: Cannot remove "{full_path}" as it is outside the permitted working directory'
        parent_directory = os.path.dirname(full_path)
        if parent_directory:
                os.makedirs(parent_directory, exist_ok=True)

        try:
                os.remove(full_path)
                return f'Successfully removed {file_path} and its contents.'

        except FileNotFoundError:
                return f'Error: Failed to remove "{file_path}", File not found'
        except Exception as e:
                return f'Error: {e}'
