from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from bson import ObjectId
from .schemas import UserCreate, UserLogin, TokenResponse
from .utils import hash_password, verify_password, create_access_token
from .db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=201)
async def register(payload: UserCreate, db = Depends(get_db)):
    users = db["users"]
    existing = await users.find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    user_doc = {
        "email": payload.email,
        "password": hash_password(payload.password),
    }
    res = await users.insert_one(user_doc)
    return {"id": str(res.inserted_id), "email": payload.email}

@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db = Depends(get_db)):
    users = db["users"]
    user = await users.find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    token = create_access_token(str(user["_id"]))
    return TokenResponse(access_token=token)