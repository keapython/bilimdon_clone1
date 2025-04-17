from fastapi import APIRouter, HTTPException

from app.schemas.participation import ParticipationResponse, ParticipationCreate, ParticipationUpdate
from app.models import Participation
from app.dependencies import db_dep, current_user_dep, admin_user_dep


router = APIRouter(
    prefix = "/participations",
    tags = ["participations"]
)

@router.get("/", response_model = list[ParticipationResponse])
async def get_all_participations(db: db_dep):
    participations = db.query(Participation).all()
    return participations

@router.get("/{participation_id}", response_model = ParticipationResponse)
async def get_participation(
    db: db_dep,
    pariticipation_id: int
):
    participation = db.query(Participation).filter(Participation.id == pariticipation_id).first()
    if not participation: 
        raise HTTPException(
            status_code=404,
            detail="Participation not found."
        )
    
    return participation

@router.post("/create/", response_model=ParticipationResponse)
async def create_participation(
    db: db_dep,
    participation: ParticipationCreate,
    current_user: current_user_dep
):
    db_participation = Participation(**participation.model_dump())

    
    db.add(db_participation)
    db.commit()
    db.refresh(db_participation)

    return db_participation 

@router.put("/update/{participation_id}", response_model=ParticipationResponse)
async def update_participation(
    db: db_dep,
    participation: ParticipationUpdate,
    participation_id: int
):
    updated_participation = db.query(Participation).filter(Participation.id == participation_id).first()
    if not updated_participation:
        raise HTTPException(
            status_code=404,
            detail="Participation not found."
        )
    
    updated_participation.game_id = participation.game_id if participation.game_id else updated_participation.game_id
    updated_participation.start_time = participation.start_time if participation.start_time else updated_participation.start_time
    updated_participation.end_time = participation.end_time if participation.end_time else updated_participation.end_time
    
    db.add(updated_participation)
    db.commit()
    db.refresh(updated_participation)

    return updated_participation

@router.delete('/delete/{participation_id}')
async def delete_participation(
    db: db_dep,
    participation_id: int,
):
    deleted_game = db.query(Participation).filter(Participation.id == participation_id).first()
    if not deleted_game:
        raise HTTPException(
            status_code=404,
            detail="Participation not found."
        )

    
    return {
        "participation_id": participation_id,
        "detail": "Participation deleted successfully"
    }
 


    