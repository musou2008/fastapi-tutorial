from doctest import Example
from enum import Enum
from lib2to3.pytree import Base
from datetime import date
from optparse import Option
from re import X
from typing import List, Optional
from fastapi import APIRouter, Path, Query, Cookie, Header
from pydantic import BaseModel, Field


app03 = APIRouter()

""" Path Parmeters and Number Validations 路径参数和数字验证 """


@app03.get("/path/parameters")
def path_params01():
    return {"message": "This is a message"}


@app03.get("/path/{parameters}")  # 函数的在代码内排列顺序就是路由的执行顺序
def path_params02(parameters: str):
    return {"message": parameters}


class CityName(str, Enum):
    Beijing = "Bejing China"
    Shanghai = "Shanghai China"


@app03.get("/enum/{city}")  # 枚举类型参数
async def latest(city: CityName):
    if city == CityName.Shanghai:
        return {"city_name": city, "confirmed": 1492, "death": 7}
    if city == CityName.Beijing:
        return {"city_name": city, "confirmed": 971, "death": 9}
    return {"city_name": city, "latest": "unknown"}


@app03.get("/files/{file_path:path}")  # 通过path parameters传递文件路径
def filepath(file_path: str):
    return f"The file path is {file_path}"


@app03.get("/path_validate/{num}")
def path_params_validate(
    num: int = Path(..., title="Your number", description="不可描述", ge=1, le=10)
):
    return num


""" Query Parmeters and String Validations 查询参数和字符串验证 """


@app03.get("/query")
def page_limit(page: int = 1, limit: Optional[int] = None):
    if limit:
        return {"page": page, "limit": limit}
    return {"page": page}


@app03.get("/query/bool/conversion")
def type_conversion(param: bool = False):
    return param


@app03.get("query/validations")
def query_params_validate(
    value: str = Query(..., min_length=8, max_length=16, regex="^a"),
    values: List[str] = Query(default=["v1", "v2"], alias="alias_name"),
):  # 多个查询参数的列表，参数别名
    return value, values


""" Request Body and Fields 请求体和字段 """


class CityInfo(BaseModel):
    name: str = Field(..., example="Beijing")  # example是注解的作用，值不会被验证
    country: str
    country_code: Optional[str] = None
    country_population: int = Field(
        default=800, title="人口数量", description="国家的人口数量", ge=800
    )

    class Config:
        schema_extra = {
            "example": {
                "name": "Shanghai",
                "country": "China",
                "country_code": "CN",
                "country_population": "1400000000",
            }
        }


@app03.post("/request_body/city")
def city_info(city: CityInfo):
    # print(city.name, city.country)
    return city.dict()


""" Request Body + Path parameters + Query parameters 多参数混合 """


@app03.put("/request_body/city/{name}")
def mix_city_info(
    name: str,  # 路径参数
    city01: CityInfo,  # 请求体
    city02: CityInfo,  # 请求体，Body可以定义多个的
    confirmed: int = Query(ge=0, description="确诊数", default=0),  # 查询参数
    death: int = Query(ge=0, description="死亡数", default=0),  # 查询参数
):
    if name == "Shanghai":
        return {"Shanghai": {"confirmed": confirmed, "death": death}}
    return city01.dict(), city02.dict()


""" Request Body - Nested Models 数据格式嵌套的请求体 """


class Data(BaseModel):
    city: Optional[List[CityInfo]] = None
    date: date
    confirmed: int = Field(ge=0, description="确诊数", default=0)
    death: int = Field(ge=0, description="死亡数", default=0)
    recovered: int = Field(ge=0, description="痊愈数", default=0)


@app03.put("/request_body/nested")
def nested_models(data: Data):
    return data


""" Cookie 和 Header 参数 """


@app03.get("/cookie")  # 需要使用PostMan测试
def cookie(cookie_id: Optional[str] = Cookie(None)):  # 定义Cookie参数需要使用Cookie类，否则就是查询参数
    return {"cookie_id": cookie_id}


@app03.get("/header")
def header(
    user_agent: Optional[str] = Header(None, convert_underscores=True),
    x_token: List[str] = Header(None),
):  # 有些HTTP代理和服务器是不允许在请求头中带有下划线的，convert_underscores=True 会把 user_agent 变成 user-agent，x_token是包含多个值的列表
    return {"User-Agent": user_agent, "x_token": X}
