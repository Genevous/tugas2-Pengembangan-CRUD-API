from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
import re

class UserBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username: str = Field(..., min_length=6, max_length=15)
    email: EmailStr
    role: str

    @field_validator("username")
    def username_lower_alnum(cls, v: str):
        if v != v.lower():
            raise ValueError("username must be lowercase")
        if not re.fullmatch(r"[a-z0-9]+", v):
            raise ValueError("username must be alphanumeric lowercase")
        return v

    @field_validator("role")
    def role_enum(cls, v: str):
        if v not in ("admin", "staff"):
            raise ValueError("role must be 'admin' or 'staff'")
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=20)

    @field_validator("password")
    def password_rules(cls, v: str):
        if not re.fullmatch(r"[A-Za-z0-9!@]{8,20}", v):
            raise ValueError("password must be alphanumeric with ! or @ only")
        if not re.search(r"[A-Z]", v):
            raise ValueError("must contain uppercase")
        if not re.search(r"[a-z]", v):
            raise ValueError("must contain lowercase")
        if not re.search(r"[0-9]", v):
            raise ValueError("must contain digit")
        if not re.search(r"[!@]", v):
            raise ValueError("must contain ! or @")
        return v

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None

class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
