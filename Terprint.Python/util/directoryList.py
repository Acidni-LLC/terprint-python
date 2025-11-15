import re
from pathlib import Path

def list_files(directory, pattern=None):
    """
    Lists all files in the specified directory and returns them as a list of strings.
    Optionally filters files that match the specified regular expression pattern in their name.
    
    Args:
        directory (str): The path to the directory.
        pattern (str, optional): A regular expression pattern to filter files by. If provided, only files
                                 whose names match this regex will be included.
    
    Returns:
        list: A list of file names (as strings) in the directory, filtered by pattern if provided.
    """
    path = Path(directory)
    if not path.is_dir():
        raise ValueError(f"{directory} is not a valid directory")
    files = [str(f.name) for f in path.iterdir() if f.is_file()]
    if pattern:
        files = [f for f in files if re.search(pattern, f)]
    return files

print(list_files(
    r'C:\Users\JamiesonGill\source\repos\Acidni-LLC\Terprint\Terprint.Python\files\test_output', 
    r'^\d{5}_\d{10}\.pdf$'))