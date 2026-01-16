import json
import os
import sys

def parse_env_lines(filepath):
    """
    Reads an .env file and yields lines.
    Returns a list of tuples (type, content) where type is 'COMMENT', 'EMPTY', or 'VAR'.
    'VAR' content is (key, value).
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line_stripped = line.strip()
            if not line_stripped:
                yield ('EMPTY', line)
            elif line_stripped.startswith('#'):
                yield ('COMMENT', line)
            else:
                # Basic parsing KEY=VAL
                if '=' in line:
                    key, value = line_stripped.split('=', 1)
                    yield ('VAR', (key.strip(), value.strip()))
                else:
                    # Treat lines without = as maybe parts of values or just text? 
                    # For safety, let's treat them as skipping or just plain lines if we were preserving exact structure, 
                    # but for this tool's purpose (making examples/converting), we care about keys.
                    # Let's assume valid property format or skip.
                    continue

def read_env_vars(filepath):
    """
    Returns a dict of key-values.
    """
    env_vars = {}
    for kind, content in parse_env_lines(filepath):
        if kind == 'VAR':
            k, v = content
            env_vars[k] = v
    return env_vars

def create_example(input_path, output_path, ignore_commented=False, ignore_empty=False, fill_with="XXXX"):
    lines = []
    
    # We parse line by line to preserve order and comments if needed
    p = parse_env_lines(input_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for kind, content in p:
            if kind == 'EMPTY':
                if not ignore_empty:
                    f.write(content)
            elif kind == 'COMMENT':
                if not ignore_commented:
                    f.write(content)
            elif kind == 'VAR':
                key, _ = content
                f.write(f"{key}={fill_with}\n")

def convert_env(input_path, output_path, format_type, indent=None, sort_keys=False, minify=False):
    data = read_env_vars(input_path)
    
    if sort_keys:
        data = dict(sorted(data.items()))
        
    mode = 'w'
    
    if format_type == 'json':
        with open(output_path, mode, encoding='utf-8') as f:
            if minify:
                json.dump(data, f, separators=(',', ':'))
            else:
                json.dump(data, f, indent=int(indent) if indent else 4)
                
    elif format_type == 'yaml':
        import yaml
        with open(output_path, mode, encoding='utf-8') as f:
            # indent in pyyaml is default 2 usually, but we can set it
            yaml.dump(data, f, default_flow_style=False, indent=int(indent) if indent else 2)
            
    elif format_type == 'toml':
        import tomli_w
        with open(output_path, 'wb') as f:
            tomli_w.dump(data, f)
