from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from src.db.session import get_db
from src.db import models
from src.auth.authentication import get_current_team_lead
from src import schemas
from src.crud import team as crud

router = APIRouter()


@router.post("/", response_model=schemas.TeamOut, status_code=status.HTTP_201_CREATED)
def create_team_endpoint(
    team_data: schemas.TeamCreate,
    db: Session = Depends(get_db),
    lead: models.TeamLead = Depends(get_current_team_lead)
):
    """Create a new team owned by the logged-in team lead."""
    team = crud.create_team(db, team_data, lead.id)
    return {
        "id": team.id,
        "team_lead_id": team.team_lead_id,
        "users_ids": [u.id for u in team.users],
    }


@router.get("/", response_model=List[schemas.TeamOut])
def list_my_teams(
    db: Session = Depends(get_db),
    lead: models.TeamLead = Depends(get_current_team_lead)
):
    """List all teams owned by the logged-in team lead."""
    teams = crud.list_teams(db, lead.id)
    return [
        {"id": t.id, "team_lead_id": t.team_lead_id, "users_ids": [u.id for u in t.users]}
        for t in teams
    ]


@router.get("/{team_id}", response_model=schemas.TeamOut)
def get_team_endpoint(
    team_id: int,
    db: Session = Depends(get_db),
    lead: models.TeamLead = Depends(get_current_team_lead)
):
    """Get a team only if it belongs to the logged-in team lead."""
    team = crud.get_team(db, team_id, lead.id)
    return {"id": team.id, "team_lead_id": team.team_lead_id, "users_ids": [u.id for u in team.users]}


@router.put("/{team_id}", response_model=schemas.TeamOut)
def update_team_endpoint(
    team_id: int,
    team_data: schemas.TeamUpdate,
    db: Session = Depends(get_db),
    lead: models.TeamLead = Depends(get_current_team_lead)
):
    """Update a team only if it belongs to the logged-in team lead."""
    team = crud.update_team(db, team_id, team_data, lead.id)
    return {"id": team.id, "team_lead_id": team.team_lead_id, "users_ids": [u.id for u in team.users]}


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team_endpoint(
    team_id: int,
    db: Session = Depends(get_db),
    lead: models.TeamLead = Depends(get_current_team_lead)
):
    """Delete a team only if it belongs to the logged-in team lead."""
    crud.delete_team(db, team_id, lead.id)
    return
