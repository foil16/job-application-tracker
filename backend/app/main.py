from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from auth import register_user


app = FastAPI()

class RegisterRequest(BaseModel):
    email: EmailStr
    password : str = Field(...,min_length = 8)

class RegisterResponse(BaseModel):
    id : int
    email: EmailStr
    created_at: datetime




@app.get("/health")
async def health():
    return {"status":"ok"}

@app.post("/auth/register",status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest):
    registerResponse = register_user(data.email.lower(),data.password)
    return RegisterResponse(id = registerResponse[0], email = registerResponse[1],created_at=registerResponse[2])
    
    

