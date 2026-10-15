import os

MAX_CHARACTERS = 10000
def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        if not os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_file, "r") as f:
            file_content = f.read(MAX_CHARACTERS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content += f'\n[...File "{file_path}" truncated at {MAX_CHARACTERS} characters]'
        return file_content
    except Exception as e:
        return f'Error: {e}'
schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the contents of a specified file relative to the working directory and detailing whether the contents of the file is greater in size than the max characters allowed to be read",
        "parameters": {
            "type": "object",
            "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "File path to read from, relative to the working directory",
                },
            },
        },
    },
}
    