
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.map import Map
from models.site import Site
from schemas.map import MapListItem, MapResponse
from schemas.site import SiteResponse
from datetime import datetime

router = APIRouter()

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
    map_response.sites = [SiteResponse.model_validate(site, from_attributes=True) for site in valid_sites]
    return map_response
