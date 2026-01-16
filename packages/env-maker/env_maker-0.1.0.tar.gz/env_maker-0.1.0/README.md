# env-maker

This python tool helps developers create and manage their development environments by offering different tools.

## Installation

```bash
pip install env-maker
```

## Usage and Tools

### `.env.example` maker

This tool helps you create a `.env.example` file from your `.env` file.

```bash
env-maker .env .env.example
```

Optional flags

- `--ignore-commented`: Ignore lines that start with a `#`.
- `--ignore-empty`: Ignore empty lines.
- `--fill-with <string>`: Fills the `.env` variables with a custom string, else it will use `XXXX`.

### Convertsion to JSON / TOML / YAML

This tool helps you convert your `.env` file to JSON / TOML / YAML.

```bash
env-maker .env .env.json
```

Optional flags
- `--indent`: Indent the JSON file.
- `--sort`: Sort the JSON file.

>[NOTE!]
> For JSON only: `--minify` flag to minify the JSON file.
