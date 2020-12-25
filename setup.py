import os, logging
from coloredlogs import install
from datetime import date
from sys import argv
from json import dumps, load
from string import ascii_letters

EXCLUDE = [
    ".vscode",
    "API",
    ".git"
]

CONFIG = {
    "MAIN": "index.html",
    "Title": "",
    "AUTHOR": "Wahyu Setianto",
    "DATE": date.today().strftime("%d/%m/%Y"),
    "SYNOPSIS": "",
    "IMG": None
}

def renderMD(API:list, header:str, footer:str) -> str:
    """
    Get new content to update README
    """
    content = ''
    for i, x in enumerate(API):
        content += f"{i + 1} [{x['Title']}]({x['url']})\n\n"
    return header + content + footer

def CreateProject(name:str) -> None:
    """
    Generate New Project
    """
    PATH = os.path.join(os.getcwd(), name)
    if not os.path.isdir(PATH):
        logging.info(f"Makin Directory for {name}")
        os.mkdir(name)

    config_file = os.path.join(PATH, 'config.json')
    if not os.path.isfile(config_file):
        logging.info("Setting config.json")
        with open(config_file, 'w') as f:
            CONFIG["Title"] = ''.join([x if x in ascii_letters else ' ' for x in name])
            f.write(dumps(CONFIG, indent = 2))
    else:
        logging.error("Project already exits!")
        raise EnvironmentError("Already exist!")

    logging.info("Done!")


if __name__ == "__main__":
    print()
    install()
    args = argv[1:]

    if args[0] == "create":
        CreateProject(args[1])

    elif len(args) == 1 and args[0] == "update":
        contents = [x for x in os.listdir('.') if x not in EXCLUDE and os.path.isdir(x)]
        API = []
        for content in contents:
            config_json = os.path.join(os.getcwd(), content, 'config.json')
            with open(config_json) as f:
                config_json = load(f)
            config_json["url"] = f'https://hyuto.github.io/notebooks/{content}/'
            if config_json["IMG"]:
                config_json["IMG"] = config_json["url"] + config_json["IMG"]
            if config_json["MAIN"] != "index.html":
                config_json["url"] += config_json["MAIN"]
            API.append(config_json)

        API.sort(key = lambda x: x["Title"])

        with open('README.md') as f:
            data = f.read()

        header = data[:data.index('## Content\n') + 11]
        footer = data[data.index('## Environments'):]

        with open(os.path.join('API', 'API.json'), 'w') as f:
            f.write(dumps(API, indent = 3))

        with open('README.md', 'w') as f:
            f.write(renderMD(API, header, footer))
    else:
        raise KeyError("Command not found!")