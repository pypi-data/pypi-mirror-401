from __future__ import annotations

from fbnconfig import schemagen


def main() -> None:
    schemagen.cmd_validate_schema()
    print("Schema generation succeeded")


if __name__ == "__main__":
    main()
