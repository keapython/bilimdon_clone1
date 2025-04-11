from fastapi import APIRouter, HTTPException, Depends, Response
from app.database  import * 
from app.schemas.question import *
from app.models import Question
from app.utils import *
from app.dependencies import *

# current_user_dep = Annotated[User, Depends(get_current_user)]

router = APIRouter(
    prefix="/question",
    tags=["question"],)


@router.get('/', response_model=list[QuestionResponse])
async def get_all_questions(db: db_dep):
    db_questions = db.query(Question).all()
    return db_questions



@router.post('/', response_model=QuestionResponse)
async def create_question(
    db:db_dep,
    question: QuestionCreate,
    ):
   
    is_question_exists = db.query(Question).filter(Question.title == question.title).first()
    if is_question_exists:
        raise HTTPException(
            status_code=400,
            detail="This question already exists."
        )
    
    db_question = Question(
        title = question.title,
        description = question.description,
        topic_id = question.topic_id,
        owner_id = question.owner_id
        )

    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    return db_question 


@router.get('/{question_id}', response_model=QuestionResponse)
async def get_question(question_id: int, db: db_dep):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise HTTPException(
            status_code=404,
            detail="Question not found."
        )
    return db_question


@router.put('/{question_id}', response_model=QuestionResponse)
async def update_question(
    question_id: int,
    updated_question: QuestionUpdate,
    db: db_dep
    ):
    
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")


    db_question.title = updated_question.title
    db_question.description = updated_question.description
    db_question.topic_id = updated_question.topic_id
    db_question.owner_id = updated_question.owner_id

    db.commit()
    db.refresh(db_question)

    return db_question   


@router.delete('/{question_id}')
async def delete_question(question_id: int, db: db_dep):
    db_question = db.query(Question).filter(Question.id == question_id).first()

    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(db_question)
    db.commit()

    return {"detail": "Question deleted successfully"}