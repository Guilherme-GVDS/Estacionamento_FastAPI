from fastapi import APIRouter, Depends, HTTPException
from models import Vehicle, ParkingSpots
from dependencies import get_session, verify_token
from schemas import UserSchema, VehicleSchema, SpotSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError

park_router = APIRouter(prefix='/vehicle',tags=['vehicle'])

@park_router.get('/')
async def home():
    '''
    Rota de veiculos
    '''
    return {'sucesso':'Rota de veiculos'}

@park_router.post('/register_vehicle')
async def register_vehicle(vehicle_schema: VehicleSchema, 
                      session: Session = Depends(get_session)):
    vehicle = session.query(Vehicle).filter(Vehicle.plate==vehicle_schema.plate).first()

    if vehicle:
        raise HTTPException (status_code=400, detail='Carro já cadastrado')
    elif vehicle_schema.type not in ['moto','carro']:
        raise HTTPException (status_code=400, detail='Definir o tipo de veiculo para moto ou carro')
    else:
        new_vehicle = Vehicle(vehicle_schema.plate, vehicle_schema.type, 
                        vehicle_schema.phone_number, vehicle_schema.email)
        session.add(new_vehicle)
        session.commit() 
        return {'mensagem': f'Veiculo cadastrado {vehicle_schema.plate}'}
    
    


