from fastapi import APIRouter, Depends, HTTPException
from models import Vehicle, ParkingSpots, ParkingRecords
from dependencies import get_session, verify_token, ensure_timezone
from schemas import VehicleSchema
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
    
    '''
    Cadastra um novo veículo no sistema.
    
    plate: Placa do veículo (única)
    type: Tipo do veículo (moto ou carro)
    phone_number: Telefone de contato
    email: Email de contato
    '''
    existing_vehicle = session.query(Vehicle).filter(Vehicle.plate==vehicle_schema.plate).first()

    if existing_vehicle:
        raise HTTPException (status_code=409,
                             detail=f'Veículo com placa {vehicle_schema.plate} já cadastrado')
    elif vehicle_schema.type not in ['moto','carro']:
        raise HTTPException (status_code=400, detail='Definir o tipo de veiculo para moto ou carro')
    else:
        new_vehicle = Vehicle(plate=vehicle_schema.plate, 
                            type=vehicle_schema.type, 
                            phone_number=vehicle_schema.phone_number, 
                            email=vehicle_schema.email)
        session.add(new_vehicle)
        session.commit() 
        return {'mensagem': f'Veiculo cadastrado {vehicle_schema.plate}'}
    

@park_router.post('/park')
async def park_vehicle(vehicle_plate, session: Session = Depends(get_session)):
    '''
    Estaciona um veículo em uma vaga disponível.
    
    vehicle_plate: Placa do veículo a ser estacionado
    '''
    vehicle = session.query(Vehicle).filter(Vehicle.plate == vehicle_plate).first()
    if not vehicle:
        raise HTTPException(status_code=400, 
                            detail=f'Veículo com placa {vehicle_plate} não encontrado')
    else:
        is_parked=session.query(ParkingSpots).filter(ParkingSpots.vehicle_id == vehicle.id).first()
        if is_parked:
            raise HTTPException(status_code=400, detail='Veiculo já estacionado')
        else:
            spot = session.query(ParkingSpots).filter(ParkingSpots.is_occupied == False,
                                                    ParkingSpots.type == vehicle.type).first()
            if not spot:
                raise HTTPException(status_code=404, detail='Nenhuma vaga disponível')
            spot.is_occupied = True
            spot.vehicle_id = vehicle.id

            park_record = ParkingRecords(parking_spot_id=spot.id, vehicle_id=vehicle.id)
            session.add(park_record)

            session.commit()
            return {
                'message': 'Veículo estacionado com sucesso',
                'placa': vehicle_plate,
                'vaga': spot.id,
                'tipo_vaga': spot.type,
                'horario_entrada': park_record.entry_time.isoformat()
            }
    

@park_router.post('/checkout')
async def checkout_vehicle(vehicle_plate, session: Session = Depends(get_session)):
    '''
    Realiza o checkout de um veículo estacionado.
    
    vehicle_plate: Placa do veículo
    
    Calcula o tempo de permanência e o valor a ser pago.
    '''
    vehicle = session.query(Vehicle).filter(Vehicle.plate == vehicle_plate).first()
    if not vehicle:
        raise HTTPException(status_code=404, 
                            detail=f'Veículo com placa {vehicle_plate} não encontrado')
    
    parking_record = session.query(ParkingRecords).filter(
        ParkingRecords.vehicle_id == vehicle.id,
        ParkingRecords.paid == False).first()
    
    if not parking_record:
        raise HTTPException(status_code=404, detail=(f'Veículo não está estacionado ou checkout já foi realizado'))
    

    spot = session.query(ParkingSpots).filter(ParkingSpots.id == parking_record.parking_spot_id).first()
    if not spot:
        raise HTTPException(status_code=404, detail=(f'Vaga não encontrada'))
    
    #Liberação da Vaga
    spot.is_occupied = False
    spot.vehicle_id = None

    # Calcula tempo e valor
    entry_time = ensure_timezone(parking_record.entry_time)
    exit_time = datetime.now(ZoneInfo("America/Sao_Paulo"))
    
    delta = exit_time - entry_time
    total_hours = delta.total_seconds() / 3600
    
    # Considera tempo mínimo de cobrança (ex: mínimo 1 hora)
    minimum_hours = max(total_hours, 1.0)  # Opcional
    
    # Atualiza registro
    parking_record.exit_time = exit_time
    parking_record.price = round(minimum_hours * float(spot.price), 2)
    parking_record.paid = True

    
    
    session.commit()
    session.refresh(parking_record)
    return {
        'mensagem': 'Checkout realizado com sucesso',
        'placa': vehicle_plate,
        'vaga': spot.id,
        'tempo_horas': round(total_hours, 2),
        'horas_cobradas': round(minimum_hours, 2),
        'valor_total': float(parking_record.price)
    }