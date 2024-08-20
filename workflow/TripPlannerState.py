import datetime
import operator
from typing import Annotated, Optional, List

from pydantic import BaseModel

from constants import HOME_LOCATION


class TripPlannerState(BaseModel):
    messages: Annotated[list, operator.add]
    start_date: str
    end_date: str
    origin_country: str = HOME_LOCATION
    destination_country: str
    traveler_info: str = ""

    expectations: Optional[str] = None
    price_calculation: Optional[str] = ""
    itinerary: Optional[str] = ""
    bookings: Optional[str] = ""

    messages_len_cutoff: int = 0
    potential_answers: list = []


if __name__ == '__main__':
    tps = TripPlannerState(
        start_date='2024-09-08',
        end_date='2024-09-19',
        destination_country='Poland',
        messages=[]
    )
