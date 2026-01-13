# tmail-api (Python wrapper)

Python port of [tmail-api](https://github.com/harshitpeer/TMail-API)

## Quick example

```py
from tmailpy import TMail

client = TMail('https://snapchat.email/api', 'API_KEY')
print(client.domains())
print(client.create())
print(client.messages('email@domain.com'))
```

## CLI

```
tmailpy https://snapchat.email/api API_KEY domains
```
