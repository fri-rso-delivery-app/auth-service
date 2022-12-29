import uvicorn
import os


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

from app.config import Settings, get_settings

settings: Settings = get_settings()

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=settings.api_http_port, reload=True, log_level="info")
