from fastapi import APIRouter, Depends, HTTPException
from models import Vehicle, ParkingSpots, ParkingRecords
from dependencies import get_session, verify_token, ensure_timezone
from schemas import UserSchema, VehicleSchema, SpotSchema, ParkingRecordCheckout
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


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
    
@park_router.post('/park')
async def park_vehicle(vehicle_plate, session: Session = Depends(get_session)):
    vehicle = session.query(Vehicle).filter(Vehicle.plate == vehicle_plate).first()
    if not vehicle:
        raise HTTPException(status_code=400, detail='Veiculo não encontrado')
    else:
        spot = session.query(ParkingSpots).filter(ParkingSpots.is_occupied == False).first()
        if not spot:
            raise HTTPException(status_code=404, detail='Nenhuma vaga disponível')
        spot.is_occupied = True
        spot.vehicle_id = vehicle.id

        park = ParkingRecords(parking_spot_id=spot.id, vehicle_id=vehicle.id)
        session.add(park)

        session.commit()
        return {'mensagem': f'Vaga atualizada'}
    

@park_router.post('/checkout')
async def checkout_vehicle(vehicle_plate, session: Session = Depends(get_session)):
    vehicle = session.query(Vehicle).filter(Vehicle.plate == vehicle_plate).first()
    parking_record = session.query(ParkingRecords).filter(
        ParkingRecords.vehicle_id == vehicle.id,
        ParkingRecords.paid == False).first()

    
    if not parking_record:
        raise HTTPException(status_code=404, detail=(f'Veículo não está estacionado ou checkout já foi realizado'))
    else:

        #Checkout
        entry_time = ensure_timezone(parking_record.entry_time)
        parking_record.exit_time = datetime.now(ZoneInfo("America/Sao_Paulo"))
        delta = parking_record.exit_time - entry_time
        total_hours = delta.total_seconds() / 3600
        parking_record.price = round(total_hours * float(spot.price), 2)
        parking_record.paid = True

        #Liberação da Vaga
        spot = session.query(ParkingSpots).filter(ParkingSpots.id == parking_record.parking_spot_id).first()
        spot.is_occupied = False
        spot.vehicle_id = None
        
        session.commit()
        session.refresh(parking_record)
        return {
            'mensagem': 'Checkout realizado com sucesso',
            'placa': vehicle_plate,
            'vaga': spot.id,
            'tempo_horas': round(total_hours, 2),
            'preco': float(parking_record.price)
        }