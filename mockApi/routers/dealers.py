from fastapi import APIRouter, HTTPException 
import random
from mockApi.schemas.dealers import DealerCreate, Dealer

router = APIRouter()

@router.post("/dealers", response_model=Dealer)
async def create_dealers(dealer_create: DealerCreate):
    return Dealer(dealer_id=format(random.randrange(2**16-1), '04x'), **dealer_create.dict())

@router.get("/dealers", response_model=list[Dealer])
async def get_dealers():
    return [Dealer(dealer_id=format(random.randrange(2**16-1), '04x'))]

@router.get("/dealers/{dealer_id}", response_model=Dealer)
async def get_dealer_info(dealer_id: str):
    return Dealer(dealer_id=dealer_id)
    
@router.put("/dealers/{dealer_id}", response_model=Dealer)
async def update_dealers_info(dealer_id: str, dealer_update: DealerCreate):
    return Dealer(dealer_id=dealer_id, **dealer_update.dict())