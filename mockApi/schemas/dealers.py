from typing import List
from pydantic import BaseModel, Field

class Dealer(BaseModel):
    dealer_id: str = Field(None, example="d12f", description="format(random.randrange(2**16-1), '04x')")
    name: str = Field("名無しのお店")
    description: str = Field("よく当たると言われているらしい")
    creator: str = Field("高槻太郎")

class DealerCreate(BaseModel):
    name: str = Field("名無しのお店")
    description: str = Field("よく当たると言われているらしい")
    creator: str = Field("高槻太郎")
