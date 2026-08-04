# tap-constrafor

`tap-constrafor` is a Singer tap for the [Constrafor](https://www.constrafor.com/) API.

## Installation

```bash
pipx install tap-constrafor
```

## Configuration

```bash
tap-constrafor --about
```

### Config options

| Setting | Required | Description |
|---------|----------|-------------|
| `api_key` | Yes | Constrafor API key (sent as `Authorization: Api-Key …`) |
| `start_date` | No | Earliest record date for incremental sync |

## Usage

```bash
tap-constrafor --version
tap-constrafor --help
tap-constrafor --config CONFIG --discover > ./catalog.json
```

## Development

```bash
pipx install poetry
poetry install
hotglue-smoke-test run
```
