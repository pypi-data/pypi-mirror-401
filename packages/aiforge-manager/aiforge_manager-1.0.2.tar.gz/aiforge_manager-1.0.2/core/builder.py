import os
import shutil

class Builder:
    def __init__(self):
        pass

    def build(self, project_data, output_dir, mode='clean'):
        """
        Builds the project structure on disk based on the parsed data.
        """
        print(f"Building project in {output_dir} with mode {mode}")
        if mode == 'clean' and os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        
        os.makedirs(output_dir, exist_ok=True)
        
        for file_data in project_data.get("files", []):
            path = file_data["path"]
            content = file_data["code"]
            
            # Handle subdirectories in file path
            full_path = os.path.join(output_dir, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"  Created {path}")
