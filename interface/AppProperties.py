import datetime

from pydantic import BaseModel


class AppProperties(BaseModel):
    chat_open: bool = False
    messages: list = []
    writing_mode: bool = True

    origin_country: str = "Singapore"
    country: str = ""
    start_date: datetime.date = datetime.date.today()
    end_date: datetime.date = datetime.date.today() + datetime.timedelta(days=7)
