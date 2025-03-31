import asyncpg
import asyncio


async def test_connection():
    try:
        conn = await asyncpg.connect(
            user="local_user",
            password="new_password_123",
            database="local_token_db",
            host="localhost",
            port=5432,
        )
        print("✅ Успешное подключение!")
        await conn.close()
    except Exception as e:
        print(f"❌ Ошибка: {e}")


asyncio.run(test_connection())
