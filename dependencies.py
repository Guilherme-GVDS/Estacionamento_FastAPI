from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from sqlalchemy.orm import sessionmaker, Session
from models import db, User
from jose import jwt, JWTError

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verify_token (token: str = Depends(oauth2_schema), session: Session = Depends(get_session)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = dic_info.get('sub')
    except JWTError:
        raise HTTPException (status_code=401, detail='Acesso Negado, verifique a validade do token')

    user = session.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail='Acesso Inválido')
    return user