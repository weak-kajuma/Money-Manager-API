from fastapi import FastAPI, Depends
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import os
import json

from api.db import destroy_db
from api.auth import get_user
from api.routers import users, dealers, transactions

class RootResponse(BaseModel):
    message: str

app = FastAPI()

# 必ずCROS変更する
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# @app.get("/", response_model=RootResponse)
# async def root(user = Depends(get_user)):
#     print(user)
#     return RootResponse(message=user["uid"])

@app.delete("/destroy")
async def destroy_database(user = Depends(get_user)):
    admin_user_mailaddress = json.loads(os.getenv("ADMIN_USER_MAILADDRESS"))
    print(user)
    if set(user['firebase']['identities']['email']) & set(admin_user_mailaddress['users']):
        destroy_db()
        print("clear to destroy database")
    return

app.include_router(users.router)
app.include_router(dealers.router)
app.include_router(transactions.router)