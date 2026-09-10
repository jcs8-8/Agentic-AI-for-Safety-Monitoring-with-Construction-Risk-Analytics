from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    role: str = "site_manager"

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserProfile(BaseModel):
    user_id: str
    email: str
    full_name: str
    role: str
