import os
from fastapi import FastAPI
from uvicorn import Config, Server
PORT = os.environ.get('PORT') or "8000"
app = FastAPI()


@app.get('/')
def app_get(name=None):
    if name:
        return f'Hello {name}!'
    else:
        return 'Hello World!'




def main():
    config = Config(app=app, host='0.0.0.0', port=int(PORT), debug=True)
    server = Server(config=config)
    server.run()


if __name__ == '__main__':
    main()
