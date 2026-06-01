from pydantic import BaseModel

# Area Distribution schema
class AreaDistribution(BaseModel):
    residential: float
    road: float
    open_space: float
