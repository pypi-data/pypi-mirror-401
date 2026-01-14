from pydantic import BaseModel


class InvestmentData(BaseModel):
    name: str
    eta: float
    I_B: float
    K: float
    P_out_nom_support: list
    maintenance_factor: float
