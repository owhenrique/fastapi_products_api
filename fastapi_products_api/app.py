from fastapi import FastAPI

from fastapi_products_api.routers import products
from fastapi_products_api.schemas.message import ResponseMessage

app = FastAPI()

app.include_router(products.router)


@app.get('/', response_model=ResponseMessage)
def read_index():
    return {'message': 'Products API v0.0.1'}
