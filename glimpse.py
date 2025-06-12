

#   Use cases for REST API:
#    1. Retrieve all sales leads from DB (get ALL). (SELECT lead_name from DB)
#    2. Filter leads based on parameters like SOurce, Interest Level, and Status (SELECT lead_name from DB WHERE source/interest_level/status = X)
#    3. Paginate results to handle large datasets
#         Batch return results (10/50 results at a time etc.) FastAPI will have to handle returning 50 results at a time.

# CRUD APIs
# READ_ALL()
# READ_BY_FILTERS(Source, Interest_Level, Status)

# How do we want the DB to look? 

# Lead ID (Primary Key)
# Remaining 6 columns can be stored as STRINGS  

import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# --- CONFIG ---
DB_URL = "postgresql://akhilmehra:your_password@localhost:5432/therapy_app"
CSV_PATH = "/Users/akhilmehra/Documents/glimpse/lead_dataset.csv"

# --- SQLAlchemy Setup ---
Base = declarative_base()
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

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


# --- Create Table ---
Base.metadata.create_all(bind=engine)

# --- Load CSV and Insert ---
df = pd.read_csv(CSV_PATH)

# Ensure columns are clean (optional sanity check)
expected_columns = {'Lead ID', 'Lead Name', 'Contact Information', 'Source', 'Interest Level', 'Status', 'Assigned Salesperson'}
if set(df.columns) != expected_columns:
    raise ValueError(f"CSV columns must match exactly: {expected_columns}")

# Insert into DB
db = SessionLocal()
for _, row in df.iterrows():
    record = SalesLeads(
        lead_id=int(row['Lead ID']),
        lead_name=str(row['Lead Name']),
        contact_information=str(row['Contact Information']),
        source=str(row['Source']),
        interest_level=str(row['Interest Level']),
        status=str(row['Status']),
        assigned_salesperson=str(row['Assigned Salesperson'])
    )
    db.add(record)

db.commit()
db.close()

print("✅ Data imported into 'sales_leads' table successfully!")