from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    
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
    type: str
    price: float
    
    class Config:
        from_attributes = True   

class ParkingRecordCreate(BaseModel):
    parking_spot_id: int 
    vehicle_id: int 
    paid: bool

    class Config:
        from_attributes = True   

class ParkingRecord(BaseModel):
    id: int
    parking_spot_id: int
    vehicle_id: int
    entry_time: datetime
    exit_time: Optional[datetime] = None
    price: Optional[float] = None
    paid: bool

    class Config:
        from_attributes = True  

class ParkingRecordCheckout(BaseModel):
    price: float 
    paid: bool

    class Config:
        from_attributes = True  