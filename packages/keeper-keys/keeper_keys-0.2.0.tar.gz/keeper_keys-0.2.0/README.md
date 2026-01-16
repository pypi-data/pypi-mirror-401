[![PyPI - Version](https://img.shields.io/pypi/v/keeper-keys.svg)](https://pypi.org/project/keeper-keys)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/keeper-keys.svg)](https://pypi.org/project/keeper-keys)

# KEYS: Keeper, Exports Your Secrets

**DISCLAIMER: This project is a private open source project and doesn't have any connection with Keeper Security.**

A straightforward CLI wrapper for [Keeper Commander](https://docs.keeper.io/en/keeperpam/commander-cli/overview) that simplifies extracting secrets to setup environment variables.

`keeper find-password` does the same thing, except it doesn't handle SSO automatically and needs the `--field` parameter to work with _API_ records.

## Usage

![](demo/keys.gif)

```bash
# Set environment variable from a Keeper record
export OPENAI_API_KEY="$(keys 'OpenAI')"

# Specify a custom field
export SECRET="$(keys 'My secert record' --field 'password2')"

# Insert a new login secret
keys --insert OpenAI

# Insert a new login secret in a folder (however, the folder MUST exists)
keys --insert "Tools/OpenAI"
```

## Installation

```bash
uv tool install .
```

**Note**: requires Keeper Commander to be installed and configured.

## Default field by record type

The `--field` argument defaults to `password` for _Login_ and _Secure Note_ records and to `API Key` for _API_ records.

## SSO login

If SSO login is required, KEYS will automatically open the SSO login URL in your browser and wait till you paste the obtained login token in the terminal.

## Donate

Donations via [Liberapay](https://liberapay.com/ilpianista) or Bitcoin (1Ph3hFEoQaD4PK6MhL3kBNNh9FZFBfisEH) are always welcomed, _thank you_!

## License

MIT
