from fastapi import APIRouter, BackgroundTasks
from ..recommender import recommender_service

router = APIRouter()


@router.post("/retrain")
def trigger_retrain(tasks: BackgroundTasks):
    tasks.add_task(recommender_service.train)
    return {"detail": "retraining started"}
