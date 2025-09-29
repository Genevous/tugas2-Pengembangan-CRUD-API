from fastapi import APIRouter, Header, HTTPException, Depends
from modules.users.schema.schemas import UserUpdate, UserOut
from modules.users.routes.createUser import USERS
from datetime import datetime, UTC

router = APIRouter()

def require_admin(x_user_role: str = Header(None)):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="admin only")

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, _=Depends(require_admin)):
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="user not found")

    user = USERS[user_id]
    if payload.username:
        user["username"] = payload.username
    if payload.email:
        user["email"] = payload.email
    if payload.password:
        user["password"] = payload.password
    if payload.role:
        user["role"] = payload.role
    user["updated_at"] = datetime.now(UTC) 

    data = {k: v for k, v in user.items() if k != "password"}
    return UserOut(**data)
