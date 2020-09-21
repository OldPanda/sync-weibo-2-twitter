# sync-weibo-2-twitter

## Environment Setup
Python 3.8 is required. Rename the file `config.json.example` to `config.json` and replace `<your-ifttt-key>` with your IFTTT key. The `"token"` field is only to prevent your API being called from malicious sources, so you should put a string ONLY KNOWN TO YOU.
```
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Deployment
Rename file `deploy.sh.example` to `deploy.sh` and replace `<your-function-name>` inside file `deploy.sh` with your function name, then
```
./deploy.sh
```
