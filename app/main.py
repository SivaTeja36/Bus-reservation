import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes import setup_routes
from app.utils.life_cycle_handler import setup_event_handlers
from app.utils.middlewares import setup_middlewares

app = FastAPI()

build_dir = os.path.abspath("frontend")
app.mount("/frontend", StaticFiles(directory=os.path.join(build_dir)), name="frontend")

setup_routes(app)
setup_middlewares(app)
setup_event_handlers(app)

@app.get("/", include_in_schema=False)
async def serve_root():
    return FileResponse(os.path.join(build_dir, "index.html"))

# Catch-all route to serve index.html for all other paths (for React routing)
@app.get("/{path_name:path}", include_in_schema=False)
async def serve_react_app(path_name: str):
    file_path = os.path.join(build_dir, path_name)
    
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return FileResponse(os.path.join(build_dir, "index.html"))