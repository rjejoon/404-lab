import requests

raw_url = "https://raw.githubusercontent.com/rjejoon/404-lab/main/01/01.py"

r = requests.get(raw_url)
print(r.text)
