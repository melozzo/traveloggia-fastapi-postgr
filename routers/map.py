
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.map import Map
from models.site import Site
from schemas.map import MapListItem, MapResponse, MapCreate, MapUpdate
from schemas.site import SiteResponse
from datetime import datetime

router = APIRouter()
@router.put("/api/Maps/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_map(id: int, map_update: MapUpdate, db: Session = Depends(get_db)):
    # Validate ID
    map_obj = db.query(Map).filter(Map.mapid == id).first()
    if not map_obj:
        raise HTTPException(status_code=404, detail="Map not found")
    if id <= 6088:
        raise HTTPException(status_code=400, detail="ID must be greater than 6088")
    # Update fields
    for field, value in map_update.model_dump(exclude_unset=True).items():
        setattr(map_obj, field, value)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating map")
    return

# POST: Create new map
@router.post("/api/Maps", response_model=MapResponse, status_code=status.HTTP_201_CREATED)
async def create_map(map_create: MapCreate, db: Session = Depends(get_db)):
    new_map = Map(**map_create.model_dump())
    new_map.createdate = datetime.now()
    db.add(new_map)
    db.commit()
    db.refresh(new_map)
    return MapResponse.model_validate(new_map, from_attributes=True)

# DELETE: Soft delete map
@router.delete("/api/Maps/{id}", response_model=MapResponse)
async def delete_map(id: int, db: Session = Depends(get_db)):
    map_obj = db.query(Map).filter(Map.mapid == id).first()
    if not map_obj:
        raise HTTPException(status_code=404, detail="Map not found")
    map_obj.isdeleted = True
    db.commit()
    return MapResponse.model_validate(map_obj, from_attributes=True)

# Returns the most recent map for a member, creates a default if none exists, and includes valid sites
@router.get("/api/Maps/{id}", response_model=MapResponse)
async def get_maps(id: int, db: Session = Depends(get_db)):
    map_response = None
    try:
        selected_map = db.query(Map).filter(Map.memberid == id, Map.isdeleted != True).order_by(Map.createdate.desc()).first()
        if selected_map:
            valid_sites = (
                db.query(Site)
                .filter(Site.mapid == selected_map.mapid, Site.isdeleted != True)
                .order_by(Site.routeindex, Site.arrival)
                .all()
            )
            map_response = MapResponse.model_validate(selected_map, from_attributes=True)
            map_response.Sites = [SiteResponse.model_validate(site, from_attributes=True) for site in valid_sites]
    except Exception as ex:
        pass

    # If no map exists, create a default map and return it
    if map_response is None:
        default_map = Map(
            mapname=datetime.now().strftime("%Y-%m-%d"),
            memberid=id,
            createdate=datetime.now()
        )
        db.add(default_map)
        try:
            db.commit()
            db.refresh(default_map)
            map_response = MapResponse.model_validate(default_map, from_attributes=True)
            map_response.Sites = []
        except Exception as ex:
            pass

    return map_response





@router.get("/api/MapList/{id}", response_model=list[MapListItem])
async def get_map_list(id: int, db: Session = Depends(get_db)):
    maps = db.query(Map).filter(
        Map.memberid == id,
        Map.isdeleted != True
    ).order_by(Map.createdate.desc()).all()
    return [MapListItem.model_validate(m) for m in maps]


# Equivalent to .NET SelectMap route
@router.get("/api/SelectMap/{id}", response_model=MapResponse)
async def select_map(id: int, db: Session = Depends(get_db)):
    selected_map = db.query(Map).filter(Map.mapid == id).first()
    if not selected_map:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Map not found")
    valid_sites = (
        db.query(Site)
        .filter(Site.mapid == selected_map.mapid, Site.isdeleted != True)
        .order_by(Site.routeindex, Site.arrival)
        .all()
    )
    map_response = MapResponse.model_validate(selected_map, from_attributes=True)
    map_response.Sites = [SiteResponse.model_validate(site, from_attributes=True) for site in valid_sites]
    return map_response
