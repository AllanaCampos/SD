import os
from fastapi import FastAPI, Response, HTTPException
from uvicorn import Config, Server
from pydantic import BaseModel
from datetime import datetime, timedelta
import uuid
PORT = os.environ.get('PORT') or "8000"
app = FastAPI()
servers = []
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
    status: str
    tipo_de_eleicao_ativa: str


class Recurso(BaseModel):
    codigo_de_acesso: str
    valor: str


class Codigo(BaseModel):
    codigo_de_acesso: str

class Validade(BaseModel):
    validade: datetime

info = Information(server_name='sd-ascampos-20212',
                   server_endpoint='https://sd-ascampos-20212.herokuapp.com/',
                   descricao='Projeto de SD. Os seguintes serviços estão implementados: request, info e peers',
                   versao='0.1',
                   status='online',
                   tipo_de_eleicao_ativa='ring')
recurso = Recurso(codigo_de_acesso = "", valor = "")
validade = Validade(validade = datetime.now() - timedelta(days=+1))
p0 = Peer(
    id=  "201720295",
    nome= "allana",
    url= "https://sd-ascampos-20212.herokuapp.com/"
  )
p1 = Peer(
    id=  "201512136",
    nome= "annya",
    url= "https://sd-annyaourives-20212.herokuapp.com/hello"
  )
p2 = Peer(
    id=  "201710375",
    nome= "emmanuel",
    url="https://sd-emmanuel.herokuapp.com/"
  )
p3 = Peer(
    id=  "201710376",
    nome= "guilherme",
    url= "https://nodejs-sd-guilhermesenna.herokuapp.com/"
  )

p4 = Peer(
    id= "201710377",
    nome= "hiago",
    url= "https://sd-api-uesc.herokuapp.com/"
  )
p5 = Peer(
    id= "201810665",
    nome= "jenilson",
    url= "https://jenilsonramos-sd-20211.herokuapp.com/"
  )
p6 = Peer(
    id="201610327",
    nome= "joao",
    url= "https://sd-joaopedrop-20212.herokuapp.com/"
  )
p7 = Peer(
    id= "201610337",
    nome= "luis",
    url= "https://sd-20212-luiscarlos.herokuapp.com/"
  )
p8 = Peer(
    id= "201620400",
    nome= "nassim",
    url= "https://sd-nassimrihan-2021-2.herokuapp.com/"
  )
p9 = Peer(
    id=  "201710396",
    nome= "robert",
    url= "https://pratica-sd.herokuapp.com/"
  )
p10 = Peer(
    id=  "201720308",
    nome= "victor",
    url= "https://sd-victor-20212.herokuapp.com/"
  )
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




@app.get('/')
def app_get(name=None):
    if name:
        return f'Hello {name}!'
    else:
        return 'Hello World!'


@app.get('/info', status_code=200)
def app_info_get():
    return info

@app.get('/peers')
def app_peers_get():
    return servers

@app.get('/peers/{id}', status_code=200)
def app_peers_get(id: str, response: Response):
    for i in range(len(servers)):
        if servers[i].id == id:
            return servers[i]
    response.status_code = 404
    return HTTPException(status_code=404, detail="Item not found")


@app.get('/recurso', status_code=200)
def app_recurso_get(cod: Codigo, response: Response):
    if recurso.codigo_de_acesso == cod.codigo_de_acesso and validade.validade > datetime.now():
        return {'valor': recurso.valor}
    else:
        response.status_code = 401

@app.post('/reset')
def app_reset_post():
    servers = []
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

@app.post('/')
def app_post():
    return 'Hello Post!'

@app.post('/peers', status_code=200)
def app_peers_post(peer: Peer, response: Response):
    for i in range(len(servers)):
        if servers[i].dict().get('id') == peer.id:
            response.status_code = 409
            return HTTPException(status_code=409, detail="Conflict")
        elif servers[i].dict().get('nome') == peer.nome:
            response.status_code = 409
            return HTTPException(status_code=409, detail="Conflict")
    if (not peer.nome.isdigit()) and (len(peer.url.split('.')) > 1):
        servers.append(peer)
    else:
        response.status_code = 400
        return HTTPException(status_code=400, detail="Bad Request")



@app.post('/resolver')
async def app_resolver_get(aluno: Aluno):
    name = aluno.arguments.nome
    for i in range(len(servers)):
        if servers[i].nome == name:
            return servers[i].url

@app.post('/recurso', status_code=200)
def app_recurso_post(response: Response):
    if validade.validade < datetime.now():
        recurso.codigo_de_acesso = str(uuid.uuid4())
        validade.validade = datetime.now()+timedelta(seconds=+10)
        return {"codigo_de_acesso": recurso.codigo_de_acesso, "validade": validade.validade}
    else:
        response.status_code = 409

@app.put('/info', status_code=200)
def app_info_put(inform: Information, response: Response):
    try:
        info.server_name = inform.server_name
        info.server_endpoint = inform.server_endpoint
        info.Status = inform.status
        info.versao = inform.versao
        info.descricao = inform.descricao
        info.tipo_de_eleicao_ativa = inform.tipo_de_eleicao_ativa
    except:
        response.status_code = 400
        HTTPException(status_code=400, detail="Bad Request")

@app.put('/peers/{id}', status_code=200)
def app_peers_put(id:str, peer: Peer, response: Response):
    if type(peer.id) == str and type(peer.nome) == str and type(peer.url) == str:
        for i in range(len(servers)):
            if servers[i].dict().get('id') == id:
                servers[i] = peer
                return servers[i].dict()
    else:
        response.status_code = 400
        return HTTPException(status_code=400, detail="Bad Request")
    response.status_code = 400
    return HTTPException(status_code=404, detail="Not Found")

@app.put('/recurso', status_code=200)
def app_recurso_put(rec: Recurso, response: Response):
    if recurso.codigo_de_acesso == rec.codigo_de_acesso and validade.validade > datetime.now():
        recurso.codigo_de_acesso = rec.codigo_de_acesso
        recurso.valor = rec.valor
        return recurso
    else:
        response.status_code = 401
        return recurso.codigo_de_acesso == rec.codigo_de_acesso


@app.delete('/peers/{id}', status_code=200)
def app_peers_delete(id: str, response: Response):
    for i in range(len(servers)):
        if servers[i].id == id:
            servers.__delitem__(i)
            return "Peer deletado"
    response.status_code = 404
    return HTTPException(status_code=404, detail="Not Found")

@app.delete('/recurso', status_code=200)
def app_recurso_delete(cod: Codigo, response: Response):
    if recurso.codigo_de_acesso == cod.codigo_de_acesso and validade.validade > datetime.now():
        recurso.codigo_de_acesso = ""
        validade.validade = datetime.now()-timedelta(hours=+30)
    else:
        response.status_code = 410
def main():
    config = Config(app=app, host='0.0.0.0', port=int(PORT), debug=True)
    server = Server(config=config)
    server.run()


if __name__ == '__main__':
    main()
