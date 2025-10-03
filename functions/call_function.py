import os
from .config import WORKING_DIR
from google.genai import types
from .get_files_info import *
from .get_file_contents import *
from .run_python_file import *
from .write_file import *


def call_function(function_call_part, verbose=False):
	result = ""
	if function_call_part:
		for part in function_call_part:
			if verbose:
				print(f"Calling function: {function_call_part.name}({function_call_part.args})")
			print(f" - Calling function: {function_call_part.name}")
			if function_call_part.name == "get_files_info":
				result = get_files_info(WORKING_DIR, **function_call_part.args)
			elif function_call_part.name == "get_file_contents":
                                result =  get_file_contents(WORKING_DIR, **function_call_part.args)
			elif function_call_part.name == "write_file":
                                result = write_file(WORKING_DIR, **function_call_part.args)
			elif function_call_part.name == "run_python_file":
                                result = run_python_file(WORKING_DIR, **function_call_part.args)
			else:
				return types.Content(
					role="tool",
    					parts=[
        				types.Part.from_function_response(
            				name=function_call_part.name,
            				response={"error": f"Unknown function: {function_call_part.name}"},
        			    )
    			      ],
			)
			
			return types.Content(
				role="tool",
    				parts=[
        			    types.Part.from_function_response(
            				name=function_call_part.name,
            				response={"result": result},
        			    )
    			      ],
			)

