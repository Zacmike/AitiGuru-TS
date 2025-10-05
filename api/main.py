from fastapi import FastAPI, Depends, HTTPException
import asyncpg
from contextlib import asynccontextmanager
from database import db
from models import AddToOrderRequest, AddToOrderResponse, ErrorResponse
from services.order_service import OrderService

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()
    
    
app = FastAPI(
    title = 'AitiGuru API',
    description = 'API для управления заказами и номенклатурой',
    version = '1.0.0',
    lifespan = lifespan
)

@app.post(
    'api/orders/add-item',
    response_model = AddToOrderResponse,
    response = {400: {'model': ErrorResponse}, 404: {'model': ErrorResponse}}
)

async def add_item_to_order(
    request: AddToOrderRequest,
    db_conn: asyncpg.Connection = Depends(db.get_connection)
):
    try:
        success, message, order_item_id, new_quantity = await OrderService.add_item_to_order(
            db_conn, request.order_id, request.nomenclature_id, request.quantity
        )
        
        return AddToOrderResponse(
            success = success,
            message = message,
            order_item_id = order_item_id,
            new_quantity = new_quantity
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f'Внутренняя ошибка сервера: {str(e)}')
    
@app.get('/health')
async def health_check():
    return {'status': 'healthy'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host = '0.0.0.0', port = 8000)