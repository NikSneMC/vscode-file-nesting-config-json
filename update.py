#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p python3 python3.pkgs.requests
from re import compile
from requests import get
from json import loads, dump

Settings = dict[str, bool | dict[str, str]]


def get_raw_settings() -> str:
    match = compile(r"\`\`\`jsonc([\s\S]*?)\`\`\`").search(get("https://github.com/antfu/vscode-file-nesting-config/raw/refs/heads/main/README.md").text)
    if match is None:
        return "{}"
    return match.group()


def parse_settings() -> Settings:
    try:
        settings_raw: str = "{" + \
        "\n".join(filter(
            lambda l: l != "", 
            get_raw_settings()
                .removeprefix("```jsonc")
                .removesuffix("```")
                .split("\n")[3:]
        )).removesuffix(",") + \
        "}"

        settings: Settings = loads(settings_raw)
        return settings
    except Exception as e:
        return {}


def main() -> None:
    settings: Settings = parse_settings()
    if settings == {}:
        return
    with open(file="./settings.json", encoding="utf-8", mode="w") as f:
        dump(settings, f, indent=2)

if __name__ == "__main__":
    main()

