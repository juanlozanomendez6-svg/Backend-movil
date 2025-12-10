# app/schemas/common.py
from pydantic import BaseModel

class SuccessResponse(BaseModel):
    success: bool
    message: str
