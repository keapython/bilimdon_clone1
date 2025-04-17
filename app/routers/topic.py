from fastapi import APIRouter, HTTPException, Depends
from app.schemas.topic import TopicResponse, TopicCreate
from app.models import Topic
from app.dependencies import db_dep, current_user_dep, admin_user_dep


router = APIRouter(
    prefix="/topics",
    tags=["topics"],
    )


@router.get("/", response_model=list[TopicResponse])
async def get_topics(db: db_dep):
    return db.query(Topic).all()

@router.post("/create/", response_model=TopicResponse)
async def create_topic(
    db: db_dep,
    topic:TopicCreate,
    admin_user: admin_user_dep
    ):

    is_topic_exists = db.query(Topic).filter(Topic.name == topic.name).first()
    if is_topic_exists:
        raise HTTPException(
            status_code=400,
            detail="This topic already exists."
        )
    
    db_topic = Topic(
        name = topic.name,
        )

    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)

    return db_topic


@router.delete("/{topic_id}")
async def delete_topic(
    db: db_dep,
    topic_id: int,
    admin_user: admin_user_dep
    ):

    db_topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(
            status_code=404,
            detail="Topic not found."
        )

    db.delete(db_topic)
    db.commit()
    
    return {
        "topic_id": topic_id,
        "message": "Topic deleted."
    }

