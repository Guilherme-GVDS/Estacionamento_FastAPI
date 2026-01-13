from sqlalchemy import create_engine , Column, DateTime, String, Integer, Float, Boolean, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

#Criar conexão
db = create_engine('sqlite:///banco.db')

#Criar base DB  
Base = declarative_base()

#Tabelas DB



class User (Base):
    __tablename__ = 'Users'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, nullable=False)
    email = Column('email', String, nullable=False)
    password = Column('password', String, nullable=False)
    admin = Column ('admin', Boolean, nullable=False, default=False)

    def __init__(self, name, email, password, admin):
        self.name = name
        self.email = email
        self.password = password
        self.admin = admin


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    plate = Column('plate',String, nullable= False, unique=True)
    type = Column('type', Enum('carro', 'moto', name='vehicle_type'), nullable= False)
    phone_number = Column('phone_number', String, nullable= False)
    email = Column('email', String, nullable= False)
    
    def __init__ (self, plate, type, phone_number, email):
        self.plate = plate
        self.type = type
        self.phone_number = phone_number
        self.email = email

        
class ParkingSpots(Base):
    __tablename__ = 'parking_spots'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    is_occupied = Column('is_occupied', Boolean, nullable= False, default=False)
    price = Column('price', Float, nullable = False)
    vehicle_id = Column('vehicle_id', ForeignKey('vehicles.id'), nullable= True)

    def __init__ (self, is_occupied, price, vehicle_id):
        self.is_occupied = is_occupied
        self.price = price
        self.vehicle_id = vehicle_id


class ParkingRecords(Base):
    __tablename__ = 'parking_records'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    parking_spot_id = Column('parking_spot_id', ForeignKey('parking_spots.id'), nullable= False)
    vehicle_id = Column('vehicle_id', ForeignKey('vehicles.id'), nullable= False)
    entry_time = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("America/Sao_Paulo")),
        nullable=False
    )
    exit_time = Column(DateTime(timezone=True), nullable=True)
    '''calculo do exit_time
    record.exit_time = datetime.now(ZoneInfo("America/Sao_Paulo"))
    delta = record.exit_time - record.entry_time
    total_minutes = delta.total_seconds() / 60
    total_hours = total_minutes / 60'''
    price = Column('price', Float, nullable= True)
    paid = Column('paid', Boolean, nullable= False)
    

    def __init__ (self, parking_spot_id, vehicle_id, entry_time, exit_time, price, paid):
        self.parking_spot_id = parking_spot_id
        self.vehicle_id = vehicle_id
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.price = price
        self.paid = paid