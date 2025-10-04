from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import database, models, schemas, crud
import io
import pandas as pd 

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="ISIN Management")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------- HTML PAGE ROUTES -----------------

@app.get("/", response_class=HTMLResponse)
def get_form():
    with open("static/form.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    try:
        with open("static/dashboard.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Dashboard file not found (static/dashboard.html)")


# ----------------- CRUD API ROUTES -----------------

@app.post("/company", response_model=schemas.Company)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    """Creates a new company record."""
    try:
        return crud.create_company(db, company)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="ISIN already exists or DB constraint error")


@app.get("/company", response_model=list[schemas.Company])
def list_companies(search: str = Query(None), db: Session = Depends(get_db)):
    """Lists all companies, optionally filtered by ISIN or Company Name."""
    return crud.get_companies(db, search)


# ----------------- EXPORT ROUTE -----------------

@app.get("/company/export", response_class=StreamingResponse)
def export_companies(search: str = Query(None), db: Session = Depends(get_db)):
    """Exports company data to an Excel file."""
    companies = crud.get_companies(db, search)
    if not companies:
        raise HTTPException(status_code=404, detail="No data to export")

    data = [company.__dict__ for company in companies]
    
    for d in data:
        d.pop('_sa_instance_state', None) 
        
    df = pd.DataFrame(data)

    export_columns = [
        'isin_no', 'company_name', 'contact_person', 'email', 'listing_status',
        'paid_up_capital', 'face_value', 'no_of_shares', 
        'shareholders_demat', 'shareholders_physical', 
        'designation', 'company_address', 'cin', 'contact_no', 'gstin', 
        'company_type', 'created_at'
    ]
    
    final_columns = [col for col in export_columns if col in df.columns]
    df = df[final_columns]
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='CompanyDetails')
    output.seek(0)
    
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=company_details_export.xlsx"}
    )


# ----------------- PARAMETERIZED ROUTES -----------------

@app.get("/company/{company_id}", response_model=schemas.Company)
def get_company(company_id: int, db: Session = Depends(get_db)):
    """Fetches a single company record by ID."""
    obj = crud.get_company(db, company_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@app.put("/company/{company_id}", response_model=schemas.Company)
def update_company(company_id: int, updates: schemas.CompanyCreate, db: Session = Depends(get_db)):
    """Updates an existing company record by ID."""
    updated = crud.update_company(db, company_id, updates.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Not found")
    return updated


@app.delete("/company/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    """Deletes a company record by ID."""
    ok = crud.delete_company(db, company_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Not found")
    return {"ok": True}