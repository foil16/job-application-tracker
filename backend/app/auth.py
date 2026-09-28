import os
from dotenv import load_dotenv
import psycopg
from fastapi import HTTPException, status
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher


load_dotenv()
database_url = os.getenv("DATABASE_URL")

hasher = PasswordHash([Argon2Hasher()])



def register_user(email,password):
    hashed_password = hasher.hash(password)

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
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