from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.auth.authentication import (
    authenticate_team_lead,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    hash_password as get_password_hash,
)
from src import schemas
from src.db import models

router = APIRouter()


@router.post("/register", response_model=schemas.TeamLeadOut, summary="Registra un nuovo Team Lead")
def register_team_lead(data: schemas.TeamLeadRegister, db: Session = Depends(get_db)):

    existing = db.query(models.TeamLead).filter(models.TeamLead.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un account con questa email esiste già."
        )


    hashed_pw = get_password_hash(data.password)
    new_lead = models.TeamLead(
        name=data.name,
        lastname=data.lastname,
        email=data.email,
        password=hashed_pw,
    )

    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    return new_lead

@router.post("/token", summary="Login TeamLead")
def login_team_lead(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    lead = authenticate_team_lead(db, form_data.username, form_data.password)
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o password errati",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": lead.email})
    refresh_token = create_refresh_token(data={"sub": lead.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh-token", summary="Refresh token")
def refresh_token(request: schemas.RefreshTokenRequest, db: Session = Depends(get_db)):
    email = verify_refresh_token(request.refresh_token)
    lead = db.query(models.TeamLead).filter(models.TeamLead.email == email).first()
    if not lead:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="TeamLead non trovato")

    access_token = create_access_token(data={"sub": lead.email})
    return {"access_token": access_token, "token_type": "bearer"}
