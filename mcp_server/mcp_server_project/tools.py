import os


def add_tool(params):
    """Add two numbers."""

    return params.get("a", 0) + params.get("b", 0)


def file_reader_tool(params):
    """Read a file path and return its content."""

    file_path = params.get("file_path", "")

    if not file_path or not os.path.exists(file_path):
        return f"File Path {file_path} does not exist"

    with open(file_path, "r") as f:
        return f.read()


def sytem_info_tool(parasms):

    return {"cwd": os.getcwd(), "files": os.listdir(".")}


Tools = {
    "add_tool": add_tool,
    "file_reader_tool": file_reader_tool,
    "system_info_tool": sytem_info_tool
}
