from fastapi import FastAPI, Depends
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from mockApi.routers import users, dealers, transactions

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
#     return RootResponse(message=user["uid"])

app.include_router(users.router)
app.include_router(dealers.router)
app.include_router(transactions.router)