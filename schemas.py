from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class CompanyBase(BaseModel):
    company_name: str
    paid_up_capital: Optional[str] = None
    face_value: Optional[float] = None
    no_of_shares: Optional[int] = None
    shareholders_demat: Optional[str] = None
    shareholders_physical: Optional[str] = None
    contact_person: Optional[str] = None
    designation: Optional[str] = None
    company_address: Optional[str] = None
    cin: Optional[str] = None

    contact_no: Optional[constr(pattern=r'^\d{10}$')] = None 

    email: Optional[EmailStr] = None
    gstin: Optional[str] = None
    company_type: Optional[str] = None
    listing_status: Optional[str] = None

    isin_no: constr(min_length=12, max_length=12)

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True