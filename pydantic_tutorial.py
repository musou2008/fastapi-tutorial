from re import A
from typing import List, Optional
from datetime import datetime, date
from pathlib import Path

from pydantic import BaseModel, ValidationError, Field

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base

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
    User(signup_ts="broken", friends=[1, 2, "not number"])
except ValidationError as e:
    print(e.json())

print("--- 模型类的属性和方法 ---")
print(user.dict())
print(user.json())
print(user.copy())  # 浅拷贝
print(User.parse_obj(obj=external_data))
print(
    User.parse_raw(
        '{"id": 123, "name": "John Snow", "signup_ts": "2022-12-22T12:22:00", "friends": [1, 2, 3]}'
    )
)
path = Path("pydantic_tutorial.json")
path.write_text(
    '{"id": 123, "name": "John Snow", "signup_ts": "2022-12-22T12:22:00", "friends": [1, 2, 3]}'
)
print(User.parse_file(path))

print(user.schema())
print(user.schema_json())


class User_Data(BaseModel):
    id: int
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


user_data = {
    "id": "error",
    "signup_ts": "2022-12-22 12:22",
    "friends": [1, 2, 3],
}  # id是字符串
print(User.construct(**user_data))  # 不检验数据直接创建模型类，不建议在construct方法中传入未经验证的数据

print(User.__fields__.keys())


class Sound(BaseModel):
    sound: str


class Dog(BaseModel):
    birthday: date
    weight: Optional[float] = None
    sound: List[Sound]  # 不同的狗有不同的叫声。递归模型(Recursive Models)就是指一个嵌套一个


wang = Sound(sound="wang wang ~")
ying = Sound(sound="ying ying ~")

dogs = Dog(
    birthday=date.today(),
    weight=6.66,
    sound=[wang, ying],
)

print(dogs.dict())

print("--- ORM模型：从类实例创建符合ORM对象的模型 ---")

Base = declarative_base()


class CompanyOrm(Base): # type: ignore
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    name = Column(String(63), unique=True)
    domains = Column(ARRAY(String(255)))


class CompanyMode(BaseModel):
    id: int
    public_key: str = Field(..., max_length=20)
    name: str = Field(..., max_length=63)
    domains: List[str] = Field(..., max_length=255)

    class Config:
        orm_mode = True


co_orm = CompanyOrm(
    id=123, public_key="foobar", name="Testing", domains=["example.com", "foobar.com"]
)

print(co_orm)
print(CompanyMode.from_orm(co_orm))
