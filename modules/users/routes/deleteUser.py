from fastapi import APIRouter, Header, HTTPException, Depends
from modules.users.routes.createUser import USERS

router = APIRouter()

def require_admin(x_user_role: str = Header(None)):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="admin only")

@router.delete("/users")
def delete_all_users(_=Depends(require_admin)):
    USERS.clear()
    return {"detail": "all users deleted"}

@router.delete("/users/{user_id}")
def delete_user(user_id: int, _=Depends(require_admin)):
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="user not found")
    del USERS[user_id]
    return {"detail": "user deleted"}
