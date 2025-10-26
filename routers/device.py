from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.device import Device
from schemas.device import DeviceCreate, DeviceResponse

router = APIRouter()

# Example endpoint for devices
@router.get("/api/Devices/{id}", response_model=DeviceResponse)
async def get_device(id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.deviceid == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    return device
