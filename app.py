import json
import os
from fastapi import FastAPI, Request
from uvicorn import Config, Server
from pydantic import BaseModel
from typing import Optional
PORT = os.environ.get('PORT') or "8000"
app = FastAPI()

@app.get('/')
def app_get(name=None):
    if name:
        return f'Hello {name}!'
    else:
        return 'Hello World!'

@app.get('/clientes')
def app_clientes_get():
    return ['Mathias', 'José', 'Thiago']

@app.get('/produto')
def app_produto_get():
    return ['P1', 'P2', 'P3']

@app.post('/')
def app_post():
    return 'Hello Post!'


@app.post('/resolver')
async def app_resolver_get(request: Request):
    #name = json.loads(json.dumps(request)).get('arguments').get('nome')
    return request.json()
    if name == 'jenilson':
        return 'https://jenilsonramos-sd-20211.herokuapp.com/'
    elif name == 'hiago':
        return 'https://sd-api-uesc.herokuapp.com/'
    elif name == 'guilherme':
        return 'https://nodejs-sd-guilhermesenna.herokuapp.com/'
    elif name == 'joao':
        return 'https://sd-joaopedrop-20212.herokuapp.com/'
    elif name == 'luis':
        return 'https://sd-20212-luiscarlos.herokuapp.com/ '
    elif name == 'robert':
        return 'https://pratica-sd.herokuapp.com/'
    elif name == 'allana':
        return 'https://sd-ascampos-20212.herokuapp.com'
    if name == 'emmanuel':
        return 'https://sd-emmanuel.herokuapp.com/'

def main():
    config = Config(app=app, host='0.0.0.0', port=int(PORT), debug=True)
    server = Server(config=config)
    server.run()


if __name__ == '__main__':
    main()
