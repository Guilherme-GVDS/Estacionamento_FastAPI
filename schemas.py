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

class VehicleSchema(BaseModel):
    plate: str
    type: str
    phone_number: str
    email: str

    class Config:
        from_attributes = True   

class SpotSchema(BaseModel):
    is_occupied: bool
    price: float
    vehicle_id: int
    
    class Config:
        from_attributes = True   
