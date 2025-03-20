from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, BeanieObjectId


from main import Product


app = FastAPI(docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json", root_path="/api")

client = AsyncIOMotorClient("mongodb://mongo:27017")


@app.get("/")
async def get_all():
    await init_beanie(database=client["test"], document_models=[Product])
    data = await Product.find({}).to_list()
    return data

@app.get("/{id}")
async def get_by_id(id: str):
    await init_beanie(database=client["test"], document_models=[Product])
    data = await Product.find_one(Product.id == BeanieObjectId(id))
    return data
