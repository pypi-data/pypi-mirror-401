import argparse
import sys
import os
from .utils import create_example, convert_env

def main():
    parser = argparse.ArgumentParser(description="Create and manage .env files and conversions.")
    parser.add_argument("input", help="Input .env file")
    parser.add_argument("output", help="Output file")
    
    # Example maker flags
    parser.add_argument("--ignore-commented", action="store_true", help="Ignore lines that start with #")
    parser.add_argument("--ignore-empty", action="store_true", help="Ignore empty lines")
    parser.add_argument("--fill-with", default="XXXX", help="String to fill variables with in example file")
    
    # Conversion flags
    parser.add_argument("--indent", type=int, help="Indentation level for JSON/YAML")
    parser.add_argument("--sort", action="store_true", help="Sort keys")
    parser.add_argument("--minify", action="store_true", help="Minify JSON output")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        sys.exit(1)

    # Detect mode based on output extension
    if args.output.endswith('.json'):
        convert_env(args.input, args.output, 'json', indent=args.indent, sort_keys=args.sort, minify=args.minify)
    elif args.output.endswith('.yaml') or args.output.endswith('.yml'):
        convert_env(args.input, args.output, 'yaml', indent=args.indent, sort_keys=args.sort)
    elif args.output.endswith('.toml'):
        convert_env(args.input, args.output, 'toml', sort_keys=args.sort)
    else:
        # Default to example maker
        # We assume if it's not a known format, it's an env file
        create_example(
            args.input, 
            args.output, 
            ignore_commented=args.ignore_commented, 
            ignore_empty=args.ignore_empty, 
            fill_with=args.fill_with
        )

if __name__ == "__main__":
    main()
