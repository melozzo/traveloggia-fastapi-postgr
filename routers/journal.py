from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.journal import Journal
from schemas.journal import JournalCreate, JournalResponse, JournalUpdate

router = APIRouter()

# Example endpoint for journals

# Returns all journals for a given site ID
from typing import List


# GET: api/Journals/{id} - get all journals for a site
@router.get("/api/Journals/{id}", response_model=List[JournalResponse])
async def get_journals(id: int, db: Session = Depends(get_db)):
    journals = db.query(Journal).filter(Journal.siteid == id).all()
    return [JournalResponse.model_validate(journal, from_attributes=True) for journal in journals]

# GET: api/Journal/{id} - get a single journal by id
@router.get("/api/Journal/{id}", response_model=JournalResponse)
async def get_journal(id: int, db: Session = Depends(get_db)):
    journal = db.query(Journal).filter(Journal.journalid == id).first()
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    return JournalResponse.model_validate(journal, from_attributes=True)

# POST: api/Journals - create a new journal
@router.post("/api/Journals", response_model=JournalResponse)
async def post_journal(journal: JournalCreate, db: Session = Depends(get_db)):
    from datetime import datetime
    data = journal.model_dump(exclude_unset=True)
    new_journal = Journal(**data)
    new_journal.dateadded = datetime.now()
    new_journal.journaldate = datetime.now()
    db.add(new_journal)
    db.commit()
    db.refresh(new_journal)
    return JournalResponse.model_validate(new_journal, from_attributes=True)

# PUT: api/Journals/{id} - update a journal
@router.put("/api/Journals/{id}", response_model=None)
async def put_journal(id: int, journal: JournalUpdate, db: Session = Depends(get_db)):
    db_journal = db.query(Journal).filter(Journal.journalid == id).first()
    if not db_journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    for key, value in journal.model_dump(exclude_unset=True).items():
        setattr(db_journal, key, value)
    db.commit()
    return

# DELETE: api/Journals/{id} - delete a journal
@router.delete("/api/Journals/{id}", response_model=JournalResponse)
async def delete_journal(id: int, db: Session = Depends(get_db)):
    journal = db.query(Journal).filter(Journal.journalid == id).first()
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    db.delete(journal)
    db.commit()
    return JournalResponse.model_validate(journal, from_attributes=True)
