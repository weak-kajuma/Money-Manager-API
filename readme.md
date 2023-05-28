# Deploy
```
touch .env
pip install -r requirements.txt
uvicorn mockApi.main:app --reload
```

# What to write in .env or secret.yaml
- DB_HOST: database hostname or ip
- DB_USER: database user
- DB_PASSWORD: database user password
- DB_DATABASE: using database
- ADMIN_USER_MAILADDRESS: admin's mail addresses in the list
- ACCOUNT_KEY: firebase account key in the json
- SSL_CA: client cert key


# Requirements
- mysql 8.0
- python 3.10.5