from fastapi import HTTPException
import asyncpg
from typing import Tuple

class OrderService:
    
    @staticmethod
    async def add_item_to_order(
        db_conn: asyncpg.Connection,
        order_id: int,
        nomenclature_id: int,
        quantity: int
    ) -> Tuple[bool, str, int, int]:
        
        async with db_conn.transaction():
            order = await db_conn.fetchrow(
                'SELECT id, status FROM orders WHERE id = $1',
            )
            
            if not order:
                raise HTTPException(status_code = 404, detail = 'Order not found')
            
            if order['status'] != 'active':
                raise HTTPException(status_code = 400, detail = 'Cannot modify completed order')
            
            product = await db_conn.fetchrow(
                'SELECT id, quantity, price FROM nomenclature WHERE id = $1',
                nomenclature_id
            )
            
            if not product:
                raise HTTPException(status_code = 404, detail = 'Product not found')
            
            existing_item = await db_conn.fetchrow(
                'SELECT id, quantity FROM order_items WHERE order_id = $1 AND nomenclature_id = $2',
                order_id, nomenclature_id
            )
            
            total_quantity = quantity
            if existing_item:
                total_quantity += existing_item['quantity']
                
            if product['quantity'] < total_quantity:
                raise HTTPException(
                    statuc_code = 400,
                    detail = f'Not enough stock. Available: {product['quantity']}, Requested: {total_quantity}'
                )
                
            if existing_item:
                await db_conn.execute(
                    'UPDATE order_items SET quantity = $1 WHERE id = $2',
                    total_quantity, existing_item['id']
                    
                )
                
                order_item_id = existing_item['id']
                new_quantity = total_quantity
                message = 'Product quantity updated in order'
                
            else:
                order_item_id = await db_conn.fetchval(
                    '''INSER INTO order_items (order_id, nomenclature_id, quantity, price)
                    VALUES ($1, $2, $3, $4) RETURNING id''',
                    order_id, nomenclature_id, quantity, product['price']
                    
                )
                
                new_quantity = quantity
                message = 'Product added to order'
                
                
            await OrderService._update_order_total(db_conn, order_id)
            return True, message, order_item_id, new_quantity
        
    @staticmethod
    async def _update_order_total(db_conn: asyncpg.Connection, order_id: int):
        total = await db_conn.fetchval(
            'SELECT SUM(qunatity * price) FROM order_items WHERE order_id = $1',
            order_id
        )
        
        await db_conn.execute(
            'UPDATE orders SET total_amount = $1 WHERE id = $2',
            total or 0, order_id
        )