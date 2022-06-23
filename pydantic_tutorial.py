from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ValidationError

print("--- Pydantic的基本用法 ---")
class User(BaseModel):
    id: int  # 必填字段
    name: str = "John Snow"  # 有默认值，选填字段
    signup_ts: Optional[datetime] = None
    friends: List[int] = []  # 列表中元素是int类型或者可以直接转换成int类型


external_data = {"id": "123", "signup_ts": "2022-12-22 12:22", "friends": [1, 2, "3"]}

user = User(**external_data)
print(user.id, user.friends)
print(user.signup_ts)
print(user.dict())

print("--- 校验失败处理 ---")
try:
    User(id=1, signup_ts=datetime.today(), friends=[1, 2, "not number"])
except ValidationError as e:
    print(e.json())

print("--- 模型类的属性和方法 ---")