from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel

# --- DB CONFIG ---
DATABASE_URL = "postgresql://akhilmehra:your_password@localhost:5432/therapy_app"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Define Table ---
class SalesLeads(Base):
    __tablename__ = "sales_leads"

    lead_id = Column(Integer, primary_key=True, index=True)
    lead_name = Column(String, nullable=False)
    contact_information = Column(String, nullable=False)
    source = Column(String, nullable=False)
    interest_level = Column(String, nullable=False)
    status = Column(String, nullable=False)
    assigned_salesperson = Column(String, nullable=False)

# --- Pydantic Schemas ---
class SalesLeadsReturnsBase(BaseModel):
    lead_id: int
    lead_name: str
    contact_information: str
    source: str
    interest_level: str
    status: str
    assigned_salesperson: str

class SalesLeadsReturnCreate(SalesLeadsReturnsBase):
    pass

class SalesLeadsReturnOut(SalesLeadsReturnsBase):
    lead_id: int

    class Config:
        orm_mode = True

# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- FastAPI App ---
app = FastAPI()

# Read all
@app.get("/sales_leads", response_model=list[SalesLeadsReturnOut])
def retrieve_sales_leads(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(SalesLeads).offset(skip).limit(limit).all()

# Read by source, interest level, status
@app.get("/sales_leads/{source}/{interest_level}/{status}", response_model=list[SalesLeadsReturnOut])
def retrieve_sales_leads_by_filter(source: str, interest_level: str, status: str, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    sales_leads = (
        db.query(SalesLeads)
        .filter(
            SalesLeads.source == source,
            SalesLeads.interest_level == interest_level,
            SalesLeads.status == status,
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
    return sales_leads
