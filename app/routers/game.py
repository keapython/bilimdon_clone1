from fastapi import APIRouter, HTTPException
 
from app.dependencies import db_dep, current_user_dep, admin_user_dep
from app.models import Game
from app.schemas.game import GameResponse, GameCreate, GameUpdate
 
 
router = APIRouter(prefix="/games", tags=["games"])

@router.get('/', response_model=list[GameResponse])
async def get_games(db: db_dep):
    db_games = db.query(Game).all() 
    return db_games

@router.get('/{game_id}', response_model=GameResponse)
async def get_game(game_id: int, db: db_dep):
    db_game = db.query(Game).filter(Game.id == game_id).first()

    if not db_game:
        raise HTTPException(
            status_code=404,
            detail="Game not found."
        )
    
    return db_game

@router.post('/create/', response_model=GameResponse)
async def create_game(
    db: db_dep,
    game: GameCreate,
    current_user: current_user_dep
):
    
    db_game = Game(
        **game.model_dump(),
        owner_id=current_user.id
        )
    
    db.add(db_game)
    db.commit()
    db.refresh(db_game)

    return db_game 

@router.put('/update/{game_id}', response_model=GameResponse)
async def update_game(
    game_id: int,
    db: db_dep,
    game: GameUpdate,
):
    db_game = db.query(Game).filter(Game.id == game_id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    db_game.title = game.title if game.title else db_game.title
    db_game.description = game.description if game.description else db_game.description
    db_game.topic_id = game.topic_id if game.topic_id else db_game.topic_id
    

    db.commit()
    db.refresh(db_game)

    return db_game 

@router.delete('/delete/{game_id}')
async def delete_game(
    db: db_dep,
    game_id: int,
    admin_user: admin_user_dep
):
    db_game = db.query(Game).filter(Game.id == game_id).first()
    
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    db.delete(db_game)
    db.commit()

    return {
        "game_id": game_id,
        "message": "Game deleted."
    }