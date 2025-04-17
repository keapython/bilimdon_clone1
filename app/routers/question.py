from fastapi import APIRouter, HTTPException, Depends

from app.schemas.question import QuestionResponse, QuestionCreate, QuestionUpdate
from app.models import Question
from app.dependencies import db_dep, current_user_dep



router = APIRouter(
    prefix="/questions",
    tags=["questions"],
    )


@router.get('/', response_model=list[QuestionResponse])
async def get_all_questions(db: db_dep):
    db_questions = db.query(Question).all()
    return db_questions

@router.get("/{id}", response_model=QuestionResponse)
async def get_question(id: int, db: db_dep):
    db_question = db.query(Question).filter(Question.id == id).first()
 
    if not db_question:
        raise HTTPException(
            status_code=404,
            detail="Question not found."
        )
     
    return db_question

@router.post('/create/', response_model=QuestionResponse)
async def create_question(
    db:db_dep,
    question: QuestionCreate,
    current_user: current_user_dep
    ):
   
    is_question_exists = db.query(Question).filter(Question.title == question.title).first()
    if is_question_exists:
        raise HTTPException(
            status_code=400,
            detail="This question already exists."
        )
    
    
    # db_question = Question(
    #     title = question.title,
    #     description = question.description,
    #     topic_id = question.topic_id,
    #     )

    db_question = Question(
        **question.model_dump(),
        owner_id=current_user.id
        )

    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    return db_question 


@router.put('/update/{question_id}', response_model=QuestionResponse)
async def update_question(
    question_id: int,
    updated_question: QuestionUpdate,
    db: db_dep
    ):
    
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")


    db_question.title = updated_question.title if updated_question.title else db_question.title
    db_question.description = updated_question.description if updated_question.description else db_question.description
    db_question.topic_id = updated_question.topic_id if updated_question.topic_id else db_question.topic_id
    

    db.commit()
    db.refresh(db_question)

    return db_question   


@router.delete('/delete/{question_id}')
async def delete_question(question_id: int, db: db_dep):
    db_question = db.query(Question).filter(Question.id == question_id).first()

    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(db_question)
    db.commit()

    return {
        "question_id": question_id,
        "message": "Question deleted."
    }
 