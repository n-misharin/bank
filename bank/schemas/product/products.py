from pydantic import BaseModel, UUID4, Field


class BuyProductRequest(BaseModel):
    product_id: UUID4
    bill_id: UUID4


class BuyProductResponse(BaseModel):
    message: str


class AddProductRequest(BaseModel):
    title: str = Field(max_length=50, min_length=2)
    description: str = Field(default="")
    cost: float


class UpdateProductRequest(BaseModel):
    title: str = Field(max_length=50, min_length=2, default=None)
    description: str = Field(default=None)
    cost: float = Field(default=None)
