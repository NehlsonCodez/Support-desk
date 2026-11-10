import asyncio
import sys
import os
from pathlib import Path

# Add backend/app directory to sys.path and set CWD for .env loading
app_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(app_dir))
os.chdir(app_dir)

from sqlalchemy import select
from database import AsyncSessionLocal
from models import User
from schemas import UserRole


async def promote_user(email: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if not user:
            print(f"Error: User with email '{email}' not found.")
            return

        user.role = UserRole.ADMIN
        await session.commit()
        print(f"Success: {user.full_name} ({user.email}) is now an ADMIN.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python promote_admin.py user@example.com")
        sys.exit(1)
        
    asyncio.run(promote_user(sys.argv[1]))