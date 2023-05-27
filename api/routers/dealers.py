import pymysql
from fastapi import APIRouter, Depends, HTTPException 
import random
from api.auth import get_user
from api.db import mysql_connect
from api.schemas.dealers import DealerCreate, Dealer

router = APIRouter()

@router.post("/dealers", response_model=Dealer)
async def create_dealers(dealer_create: DealerCreate, user = Depends(get_user)):
    _dealer_id = format(random.randrange(2**16-1), '04x')
    with mysql_connect() as con:
        with con.cursor() as cur:
            cur.execute("INSERT INTO dealers (dealer_id, name, description, creator) VALUES (%s, %s, %s, %s)", (_dealer_id, dealer_create.name, dealer_create.description, dealer_create.creator))
            con.commit()
            cur.execute("SELECT * FROM dealers WHERE dealer_id = %s", (_dealer_id))
        return Dealer(**cur.fetchone())

@router.get("/dealers", response_model=list[Dealer])
async def get_dealers():
    with mysql_connect() as con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM dealers")
            return [Dealer(**dealers) for dealers in cur.fetchall()]

@router.get("/dealers/{dealer_id}", response_model=Dealer)
async def get_dealer_info(dealer_id: str):
    with mysql_connect() as con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM dealers WHERE dealer_id = %s", (dealer_id))
            dealer = cur.fetchone()
            if dealer is None:
                raise HTTPException(status_code=404, detail="The Dealer is Not Found")
            return Dealer(**dealer)

@router.put("/dealers/{dealer_id}", response_model=Dealer)
async def update_dealers_info(dealer_id: str, dealer_update: DealerCreate, user = Depends(get_user)):
    with mysql_connect() as con:
        with con.cursor() as cur:
            try:
                cur.execute("UPDATE dealers SET name = %s, description = %s, creator = %s WHERE dealer_id = %s", (dealer_update.name, dealer_update.description, dealer_update.creator, dealer_id))
            except pymysql.err.DataError:
                raise HTTPException(status_code=400, detail="The name or description is too long. Under 10 or 32")
        con.commit()
        with con.cursor() as cur:
            cur.execute("SELECT * FROM dealers WHERE dealer_id = %s", (dealer_id))
            dealer = cur.fetchone()
            if dealer is None:
                raise HTTPException(status_code=404, detail="The Dealer is Not Found") 
            return Dealer(**dealer)
