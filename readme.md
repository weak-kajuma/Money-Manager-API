# Deploy
```
touch .env
pip install -r requirements.txt
uvicorn mockApi.main:app --reload
```

# What to write in .env
- DB_HOST: database hostname or ip
- DB_USER: database user
- DB_PASSWORD: database user password
- DB_DATABASE: using database

# Requirements
- mysql 8.0
- python 3.10.5