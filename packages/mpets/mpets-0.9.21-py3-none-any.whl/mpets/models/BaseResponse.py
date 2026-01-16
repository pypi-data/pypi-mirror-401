from typing import Optional

from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: bool
    error: Optional[int] = None
    error_message: Optional[str] = None