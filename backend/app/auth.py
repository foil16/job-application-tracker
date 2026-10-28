import os
import sys
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
from fastapi import HTTPException, status, Depends
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer



needed_env_vars = ["DATABASE_URL","SECRET_KEY_JWT"]
load_dotenv()

def check_env_vars():
    missing = [var for var in needed_env_vars if not os.getenv(var)]
    print(f"Missing environment variables : {', '.join(missing)}", file = sys.stderr)



database_url = os.getenv("DATABASE_URL")
secret_key_jwt = os.getenv("SECRET_KEY_JWT")


hasher = PasswordHash([Argon2Hasher()])
security_scheme = HTTPBearer()




def register_user(email,password):
    hashed_password = hasher.hash(password)

    with psycopg.connect(database_url) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            try:
                cur.execute(
                "INSERT INTO users (email,hashed_password) VALUES (%s,%s) RETURNING id,email,created_at",
                (email,hashed_password)

                )

                
                return cur.fetchone()

            except psycopg.errors.UniqueViolation:
                raise HTTPException(
                    status_code = status.HTTP_409_CONFLICT,
                    detail = "Email is already in use"
                    )

def login_user(email,password):
    with psycopg.connect(database_url) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT id,hashed_password FROM users WHERE email = %s", (email,))

            query_response = cur.fetchone()

            if query_response is None: raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= "Wrong email or password"
            )

            user_id = query_response['id']
            
            hashed_password = query_response['hashed_password']

            success = hasher.verify(password,hashed_password)
            
            

            if not success: raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Wrong email or password"
            )

            payload = {"sub" : str(user_id), "exp" : datetime.now(timezone.utc) + timedelta(hours = 1)}

            jwt_token = jwt.encode(payload, secret_key_jwt, algorithm = "HS256")

            return jwt_token

            
def read_token(token):
    try: 
        payload = jwt.decode(token,secret_key_jwt,algorithms=["HS256"])
    except jwt.exceptions.PyJWTError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid token"
        )

    user_id = payload['sub']
   
    with psycopg.connect(database_url) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(("SELECT id, email, created_at FROM users WHERE id = %s"),
            (user_id,))
            resp = cur.fetchone()

            if resp is None:
                raise HTTPException(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    detail= "Invalid token"
                )

            return resp

def get_current_user(credentials = Depends(security_scheme)):
    token = credentials.credentials
    return read_token(token)

