import os
from json import dumps
from string import ascii_letters

def renderMD(API, header, footer):
    content = ''
    for i, x in enumerate(API):
        content += f"{i + 1} [{x['name']}]({x['url']})\n\n"
    return header + content + footer

if __name__ == "__main__":
    exclude = [
        "API",
        ".git"
    ]

    contents = [x for x in os.listdir('.') if x not in exclude and os.path.isdir(x)]
    API = []
    for content in contents:
        temp = {
            'name':''.join([x if x in ascii_letters else ' ' for x in content]),
            'url' : '/'.join([content, 'index.html'])
        }
        API.append(temp)

    with open('README.md') as f:
        data = f.read()

    header = data[:data.index('## Content\n') + 11]
    footer = data[data.index('## Environments'):]

    with open('API/API.json', 'w') as f:
        f.write(dumps(API))

    with open('README.md', 'w') as f:
        f.write(renderMD(API, header, footer))