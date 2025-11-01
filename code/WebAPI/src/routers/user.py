from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from src.db.session import get_db
from src.db import models
from src.auth.authentication import get_current_team_lead
from src import schemas
from src.crud import user as crud

router = APIRouter()


@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db),
    lead: models.TeamLead = Depends(get_current_team_lead)
):
    """Create a new user in one of the lead's teams."""
    user = crud.create_user(db, user_data, lead.id)
    return {
        "id": user.id,
        "name": user.name,
        "lastname": user.lastname,
        "email": user.email
    }


@router.get("/", response_model=List[schemas.UserOut])
def list_my_users(
    db: Session = Depends(get_db),
    lead: models.TeamLead = Depends(get_current_team_lead)
):
    """List all users from all teams owned by the logged-in team lead."""
    users = crud.list_users(db, lead.id)
    return [
        {
            "id": u.id,
            "name": u.name,
            "lastname": u.lastname,
            "email": u.email
        }
        for u in users
    ]


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    lead: models.TeamLead = Depends(get_current_team_lead)
):
    """Get user info only if they belong to one of the lead's teams."""
    user = crud.get_user(db, user_id, lead.id)
    return {
        "id": user.id,
        "name": user.name,
        "lastname": user.lastname,
        "email": user.email
    }


@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user_endpoint(
    user_id: int,
    user_data: schemas.UserUpdate,
    db: Session = Depends(get_db),
    lead: models.TeamLead = Depends(get_current_team_lead)
):
    """Update user info only if they belong to one of the lead's teams."""
    user = crud.update_user(db, user_id, user_data, lead.id)
    return {
        "id": user.id,
        "name": user.name,
        "lastname": user.lastname,
        "email": user.email
    }


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    lead: models.TeamLead = Depends(get_current_team_lead)
):
    """Delete a user only if they belong to one of the lead's teams."""
    crud.delete_user(db, user_id, lead.id)
    return
