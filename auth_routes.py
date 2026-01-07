from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import sessionmaker
from models import User
from dependencies import get_session, verify_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix='/auth',tags=['auth'])

def create_token(id_user, token_duration = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + token_duration
    dic_info = {'sub': str(id_user), 'exp': expiration_date}
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt



def authenticate_user (email, password, session):
    usuario = session.query(User).filter(User.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(password, usuario.password):
        return False
    return usuario


@auth_router.get('/')
async def home():
    '''
    Rota padrão de autenticação
    '''
    return {'Autenticar':'Rota de Autenticação'}

@auth_router.post('/create_user')
async def create_user(user_schema: UserSchema, 
                      session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email==user_schema.email).first()

    if user:
        raise HTTPException (status_code=400, detail='E-mail já cadastrado')
    else:
        password_cript = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, 
                        password_cript, user_schema.admin)
        session.add(new_user)
        session.commit() 
        return {'mensagem': f'usuário cadastrado {user_schema.email}'}
    
    #ativar o create_adm_user após a criação de um usuario adm
'''@auth_router.post('/create_adm_user')
async def create_adm_user(user_adm_schema: UserAdmSchema, 
                      session: Session = Depends(get_session),
                      user_adm: User = Depends(verify_token)):
    user = session.query(User).filter(User.email==user_adm_schema.email).first()

    if user:
        raise HTTPException (status_code=400, detail='E-mail já cadastrado')
    elif user_adm_schema.admin and not user_adm.admin:
        raise HTTPException (status_code=401, detail='Você não tem autorização para fazer essa modificação')
    else:    
        password_cript = bcrypt_context.hash(user_adm_schema.password)
        new_user = User(user_adm_schema.name, user_adm_schema.email, 
                        password_cript, user_adm_schema.admin)
        session.add(new_user)
        session.commit() 
        return {'mensagem': f'usuário cadastrado {user_adm_schema.email}'}'''
    
@auth_router.post('/login')
async def login (login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = authenticate_user(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException (status_code=400, detail= 'Usuário não encontrado ou informações de login incorretas')
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, token_duration= timedelta(days=7))
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer'
            }

@auth_router.post('/login-form')
async def login_form (form_data : OAuth2PasswordRequestForm = Depends(), 
                 session: Session = Depends(get_session)):
    user = authenticate_user(form_data.username, form_data.password, session)

    if not user:
        raise HTTPException (status_code=400, 
                             detail= 'Usuário não encontrado ou informações de login incorretas')
    else:
        access_token = create_token(user.id)
        return {
            'access_token': access_token,
            'token_type': 'Bearer'
            }            
    
@auth_router.get ('/refresh')
async def use_refresh_token(user: User = Depends(verify_token)):
    
    access_token = create_token(user.id)
    return {
        'access_token': access_token,
        'token_type': 'Bearer'
        }