from pydantic import BaseModel
from typing import Optional, List

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    admin: bool
    
    class Config:
        from_attributes = True

class UserAdmSchema(BaseModel):

    name: str
    email: str
    password: str
    admin: bool
    
    class Config:
        from_attributes = True
        
class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True    
