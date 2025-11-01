from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from pydantic import Field

# -------------------------
# USER
# -------------------------
class UserBase(BaseModel):
    name: Optional[str]
    lastname: Optional[str]
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


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
        from_attributes = True


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
        from_attributes = True


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
        from_attributes = True


# -------------------------
# QUESTION
# -------------------------
class QuestionBase(BaseModel):
    content: str
    team_lead_id: int
    question_type_id: int


class Question(QuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class QuestionCreate(QuestionBase):
    token_type: str
    teams_ids: List[int]
    users_ids: Optional[List[int]] = Field(default_factory=list)


class QuestionCreateResponse(BaseModel):
    question: Question
    tokens: List[str]

    class Config:
        from_attributes = True


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
        from_attributes = True


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

class TokenOut(BaseModel):
    token_value: str
    id: int
    question_id: int
    user_id: Optional[int]
    used: bool
    created_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True
