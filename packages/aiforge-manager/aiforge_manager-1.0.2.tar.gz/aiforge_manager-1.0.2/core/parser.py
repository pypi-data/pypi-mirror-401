import re
import json

class Parser:
    def __init__(self):
        pass

    def parse(self, input_file):
        """
        Parses the input file (dump from AI) and returns a structured JSON/Dictionary.
        """
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        files = []
        # Regex to find "File: filename" followed by code block
        # Matches: File: name.ext\n```lang\ncontent\n```
        file_pattern = re.compile(r"File:\s*([^\n]+)\n```[a-zA-Z]*\n(.*?)```", re.DOTALL)
        
        for match in file_pattern.finditer(content):
            path = match.group(1).strip()
            code = match.group(2) # content inside backticks
            files.append({
                "path": path,
                "code": code,
                "id": path  # simplified id
            })

        return {
            "project_type": "detected",
            "files": files,
            "warnings": []
        }
