from sqlalchemy import Column, Integer, String, Text, DateTime, Float, func
from database import Base

class CompanyDetails(Base):
    __tablename__ = "company_details"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False)
    paid_up_capital = Column(String(100))
    face_value = Column(Float)
    no_of_shares = Column(Integer)
    shareholders_demat = Column(String(100))
    shareholders_physical = Column(String(100))
    contact_person = Column(String(100))
    designation = Column(String(100))
    company_address = Column(Text)
    cin = Column(String(100))
    contact_no = Column(String(20))
    email = Column(String(150))
    gstin = Column(String(50))
    company_type = Column(String(100))
    listing_status = Column(String(100))
    isin_no = Column(String(12), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
