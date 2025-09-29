from fastapi import APIRouter, Header, HTTPException, Depends
from typing import Optional, List
from modules.users.schema.schemas import UserOut
from modules.users.routes.createUser import USERS

router = APIRouter()

def get_request_user(x_user_role: Optional[str] = Header(None), x_user_id: Optional[int] = Header(None)):
    if x_user_role not in ("admin", "staff"):
        raise HTTPException(status_code=403, detail="Invalid or missing role")
    return {"role": x_user_role, "id": x_user_id}

@router.get("/users", response_model=List[UserOut])
def read_all_users(req=Depends(get_request_user)):
    if req["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can read all")
    return [UserOut(**{k: v for k, v in u.items() if k != "password"}) for u in USERS.values()]

@router.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: int, req=Depends(get_request_user)):
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="user not found")

    if req["role"] == "admin":
        u = USERS[user_id]
        return UserOut(**{k: v for k, v in u.items() if k != "password"})

    if req["role"] == "staff":
        if req["id"] is None or int(req["id"]) != user_id:
            raise HTTPException(status_code=403, detail="staff can only read own")
        u = USERS[user_id]
        return UserOut(**{k: v for k, v in u.items() if k != "password"})
