from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas import User, UserCreate, UserUpdate
from services.database import users_db, get_next_user_id

router = APIRouter()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """Create a new user"""
    # Check if email already exists
    for existing_user in users_db.values():
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    user_id = get_next_user_id()
    new_user = {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "is_active": True
    }
    users_db[user_id] = new_user
    return new_user


@router.get("/", response_model=List[User])
def get_all_users():
    """Get all users"""
    return list(users_db.values())


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    """Get a specific user by ID"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return users_db[user_id]


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate):
    """Update a user"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user = users_db[user_id]
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Check if email is being updated and if it already exists
    if "email" in update_data and update_data["email"] != user["email"]:
        for uid, existing_user in users_db.items():
            if uid != user_id and existing_user["email"] == update_data["email"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
    
    user.update(update_data)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """Delete a user"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    del users_db[user_id]


@router.patch("/{user_id}/deactivate", response_model=User)
def deactivate_user(user_id: int):
    """Deactivate a user"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    users_db[user_id]["is_active"] = False
    return users_db[user_id]