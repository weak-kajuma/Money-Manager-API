from fastapi import APIRouter, Depends, HTTPException
import random
import datetime

from api.auth import get_user
from api.schemas.transactions import OneTransactionsResponse, Transaction, TransactionCreate, OneRankingResponse, TransactionType
from api.db import mysql_connect

router = APIRouter()

@router.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: str):
    with mysql_connect().cursor() as cur:
        cur.execute("SELECT * FROM transactions WHERE transaction_id = %s", (transaction_id,))
        return Transaction(**cur.fetchone())
    
@router.get("/transactions", response_model=list[OneTransactionsResponse])
async def get_transactions_latest(limit: int = 4):
    with mysql_connect().cursor() as cur:
        cur.execute("SELECT transaction_id, amount, type, timestamp, users.user_id, nickname FROM transactions JOIN users ON transactions.user_id=users.user_id ORDER BY timestamp DESC LIMIT %s", (limit,))
        return [OneTransactionsResponse(**ts) for ts in cur.fetchall()]


@router.post("/transactions", response_model=Transaction)
async def create_transactions(create_transaction: TransactionCreate, user = Depends(get_user)):
    with mysql_connect().cursor() as cur:
        cur.execute("SELECT having_money FROM users WHERE user_id = %s", (create_transaction.user_id,))
        row = cur.fetchone()
        if row is None or row["having_money"] is None:
            raise HTTPException(status_code=404, detail="The User is Not Found")
        having_money = row["having_money"]
        cur.execute("SELECT dealer_id FROM dealers WHERE dealer_id = %s", (create_transaction.dealer_id,))
        if cur.fetchone() is None:
            raise HTTPException(status_code=404, detail="The Dealer is Not Fount")
    _transaction_id = format(random.randrange(2**16-1), '04x')
    with mysql_connect() as con:
        with con.cursor() as cur:
            # ここからユーザーの所持金計算
            now_money = having_money + create_transaction.amount \
                if create_transaction.type in [TransactionType.payout, TransactionType.gift, TransactionType.other] \
                else having_money - create_transaction.amount
            if now_money < 0:
                raise HTTPException(status_code=402, detail="You do not have enough funds to complete the payment or the bet.")
            cur.execute("INSERT INTO transactions (transaction_id, user_id, dealer_id, amount, type, detail, hide_detail) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (_transaction_id, create_transaction.user_id, create_transaction.dealer_id, create_transaction.amount, create_transaction.type.name, create_transaction.detail, create_transaction.hide_detail))
            cur.execute("UPDATE users SET having_money = %s WHERE user_id = %s", (now_money, create_transaction.user_id))
            
            con.commit()
            cur.execute("SELECT * FROM transactions WHERE transaction_id = %s", (_transaction_id,))
            return Transaction(**cur.fetchone())

@router.get("/rankings", response_model=list[OneRankingResponse])
async def get_rankings(limit: int = 10):
    with mysql_connect().cursor() as cur:
        cur.execute(f"SELECT * FROM (SELECT user_id, nickname, having_money, ROW_NUMBER() OVER (ORDER BY having_money DESC) AS ranking FROM users) AS subquery LIMIT {limit}")
        return [OneRankingResponse(**user, rank=user["ranking"]) for user in cur.fetchall() if user["having_money"] > 3000]
    
@router.get("/rankings/{times}", response_model=list[OneRankingResponse])
async def get_rankings_limited_times(limit: int = 10, times: int = 5):
    with mysql_connect().cursor() as cur:
        cur.execute(f"SELECT * FROM (SELECT u.user_id, u.nickname, u.having_money, ROW_NUMBER() OVER (ORDER BY having_money DESC) AS ranking FROM users u LEFT JOIN ( SELECT user_id, COUNT(*) AS payout_count FROM transactions WHERE type = 'payout' GROUP BY user_id ) t ON u.user_id = t.user_id WHERE (t.payout_count >= 1 AND t.payout_count <= {times})) AS subquery LIMIT {limit};")
        print(f"SELECT * FROM (SELECT u.user_id, u.nickname, u.having_money, ROW_NUMBER() OVER (ORDER BY having_money DESC) AS ranking FROM users u LEFT JOIN ( SELECT user_id, COUNT(*) AS payout_count FROM transactions WHERE type = 'payout' GROUP BY user_id ) t ON u.user_id = t.user_id WHERE (t.payout_count >= 1 AND t.payout_count <= {times})) AS subquery LIMIT {limit}")
        return [OneRankingResponse(**user, rank=user["ranking"]) for user in cur.fetchall() if user["having_money"] > 3000]
        