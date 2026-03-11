from pydantic import BaseModel

class FuelInput(BaseModel):

    gasoline: float
    diesel: float
    service_revenue: float
    fuel_revenue: float
    cash_gap: float