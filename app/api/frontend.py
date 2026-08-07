from fastapi.responses import FileResponse


def get_frontend():
    return FileResponse("frontend/index.html")