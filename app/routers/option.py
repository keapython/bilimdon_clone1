from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas.option import OptionCreate, OptionResponse, OptionUpdate
from app.dependencies import db_dep, current_user_dep
from app.models import Option




router = APIRouter(
    prefix="/options",
    tags=["options"],
)

@router.get("/", response_model=List[OptionResponse])
async def get_all_options(
    db: db_dep,
    ):

    db_options = db.query(Option).all()
    return db_options


@router.get("/{option_id}", response_model=OptionResponse)
async def get_option(
    db: db_dep,
    option_id: int,
    ):

    db_option = db.query(Option).filter(Option.id == option_id).first()
    if not db_option:
        raise HTTPException(
            status_code=404,
            detail="Option not found."
        )
    return db_option



@router.post("/create/", response_model=OptionResponse)
async def create_option(
    db: db_dep,
    option: OptionCreate,
    current_user: current_user_dep
    ):
    existing_correct_option = db.query(Option).filter(
        Option.question_id == option.question_id, 
        Option.is_correct == True
    ).first()

    if existing_correct_option and option.is_correct:
        raise HTTPException(
            status_code=400,
            detail="Question already has a correct option."
        )
    
    # db_option = Option(
    #     question_id = option.question_id,
    #     title = option.title,
    #     is_correct = option.is_correct,
    # ) 

    # or

    db_option = Option(
        **option.model_dump()
        )
 
    db.add(db_option)
    db.commit()
    db.refresh(db_option)

    return db_option


@router.put("/update/{option_id}", response_model=OptionResponse)
async def update_option(
    option_id: int,
    option: OptionCreate,
    db: db_dep,
    ):
    updated_option = db.query(Option).filter(Option.id == option_id).first()
    if not updated_option:
        raise HTTPException(
            status_code=404,
            detail="Option not found."
        )
    
    updated_option.title = option.title if option.title else updated_option.title
    updated_option.is_correct = option.is_correct if option.is_correct else updated_option.is_correct
    
    db.add(updated_option)
    db.commit()
    db.refresh(updated_option)

    return updated_option


@router.delete("/delete/{option_id}")
async def delete_option(
    db: db_dep,
    option_id: int,
    ):

    deleted_option = db.query(Option).filter(Option.id == option_id).first()

    if not deleted_option:
        raise HTTPException(status_code=404, detail="Option not found")

    db.delete(deleted_option)
    db.commit()

    return {
        "option_id": option_id,
        "detail": "Option deleted successfully"
    }

   