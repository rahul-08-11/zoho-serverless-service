from pydantic import BaseModel, Field
from typing import Optional


class Quotes(BaseModel):
    Name : Optional[str] = None
    Carriers : Optional[str] = None
    Delivery_Date_Range : Optional[str] = None
    pickup_date_range : Optional[str] = None
    Dropoff_Location : Optional[str] = None
    Estimated_Amount : Optional[str] = None
    Pickup_Location	 : Optional[str] = None
    Transport_Job_in_Deal: Optional[str] = None