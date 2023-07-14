from pydantic import BaseModel, Field
from typing import Optional, List

from api.schemas.transactions import Transaction

class User(BaseModel):
    user_id: str = Field(None, example="9cf2", description="format(random.randrange(2**16-1), '04x')")
    nickname: str = Field("名無しのギャンブラー")
    having_money: int = Field(3000, description="DEC(Denbutu Coin)")
    rank: int = Field(None, description="ranking")
    transaction_history: List[Transaction]

class CreateUserResponse(BaseModel):
    user_id: str = Field(None, example="9cf2", description="format(random.randrange(2**16-1), '04x')")
    nickname: str = Field("名無しのギャンブラー")
    having_money: int = Field(3000, description="DEC(Denbutu Coin)")
    token: str = Field()

class ShortUserResponse(BaseModel):
    user_id: str = Field(None, example="9cf2", description="format(random.randrange(2**16-1), '04x')")
    nickname: str = Field("名無しのギャンブラー")
    having_money: int = Field(3000, description="DEC(Denbutu Coin)")