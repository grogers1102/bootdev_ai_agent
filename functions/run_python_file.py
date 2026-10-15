import os
import subprocess
def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        if not os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        command: list[str] = ["python", target_file]
        if args != None:
            command.extend(args)
        completed_process = subprocess.run(command, capture_output=True, timeout=30, text=True)
        output: str = ""
        if completed_process.returncode != 0:
            output += f"Process exited with code {completed_process.returncode}\n"
        if completed_process.stdout == None and completed_process.stderr == None:
            output += "No output produced"
        else:
            output += f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e} at {e.__traceback__.tb_lineno}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs the script within a specified python file (with any relevant arguments provided) relative to the working directory, providing the stdout and stderr produced from the file run",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to run the python script from, relative to the working directory",
                },
                "args": {
                    "type": ["array", "null"],
                    "description": "List of arguments that are provided for the script to run, or null if no arguments are needed",
                    "items": {
                        "type": "string"
                    },
                },
            },
        },
    },
}