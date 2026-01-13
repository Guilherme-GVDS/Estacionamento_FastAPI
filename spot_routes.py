from fastapi import APIRouter, Depends, HTTPException
from models import Vehicle, ParkingSpots
from dependencies import get_session, verify_token
from schemas import UserSchema, VehicleSchema, SpotSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError

spot_router = APIRouter(prefix='/spot',tags=['spot'])

@spot_router.get('/')
async def home():
    '''
    Rota de vagas
    '''
    return {'sucesso':'Rota de vagas'}

@spot_router.post('/register_spot')
async def register_spot(spot_schema: SpotSchema,
                        session: Session = Depends(get_session)):
        new_spot = ParkingSpots(spot_schema.is_occupied, spot_schema.price, spot_schema.vehicle_id)
        session.add(new_spot)
        session.commit() 
        return {'mensagem': f'Vaga cadastrada'}


