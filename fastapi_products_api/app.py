from fastapi import FastAPI

from fastapi_products_api.routers import auth, inventory, products, users
from fastapi_products_api.schemas.message import ResponseMessage

app = FastAPI()

app.include_router(products.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(inventory.router)


@app.get('/', response_model=ResponseMessage)
def read_index():
    return {'message': 'Products API v0.0.1'}
