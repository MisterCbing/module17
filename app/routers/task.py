from fastapi import APIRouter

router = APIRouter(prefix='/task', tags=['task'])

@router.get('/')
async def all_tasks():
    pass

@router.get('/task_id')
async def task_by_id():
    pass

@router.post('/create')
async def create_task():
    pass

@router.post('/update')
async def update_task():
    pass

@router.post('/delete')
async def delete_task():
    pass

