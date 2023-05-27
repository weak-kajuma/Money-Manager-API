import pymysql
from fastapi import APIRouter, Depends, HTTPException
import random

from api.auth import get_user
from api.schemas.users import User, CreateUserResponse
from api.schemas.transactions import Transaction
from api.db import mysql_connect

router = APIRouter()

@router.post("/users", response_model=CreateUserResponse)
async def create_user(user = Depends(get_user)):
    _user_id = format(random.randrange(2**16-1), '04x')
    with mysql_connect() as con:
        with con.cursor() as cur:
            cur.execute("INSERT INTO users (user_id) VALUES (%s)", (_user_id,))
            con.commit()
            cur.execute("SELECT * FROM users WHERE user_id = %s", (_user_id,))
            return CreateUserResponse(**cur.fetchone())
        
@router.get("/users", response_model=list[CreateUserResponse])
async def get_users(user = Depends(get_user)):
    with mysql_connect().cursor() as cur:
        cur.execute("SELECT * FROM users")
        return [CreateUserResponse(**user) for user in cur.fetchall()]
        
@router.get("/users/{user_id}", response_model=User)
async def get_user_info(user_id: str):
    with mysql_connect().cursor() as cur:
        cur.execute("SELECT * FROM (SELECT user_id, nickname, having_money, @rank := @rank + 1 AS `rank` FROM users, (SELECT @rank := 0) r ORDER BY having_money DESC) AS subquery WHERE user_id = %s", (user_id,))
        user_info = cur.fetchone()
        cur.execute("SELECT * FROM transactions WHERE user_id = %s", (user_id,))
        transactions = cur.fetchall()
    return User(**user_info, transaction_history=[Transaction(**tn) for tn in transactions])

@router.put("/users/{user_id}/nickname", response_model=CreateUserResponse)
async def update_name(user_id: str, nickname: str):
    with mysql_connect() as con:
        with con.cursor() as cur:
            try:
                cur.execute("UPDATE users SET nickname = %s WHERE user_id = %s", (nickname, user_id))
            except pymysql.err.DataError:
                raise HTTPException(status_code=400, detail="The Nickname is too long. Under 10")
        con.commit()
        with con.cursor() as cur:
            cur.execute("SELECT user_id, nickname, having_money FROM users WHERE user_id = %s", (user_id))
            user = cur.fetchone()
            if user is None:
                raise HTTPException(status_code=404, detail="The User is Not Found") 
            return CreateUserResponse(**user)
