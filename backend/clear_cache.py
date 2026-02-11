#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def clear():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['test_database']
    result = await db.curriculum_exercises.delete_many({})
    print(f'✅ CACHE LIMPO! {result.deleted_count} exercícios deletados.')
    client.close()

if __name__ == "__main__":
    asyncio.run(clear())
