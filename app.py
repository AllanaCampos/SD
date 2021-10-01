import json
import os
from fastapi import FastAPI, Request
from uvicorn import Config, Server
from pydantic import BaseModel
PORT = os.environ.get('PORT') or "8000"
app = FastAPI()
servers = [
  {
    "id":  "201720295",
    "nome": "allana",
    "url": "https://sd-ascampos-20212.herokuapp.com/"
  },
  {
    "id":  "201512136",
    "nome": "annya",
    "url": "https://sd-annyaourives-20212.herokuapp.com/hello"
  },
  {
    "id":  "201710375",
    "nome": "emmanuel",
    "url": "https://sd-emmanuel.herokuapp.com/"
  },
  {
    "id":  "201710376",
    "nome": "guilherme",
    "url": "https://nodejs-sd-guilhermesenna.herokuapp.com/"
  },
  {
    "id":  "201710377",
    "nome": "hiago",
    "url": "https://sd-api-uesc.herokuapp.com/"
  },
  {
    "id":  "201810665",
    "nome": "jenilson",
    "url": "https://jenilsonramos-sd-20211.herokuapp.com/"
  },
  {
    "id":  "201610327",
    "nome": "joao",
    "url": "https://sd-joaopedrop-20212.herokuapp.com/"
  },
  {
    "id":  "201610337",
    "nome": "luis",
    "url": "https://sd-20212-luiscarlos.herokuapp.com/"
  },
  {
    "id":  "201620400",
    "nome": "nassim",
    "url": "https://sd-nassimrihan-2021-2.herokuapp.com/"
  },
  {
    "id":  "201710396",
    "nome": "robert",
    "url": "https://pratica-sd.herokuapp.com/"
  },
  {
    "id":  "201720308",
    "nome": "victor",
    "url": "https://sd-victor-20212.herokuapp.com/"
  }
]
ids = [[201720295, "allana"],
 [201512136, "annya"],
 [201710375, "emmanuel"],
 [201710376, "guilherme"],
 [201710377, "hiago"],
 [201810665, "jenilson"],
 [201610327, "joao"],
 [201610337, "luis"],
 [201620400, "nassim"],
 [201710396, "robert"],
 [201720308, "victor"]]
urls =["https://sd-ascampos-20212.herokuapp.com/",
       "https://sd-annyaourives-20212.herokuapp.com/hello",
       "https://sd-emmanuel.herokuapp.com/",
       "https://nodejs-sd-guilhermesenna.herokuapp.com/",
       "https://sd-api-uesc.herokuapp.com/",
       "https://jenilsonramos-sd-20211.herokuapp.com/",
       "https://sd-joaopedrop-20212.herokuapp.com/",
       "https://sd-20212-luiscarlos.herokuapp.com/",
       "https://sd-nassimrihan-2021-2.herokuapp.com/",
       "https://pratica-sd.herokuapp.com/",
       "https://sd-victor-20212.herokuapp.com/"]



class Arguments(BaseModel):
    nome: str

class Aluno(BaseModel):
    operacao: str
    arguments: Arguments

class Peer(BaseModel):
    id: str
    nome: str
    url: str

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

@app.get('/info')
def app_info_get():
    info = {
        "server_name": "sd-ascampos-20212",
        "server_endpoint": "https://sd-ascampos-20212.herokuapp.com/",
        "descrição": "Projeto de SD. Os seguintes serviços estão implementados, ... etc",
        "versao": "0.1",
        "Status": "online",
        "tipo_de_eleicao_ativa": ""
    }
    return info

@app.get('/peers')
def app_peers_get(Id = None):
    if Id:
        for i in range(len(servers)):
            if servers[i].__contains__(Id):
                return servers[i]
    else: return servers

@app.post('/')
def app_post():
    return 'Hello Post!'

@app.post('/peers')
def app_post(peer: Peer):
    servers.append({"id": peer.id,
                    "nome": peer.nome,
                    "url": peer.url})

@app.post('/resolver')
async def app_resolver_get(aluno: Aluno):
    name = aluno.arguments.nome
    for i in range(len(ids)):
        if ids[i].__contains__(name):
            return urls[i]

def main():
    config = Config(app=app, host='0.0.0.0', port=int(PORT), debug=True)
    server = Server(config=config)
    server.run()


if __name__ == '__main__':
    main()
