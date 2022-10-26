from pydantic import BaseModel, UUID4


class BuyProductRequest(BaseModel):
    product_id: UUID4
    bill_id: UUID4


class BuyProductResponse(BaseModel):
    message: str
