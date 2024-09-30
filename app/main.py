from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.endpoints import cart, user, product
from app.db.session import engine
from app.db.base import Base

app = FastAPI(title="Shopping Cart API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(product.router, prefix="/products", tags=["Product"])
app.include_router(cart.router, prefix="/cart", tags=["Cart"])

# Create database tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
