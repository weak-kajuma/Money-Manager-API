from pydantic import BaseModel, Field
from enum import Enum
import datetime

class TransactionType(Enum):
    bet = 1
    payout = 2
    payment = 3
    other = 4

class Transaction(BaseModel):
    transaction_id: str = Field(None, example="b5eb", description="format(random.randrange(2**16-1), '04x')")
    user_id: str = Field(None, example="9cf2", description="format(random.randrange(2**16-1), '04x')")
    dealer_id: str = Field(None, example="d12f", description="format(random.randrange(2**16-1), '04x')")
    amount: int = Field(None, example=100)
    type: TransactionType 
    timestamp: datetime.datetime = Field(None, example="2023-08-31 13:39:25")


class TransactionCreate(BaseModel):
    user_id: str = Field(None, example="9cf2", description="format(random.randrange(2**16-1), '04x')")
    dealer_id: str = Field(None, example="d12f", description="format(random.randrange(2**16-1), '04x')")
    amount: int = Field(None, example=100)
    type: TransactionType

class OneRankingResponse(BaseModel):
    rank: int
    user_id: str = Field(None, example="9cf2", description="format(random.randrange(2**16-1), '04x')")
    nickname: str = Field(None, example="名無しのギャンブラー")
    having_money: int