"""Contains functions for snake case conversions."""


def kebab_to_snake(name: str) -> str:
    """Convert `name` from kebab-case to snake_case."""
    return name.replace("-", "_").lower()
