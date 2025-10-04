from sqlalchemy.orm import Session
from sqlalchemy import or_
import models, schemas

def create_company(db: Session, company: schemas.CompanyCreate):
    db_obj = models.CompanyDetails(**company.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_companies(db: Session, search: str = None):
    q = db.query(models.CompanyDetails)
    if search:
        like = f"%{search}%"
        q = q.filter(or_(
            models.CompanyDetails.isin_no.like(like),
            models.CompanyDetails.company_name.like(like)
        ))
    return q.order_by(models.CompanyDetails.created_at.desc()).all()

def get_company(db: Session, company_id: int):
    return db.query(models.CompanyDetails).filter(models.CompanyDetails.id == company_id).first()

def update_company(db: Session, company_id: int, updates: dict):
    db_obj = get_company(db, company_id)
    if not db_obj:
        return None
    for k, v in updates.items():
        setattr(db_obj, k, v)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_company(db: Session, company_id: int):
    db_obj = get_company(db, company_id)
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True
