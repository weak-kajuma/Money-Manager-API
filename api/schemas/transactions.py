from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
import datetime

class TransactionType(Enum):
    bet = "bet"
    payout = "payout"
    payment = "payment"
    gift = "gift"
    other = "other"

class Transaction(BaseModel):
    transaction_id: str = Field(None, example="b5eb", description="format(random.randrange(2**16-1), '04x')")
    user_id: str = Field(None, example="9cf2", description="format(random.randrange(2**16-1), '04x')")
    dealer_id: str = Field(None, example="d12f", description="format(random.randrange(2**16-1), '04x')")
    amount: int = Field(None, example=100)
    type: TransactionType
    detail: Optional[str] = Field(None, example="オッズ15倍 第一レース", description="倍率やレースの詳細など表示したいデータ")
    hide_detail: Optional[str] = Field(None, example="購入ID: 128", description="購入した商品のIDなど隠して保存しておきたいデータ")
    timestamp: datetime.datetime = Field(None, example="2023-08-31 13:39:25")


class TransactionCreate(BaseModel):
    user_id: str = Field(None, example="9cf2", description="format(random.randrange(2**16-1), '04x')")
    dealer_id: str = Field(None, example="d12f", description="format(random.randrange(2**16-1), '04x')")
    amount: int = Field(None, example=100)
    type: TransactionType
    detail: Optional[str] = Field(None, example="オッズ15倍 第一レース", description="倍率やレースの詳細など表示したいデータ")
    hide_detail: Optional[str] = Field(None, example="購入ID: 128", description="購入した商品のIDなど隠して保存しておきたいデータ")

class OneRankingResponse(BaseModel):
    rank: int
    user_id: str = Field(None, example="9cf2", description="format(random.randrange(2**16-1), '04x')")
    nickname: str = Field(None, example="名無しのギャンブラー")
    having_money: int