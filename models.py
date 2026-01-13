from sqlalchemy import create_engine , Column, DateTime, String, Integer, Float, Boolean, ForeignKey, Enum, Numeric
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



class ParkingRecords(Base):
    __tablename__ = 'parking_records'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    parking_spot_id = Column('parking_spot_id', ForeignKey('parking_spots.id'), nullable= False)
    vehicle_id = Column('vehicle_id', ForeignKey('vehicles.id'), nullable= False)
    entry_time = Column(
        DateTime,
        default=lambda: datetime.now(),
        nullable=False
    )
    exit_time = Column(DateTime(timezone=True), nullable=True)
    price = Column('price', Numeric(10, 2), nullable= True)
    paid = Column('paid', Boolean, nullable= False, default=False)
    

    '''calculo do exit_time
    record.exit_time = datetime.now(ZoneInfo("America/Sao_Paulo"))
    delta = record.exit_time - record.entry_time
    total_minutes = delta.total_seconds() / 60
    total_hours = total_minutes / 60'''