import os
def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        return_str = ""
        working_directory_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))
        # Checks if the target directory is within the abspath (Will be True or False)
        if not os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs:
            return_str = f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
            return f"Result for '{directory}' directory:\n{return_str}"
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        #return f'Success: "{directory}" is within the working directory'
        file_list = os.listdir(target_dir)
        data: list[str] = []
        for file in file_list:
            data.append(f"  - {file}: file_size={os.path.getsize(target_dir + f"/{file}")} bytes, is_dir={os.path.isdir(target_dir + f"/{file}")}")
        return_str = "\n".join(data)
        if directory == ".":
            return f"Result for current directory:\n{return_str}"
        else:
            return f"Result for '{directory}' directory:\n{return_str}"
    except Exception as e:
        return f'Error: {e}'

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
