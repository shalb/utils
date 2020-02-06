# Get logs from github actions

## Requirements

* Admin rights to repo
* `GITHUB_TOKEN` with access to repo. [How create](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line#creating-a-token)
* copy `configuration.py.example` to `configuration.py` and set what you need

## First run

### Docker

```bash
docker build -t github_action_logs . && docker run github_action_logs
```

### Localy via Python

Python 3.6+

```bash
pip3 install -r requirements.txt
python3 main.py
```
