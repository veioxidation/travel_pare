import datetime
import operator
from typing import Annotated, Optional

from pydantic import BaseModel

from constants import HOME_LOCATION


class TripPlannerState(BaseModel):
    messages: Annotated[list, operator.add]
    start_date: str
    end_date: str
    origin_country: str = HOME_LOCATION
    destination_country: str

    expectations: Optional[str] = None
    price_calculation: Optional[str] = ""
    itinerary: Optional[str] = ""
    bookings: Optional[str] = ""
