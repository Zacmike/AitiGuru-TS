import asyncpg
from typing import AsyncGenerator
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@127.0.0.1/ecommerce')

class Database:
    def __init__(self):
        self.pool = None
        
    async def connect(self):
        self.pool = await asyncpg.create_pool(DATABASE_URL)
        
    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            
    async def get_connection(self):
        async with self.pool.acquire() as connection:
            yield connection
    
db = Database()