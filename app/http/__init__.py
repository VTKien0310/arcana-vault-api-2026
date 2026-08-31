from app.http.key_router import router as key_router
from app.http.item_router import router as item_router


router_registry = [key_router, item_router]
