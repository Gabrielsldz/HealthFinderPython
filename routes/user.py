from fastapi import HTTPException, Depends, Request, BackgroundTasks
from fastapi import APIRouter
import jwt
from prisma.errors import UniqueViolationError
from prismadb import prisma
from models.user import User
from utils.encrypt_pass import encrypt_password, check_password
from fastapi.security import OAuth2PasswordRequestForm
from utils.access_token import create_access_token, validate_token
from datetime import timedelta
from utils.database.updatedb import update_database

router = APIRouter(prefix = '/user')

@router.post('/register')
async def register(user: User):
    try:
        user.password = encrypt_password(user.password)
        await prisma.user.create(data = user.model_dump())
    except UniqueViolationError:
        raise HTTPException(status_code = 400, detail = 'Email already exists')
    except Exception as e:
        raise HTTPException(status_code = 500, detail = 'Internal server error')
    return {'message': 'User registered'}

@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await prisma.user.find_first(where = {'email': form_data.username})
    if not user:
        raise HTTPException(status_code = 400, detail = 'Invalid credentials')
    if not check_password(user.password, form_data.password):
        raise HTTPException(status_code = 400, detail = 'Invalid credentials')
    access_token = create_access_token(data = {'sub': user.id}, expires_delta = timedelta(minutes = 30))
    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/delete_user')
async def delete_user(request: Request):
    token = validate_token(request.headers)
    print(token)
    if not token:
        raise HTTPException(status_code = 401, detail = 'Invalid token')
    user_id = jwt.decode(token, "secret_key", algorithms = ['HS256'])['sub']
    await prisma.user.delete(where = {'id': user_id})
    return {'message': 'User deleted'}

@router.get('/get_user_data')
async def get_user_data(request: Request):
    token = validate_token(request.headers)
    if not token:
        raise HTTPException(status_code = 401, detail = 'Invalid token')
    user_id = jwt.decode(token, "secret_key", algorithms = ['HS256'])['sub']
    user = await prisma.user.find_first(where = {'id': user_id})
    return {'name': user.name, 'email': user.email}

@router.post('/update_user')
async def update_user(request: Request):
    token = validate_token(request.headers)
    if not token:
        raise HTTPException(status_code=401, detail='Invalid token')
    user_id = jwt.decode(token, "secret_key", algorithms=['HS256'])['sub']

    current_user = await prisma.user.find_first(where={'id': user_id})
    if not current_user:
        raise HTTPException(status_code=404, detail='User not found')

    update_data = await request.json()

    if 'password' in update_data and update_data['password']:
        update_data['password'] = encrypt_password(update_data['password'])

    update_data = {
        'name': update_data.get('name', current_user.name),
        'email': update_data.get('email', current_user.email),
        'password': update_data.get('password', current_user.password)
    }
    print(current_user)
    await prisma.user.update(where={'id': user_id}, data=update_data)

    return {'message': 'User updated'}

@router.post('/reset_and_update_database')
async def reset_and_update_database(request: Request, background_tasks: BackgroundTasks):
    async def update_and_reset():
        await update_database(request)

    background_tasks.add_task(update_and_reset)
    return {'message': 'Database reset and update started'}

@router.get('/is_updating_database')
async def get_is_updating_database(request: Request):
    return {'is_updating_database': request.app.state.is_updating_database}

@router.post('/validate_access_token')
async def validate_token_endpoint(request: Request):
    try:
        # Utilize o validate_token corretamente
        token = validate_token(request.headers)
        if not token:
            raise HTTPException(status_code=401, detail='Invalid token')

        # Decodifica o token JWT
        payload = jwt.decode(token, "secret_key", algorithms=['HS256'])
        user_id = payload['sub']

        # Procura o usuário no banco de dados
        user = await prisma.user.find_first(where={'id': user_id})

        if not user:
            raise HTTPException(status_code=401, detail='User not found')

        # Retorna o usuário ou uma confirmação de que o token é válido
        return {"message": "Valid token"}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Expired token')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')

