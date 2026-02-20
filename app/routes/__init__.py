from app.routes.key_router import router as key_router
from app.routes.item_router import router as item_router

router_registry = [key_router, item_router]
