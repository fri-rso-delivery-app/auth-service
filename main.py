import uvicorn
import os


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

if __name__ == "__main__":
    if not os.path.exists('./data'):
        os.makedirs('./data')

    uvicorn.run("app.app:app", host="0.0.0.0", port=8080, reload=True, log_level="info")
