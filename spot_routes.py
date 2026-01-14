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
    '''
    Cadastra uma nova vaga no sistema.
    
    type: Tipo de vaga (moto ou carro)
    price: Preço por hora da vaga
    '''   
    
    if spot_schema.type not in ['moto','carro']:
        raise HTTPException (status_code=400, detail='Definir o tipo de veiculo para moto ou carro')
    else:
        new_spot = ParkingSpots(type=spot_schema.type, 
                                price=spot_schema.price)
        session.add(new_spot)
        session.commit() 
        return {'mensagem': f'Vaga cadastrada'}


