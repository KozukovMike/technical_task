from pydantic import BaseModel, Field


class Currency(BaseModel):
    name: str = Field(alias='Cur_Name')
    cur_id: int = Field(alias='Cur_ID')
    start_date: str = Field(alias='Cur_DateStart')
    end_date: str = Field(alias='Cur_DateEnd')
    scale:  int = Field(alias='Cur_Scale')
    offrate: int or None = None