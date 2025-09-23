from typing import List, Optional

from fastapi import APIRouter, Cookie, Form, Header, Response
from fastapi.responses import HTMLResponse, PlainTextResponse

router = APIRouter(
    prefix="/product",
    tags=["product"],
)

products = ["watch", "camera", "phone"]


@router.post("/new")
def create_product(name: str = Form(...)):
    products.append(name)
    return products


@router.get("/")
def get_all_products():
    data = " ".join(products)
    response = Response(
        content=data,
        media_type="text/plain",
    )
    response.set_cookie(key="test_cookie", value="test_cookie_value")
    return response


@router.get(
    "/{id}",
    responses={
        200: {
            "content": {
                "text/html": {"example": "<div>Product</div>"},
            },
            "description": "Returns HTML for an object",
        },
        404: {
            "content": {
                "text/plain": {"example": "Product not found"},
            },
            "description": "plaintext error",
        },
    },
)
def get_product(id: int):
    product = products[id]
    if id > len(product):
        out = "product not available"
        return PlainTextResponse(content=out, media_type="text/plain", status_code=404)
    else:
        out = f"""
        <head>
            <style>
            .product{{
                width: 500px;
                height: 20px;
                border: 2px inset green;
                background-color: lightblue;
                text-align: center 
            }}
            </style>
        </head>
        <div class="product">{product}</div>
        """
        return HTMLResponse(content=out, media_type="text/html")


@router.get("withheader")
def get_products(
    response: Response,
    custom_header: Optional[List[str]] = Header(None),
    test_cookie: Optional[str] = Cookie(None),
):
    if custom_header:
        response.headers["custom_response_header"] = " and ".join(custom_header)
    return {
        "data": products,
        "custom_header": custom_header,
        "test_cookie": test_cookie,
    }
