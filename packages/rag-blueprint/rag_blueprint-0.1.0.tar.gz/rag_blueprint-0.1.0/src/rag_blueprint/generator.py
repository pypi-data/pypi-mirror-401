import os
import shutil
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = Path(__file__).parent / "templates"

def generate_project(project_name: str, template_name: str, output_dir: Path) -> None:
    """
    Generate a new project from a template.
    """
    template_path = TEMPLATE_DIR / template_name
    if not template_path.exists():
        raise ValueError(f"Template '{template_name}' not found.")

    output_path = output_dir / project_name
    if output_path.exists():
        raise FileExistsError(f"Directory '{project_name}' already exists.")

    # iterate over all files and render them
    env = Environment(loader=FileSystemLoader(template_path))
    
    # Context for rendering
    context = {
        "project_name": project_name,
        "project_slug": project_name.replace(" ", "_").replace("-", "_").lower(),
    }

    # Copy and render
    shutil.copytree(template_path, output_path)
    
    # Process files in the new directory
    for root, _, files in os.walk(output_path):
        for file in files:
            file_path = Path(root) / file
            
            # If it's a python file or md or toml, generic render might be safer 
            # or strictly .j2 extensions. 
            # For now, let's treat py, md, toml, txt as templates if they contain {{ }}
            # OR better, just rename .jinja files. 
            # Let's assume we copy everything, then render in-place if extension is .j2
            
            if file_path.suffix == ".j2":
                # Render
                rel_path = file_path.relative_to(output_path)
                # We need to get the template from the SOURCE, not the copy
                # actually jinja loader is set to template_path
                # But we are walking the OUTPUT path.
                
                # Let's map output path back to relative path
                # rel_path_str = str(rel_path).replace("\\", "/") # win compat
                # template = env.get_template(rel_path_str) 
                
                # Simpler approach: Read content, render string, write back, rename
                content = file_path.read_text(encoding="utf-8")
                template = env.from_string(content)
                rendered_content = template.render(**context)
                
                new_path = file_path.with_suffix("") # Remove .j2
                new_path.write_text(rendered_content, encoding="utf-8")
                file_path.unlink() # Remove .j2 file
