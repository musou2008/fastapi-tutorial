from optparse import Option
from typing import Optional, List
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

app04 = APIRouter()

"""Response Model 响应模型"""


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    mobile: str = "10086"
    address: Optional[str] = None
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr  # 需要pip install pydantic[email]
    mobile: str = "10086"
    address: Optional[str] = None
    full_name: Optional[str] = None


users = {
    "user01": {
        "username": "user01",
        "password": "123123",
        "email": "user01@example.com",
    },
    "user02": {
        "username": "user02",
        "password": "123456",
        "email": "user02@example.com",
        "mobile": "110",
    },
}
# path operation
@app04.post("/reponse_model", response_model=UserOut, response_model_exclude_unset=True)
async def response_model(user: UserIn):
    """response_model_exclude_unset=True表示默认值不包含在响应中，仅包含实际给的值，如果实际给的值与默认值相同，也会包含在响应中"""
    print(user.password)  # password不会被返回
    return users["user02"]
