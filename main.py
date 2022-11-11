import uvicorn
import os


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

from app import config

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=config.http_port, reload=True, log_level="info")
