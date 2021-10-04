import json
import os
from fastapi import FastAPI, Request
from uvicorn import Config, Server
from pydantic import BaseModel
PORT = os.environ.get('PORT') or "8000"
app = FastAPI()
servers = []


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

class Information(BaseModel):
    server_name: str
    server_endpoint: str
    descricao: str
    versao: str
    Status: str
    tipo_de_eleicao_ativa: str

info = Information({"server_name": "sd-ascampos-20212",
                    "server_endpoint": "https://sd-ascampos-20212.herokuapp.com/",
                    "descricao": "Projeto de SD. Os seguintes serviços estão implementados, ... etc",
                    "versao": "0.1",
                    "Status": "online",
                    "tipo_de_eleicao_ativa": ""})
'''p0 = Peer({
    "id":  "201720295",
    "nome": "allana",
    "url": "https://sd-ascampos-20212.herokuapp.com/"
  })
p1 = Peer({
    "id":  "201512136",
    "nome": "annya",
    "url": "https://sd-annyaourives-20212.herokuapp.com/hello"
  })
p2 = Peer({
    "id":  "201710375",
    "nome": "emmanuel",
    "url": "https://sd-emmanuel.herokuapp.com/"
  })
p3 = Peer({
    "id":  "201710376",
    "nome": "guilherme",
    "url": "https://nodejs-sd-guilhermesenna.herokuapp.com/"
  })
p4 = Peer({
    "id":  "201710377",
    "nome": "hiago",
    "url": "https://sd-api-uesc.herokuapp.com/"
  })
p5 = Peer({
    "id":  "201810665",
    "nome": "jenilson",
    "url": "https://jenilsonramos-sd-20211.herokuapp.com/"
  })
p6 = Peer({
    "id":  "201610327",
    "nome": "joao",
    "url": "https://sd-joaopedrop-20212.herokuapp.com/"
  })
p7 = Peer({
    "id":  "201610337",
    "nome": "luis",
    "url": "https://sd-20212-luiscarlos.herokuapp.com/"
  })
p8 = Peer({
    "id":  "201620400",
    "nome": "nassim",
    "url": "https://sd-nassimrihan-2021-2.herokuapp.com/"
  })
p9 = Peer({
    "id":  "201710396",
    "nome": "robert",
    "url": "https://pratica-sd.herokuapp.com/"
  })
p10 = Peer({
    "id":  "201720308",
    "nome": "victor",
    "url": "https://sd-victor-20212.herokuapp.com/"
  })
servers.append(p0)
servers.append(p1)
servers.append(p2)
servers.append(p3)
servers.append(p4)
servers.append(p5)
servers.append(p6)
servers.append(p7)
servers.append(p8)
servers.append(p9)
servers.append(p10)
'''
@app.get('/')
def app_get(name=None):
    if name:
        return f'Hello {name}!'
    else:
        return 'Hello World!'


'''@app.get('/info')
def app_info_get():
    return info

@app.get('/peers')
def app_peers_get(Id = None):
    if Id:
        for i in range(len(servers)):
            if servers[i].id == Id:
                return servers[i]
    else: return servers

@app.post('/')
def app_post():
    return 'Hello Post!'

@app.post('/peers')
def app_peers_post(peer: Peer):
    servers.append(peer)

@app.post('/resolver')
async def app_resolver_get(aluno: Aluno):
    name = aluno.arguments.nome
    for i in range(len(ids)):
        if ids[i].__contains__(name):
            return urls[i]

@app.put('/info', status_code=200)
def app_info_put(inform: Information):
    info.server_name = inform.server_name
    info.server_endpoint = inform.server_endpoint
    info.Status = inform.Status
    info.versao = inform.versao
    info.descricao = inform.descricao
    info.tipo_de_eleicao = inform.tipo_de_eleicao

@app.put('/peers', status_code=200)
def app_peers_put(Id, peer: Peer):
    for i in range(len(servers)):
        if servers[i].id == Id:
            servers[i] = peer
            return "Peer atualizado", servers[i]

@app.delete('/peers', status_code=200)
def app_peers_delete(Id):
    for i in range(len(servers)):
        if servers[i].id == Id:
            servers.__delitem__(i)
            return "Peer deletado"
    return "Peer não encontrado"'''

def main():
    config = Config(app=app, host='0.0.0.0', port=int(PORT), debug=True)
    server = Server(config=config)
    server.run()


if __name__ == '__main__':
    main()
