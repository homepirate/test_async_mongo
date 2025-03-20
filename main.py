import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from beanie import Document, Indexed, init_beanie
import random
import string



class Product(Document):
    name: str
    price: Indexed(float)

    class Settings:
        name = "test"


async def example():
    tonybar = Product(name="Tony's", price=5.95,)
    await tonybar.insert()

    product = await Product.find_one(Product.price < 10)

    await product.set({Product.name:"Gold bar"})

async def create_many():
    for i in range(1000):
        name = "".join(random.choice(string.ascii_letters) for _ in range(random.randint(3, 10)))
        await Product(name=name, price=random.randrange(1, 10000)).insert()


async def get_all():
    data = await Product.find({}).to_list()
    print(data)


async def get_gt(price: int = 1000):
    data = await Product.find(Product.price > price).to_list()
    print(len(data))


async def main():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client["test"], document_models=[Product])

    # await example()
    # await create_many()

    await get_all()
    await get_gt(9998)


if __name__ == "__main__":
    asyncio.run(main())
