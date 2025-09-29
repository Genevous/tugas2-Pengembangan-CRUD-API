from fastapi import APIRouter, HTTPException, status
from modules.users.schema.schemas import UserCreate, UserOut
from typing import Dict
from datetime import datetime, UTC

router = APIRouter()

# In-memory storage
USERS: Dict[int, dict] = {}
NEXT_ID = {"val": 1}

def get_next_id() -> int:
    val = NEXT_ID["val"]
    NEXT_ID["val"] += 1
    return val

@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate):
    for u in USERS.values():
        if u["username"] == payload.username:
            raise HTTPException(status_code=400, detail="username already exists")
        if u["email"] == payload.email:
            raise HTTPException(status_code=400, detail="email already exists")

    user_id = get_next_id()
    now = datetime.now(UTC) 
    user = {
        "id": user_id,
        "username": payload.username,
        "email": payload.email,
        "password": payload.password,
        "role": payload.role,
        "created_at": now,
        "updated_at": now,
    }
    USERS[user_id] = user

    data = user.copy()
    data.pop("password", None)
    return UserOut(**data)
