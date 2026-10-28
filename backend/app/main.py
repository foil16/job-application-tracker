from fastapi import FastAPI, status, Depends
from auth import register_user,login_user, get_current_user
from schemas import RegisterRequest, LoginRequest, Token, UserResponse


app = FastAPI()






@app.get("/health")
async def health():
    return {"status":"ok"}

@app.post("/auth/register",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def register(data: RegisterRequest):
    register_response = register_user(data.email,data.password)
    return register_response

@app.post("/auth/login",status_code = status.HTTP_200_OK, response_model= Token)
def login(data: LoginRequest):
    login_response = login_user(data.email,data.password)
    return Token(access_token=login_response,token_type = "Bearer")

@app.get("/users/me",status_code=status.HTTP_200_OK, response_model=UserResponse)
def read_me(current_user = Depends(get_current_user)):
    return current_user
    



    

