from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

# -------------------------
# USER
# -------------------------
class UserBase(BaseModel):
    name: Optional[str]
    lastname: Optional[str]
    email: EmailStr

class UserCreate(UserBase):
    pass  # aggiungi password se vuoi gestire login/autenticazione

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# -------------------------
# TEAM LEAD
# -------------------------
class TeamLeadBase(BaseModel):
    name: str
    lastname: str
    email: EmailStr

class TeamLeadCreate(TeamLeadBase):
    password: str

class TeamLead(TeamLeadBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# -------------------------
# TEAM
# -------------------------
class TeamBase(BaseModel):
    team_lead_id: int

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# -------------------------
# QUESTION TYPE
# -------------------------
class QuestionTypeBase(BaseModel):
    type: str

class QuestionTypeCreate(QuestionTypeBase):
    pass

class QuestionType(QuestionTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# -------------------------
# QUESTION
# -------------------------
class QuestionBase(BaseModel):
    content: str
    team_lead_id: int
    question_type_id: int

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# -------------------------
# ANSWER
# -------------------------
class AnswerBase(BaseModel):
    content: str
    question_id: int

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# -------------------------
# TOKEN
# -------------------------
class TokenBase(BaseModel):
    token_value: str
    question_id: int
    user_id: Optional[int] = None
    used: Optional[bool] = False

class TokenCreate(TokenBase):
    expires_at: datetime

class Token(TokenBase):
    id: int
    created_at: datetime
    expires_at: datetime

    class Config:
        orm_mode = True
