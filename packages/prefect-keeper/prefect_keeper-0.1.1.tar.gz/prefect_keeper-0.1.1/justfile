# Format the codebase
format:
    uv run ruff format

# Run the linter against the codebase
check *args:
    uv run ruff check {{ args }}

# Run the tests
tests *args:
    uv run pytest {{ args }}

# Run the type checker
type *args:
    uv run ty check {{ args }}

# Run the tests with coverage
coverage:
    uv run pytest --cov=src/

# Build the package
build:
    uv build

# Publish the package to pypi
publish token:
    uv publish --username __token__ --password {{ token }}
