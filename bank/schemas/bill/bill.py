from pydantic import BaseModel, UUID4, validator


class AddAmountRequest(BaseModel):
    signature: str
    transaction_id: int
    user_id: UUID4
    bill_id: UUID4
    amount: float
