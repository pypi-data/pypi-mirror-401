# Prefect Keeper

A Prefect block for interacting with Keeper Security's Secrets Manager.

## Description

This project provides a custom Prefect block that allows interaction with Keeper Security's Secrets Manager. It enables secure retrieval of secrets stored in Keeper by record UID or record title within Prefect workflows.

## Features

- Seamless integration with Keeper Security's Secrets Manager
- Retrieve secrets by record UID or record title
- Secure handling of KSM configuration
- Easy configuration and intuitive usage

## Installation

To install this package, use the following command:

```bash
uv add prefect-keeper
```

## Usage

### Configuration

Before using the block, ensure that you have a valid KSM (Keeper Secrets Manager) configuration. The configuration should be provided as a base64 encoded string.

### Saving the Block

To save the Keeper block :

```python
from prefect_keeper import Keeper
from pydantic import SecretStr

# Initialize the Keeper block with your KSM configuration
keeper = Keeper(ksm_config=SecretStr("your-base64-encoded-config"))

# Save the block
keeper.save("my-keeper-block", overwrite=True)
```

### Loading and Using the Block

To load a previously saved block and use its methods:

```python
from prefect import flow
from prefect_keeper import Keeper

@flow
def example_flow():
    # Load the saved block
    keeper = Keeper.load("my-keeper-block")
    
    # Retrieve a secret by record UID
    record = keeper.get_record_by_uid("record-uid-123")
    print(f"Record by UID: {record}")
    
    # Retrieve a secret by record title
    record = keeper.get_record_by_title("My Secret Title")
    print(f"Record by Title: {record}")

if __name__ == "__main__":
    example_flow()
```

## Configuration

The block can be configured with the following parameters:

- `ksm_config`: The KSM config provided as a base64 encoded string. This is a required field and should be provided as a `SecretStr` for security.

### Configuration Example

```python
from prefect_keeper import Keeper
from pydantic import SecretStr

keeper = Keeper(
    ksm_config=SecretStr("your-base64-encoded-config")
)
```

## Development

### Prerequisites

- Python 3.10+
- Uv for dependency management
- Access to Keeper Security's Secrets Manager

### Development Installation

1. Clone the repository:

```bash
git clone https://github.com/patacoing/prefect-keeper.git
cd prefect-keeper
```

2. Install dependencies:

```bash
uv sync
```

This project uses [just](https://just.systems/man/en/) as a way to save and run project-specific commands.
You can go to [justfile](./justfile) or run `just -l` to display all available recipes

## Contribution

Contributions are welcome! Please open an issue or a pull request for any improvements or fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
