import os, uuid, requests, time, asyncio
from fastapi import FastAPI, Response, HTTPException
from typing import Optional
from uvicorn import Config, Server
from datetime import datetime, timedelta
from fastapi.responses import HTMLResponse
from models import Aluno, Peer, Information, Recurso, Codigo, Validade, Coordenador, Coordenador_eleito, Requisicao
from servidores import servers

PORT = os.environ.get('PORT') or "8000"
app = FastAPI()

info = Information(server_name='sd-ascampos-20212',
                   server_endpoint='https://sd-ascampos-20212.herokuapp.com/',
                   descricao='Projeto de SD. Os seguintes serviços estão implementados: request, info e peers',
                   versao='0.1',
                   status='online',
                   tipo_de_eleicao_ativa='anel')
recurso = Recurso(codigo_de_acesso="", valor=0)
validade = Validade(validade=datetime.now() - timedelta(days=+1))

coordenador = Coordenador(coordenador=False,
                          coordenador_atual=0)
eleicoes = []


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


@app.get('/coordenador', status_code=200)
def app_coordenador_get():
    return coordenador.dict()


@app.get('/eleicao', status_code=200)
def app_eleicao_get():
    return {"tipo_de_eleicao_ativa": info.tipo_de_eleicao_ativa,
            "eleicoes_em_andamento": eleicoes}


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
async def app_resolver_post(aluno: Aluno):
    name = aluno.arguments.nome
    for i in range(len(servers)):
        if servers[i].nome == name:
            return servers[i].url


@app.post('/recurso', status_code=200)
def app_recurso_post(cod: Optional[Codigo] = None):
    if validade.validade < datetime.now():
        if cod:
            if cod.codigo_de_acesso == recurso.codigo_de_acesso:
                return {"codigo_de_acesso": recurso.codigo_de_acesso, "validade": validade.validade}
            else:
                return HTMLResponse(content="Conflict", status_code=409)
        else:
            recurso.codigo_de_acesso = str(uuid.uuid4())
            validade.validade = datetime.now() + timedelta(seconds=+10)
            return {"codigo_de_acesso": recurso.codigo_de_acesso, "validade": validade.validade}
    else:
        return HTMLResponse(content="Conflict", status_code=409)


@app.post('/eleicao', status_code=200)
async def app_eleicao_post(req: Requisicao):
    eleicoes.append(req.id)
    if info.tipo_de_eleicao_ativa == 'anel':
        a = ring(req)
        return a
    else:
        bully(req)
        return 'valentao'


@app.post('/eleicao/coordenador', status_code=200)
def app_eleicao_coordenador_post(coord: Coordenador_eleito):
    eleicoes.remove(coord.id_eleicao)
    if coord.coordenador == 201720295:
        coordenador.coordenador = True
    else:
        coordenador.coordenador = False
    coordenador.coordenador_atual = coord.coordenador


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
def app_peers_put(id: str, peer: Peer, response: Response):
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
        validade.validade = datetime.now() - timedelta(days=+1)
    else:
        response.status_code = 410


def ring(req: Requisicao):
    coord = Coordenador_eleito(coordenador=0, id_eleicao=req.id)
    new_req = Requisicao(id = req.id, dados = req.dados)
    if req.dados.__contains__("201720295"):
        for id in req.dados:
            if int(id) > coord.coordenador:
                coord.coordenador = int(id)
        for i in servers:
            if i.id != '201720295':
                requests.post(i.url + "eleicao/coordenador", json=coord.dict())
        coordenador.coordenador_atual = coord.coordenador
        if coordenador.coordenador_atual == 201720295:
            coordenador.coordenador = True

    else:
        new_req.dados.append("201720295")
        tentativa = True
        indice = 9
        while (tentativa):
            r = requests.post(servers[indice].url + "eleicao", json=req.dict())
            if r.status_code == 200:
                tentativa = False
            else:
                if indice < len(servers) - 1:
                    indice += 1
                else:
                    indice = 0

def bully(req: Requisicao):
    maior = 0
    for i in servers:
        r = requests.post(i.url + "eleicao", json=req.dict())
        if r.status_code == 200 and int(i.id) > 201720295:
            maior = 1
            break
    if maior == 0:
        coord = Coordenador_eleito(coordenador=201720295, id_eleicao=req.id)
        for i in servers:
            requests.post(i.url + "eleicao/coordenador", json=coord.dict())


async def verify_event():
    reqInit = Requisicao(id=str(uuid.uuid4()), dados=[])
    while(True):
        for i in servers:
            if i.id == str(coordenador.coordenador_atual):
                r = requests.get(i.url + "info")
                if r.text.split('"status":')[1].split(',')[0].strip('"') == 'offline':
                    time.sleep(5)
                    r = requests.get(i.url + "info")
                    if r.text.split('"status":')[1].split(',')[0].strip('"') == 'offline':
                        reqInit.id = str(uuid.uuid4())
                        requests.post(servers[8] + "eleicao", json=reqInit.dict())
                    else:
                        break
                else:
                    break
        time.sleep(2)



async def coordenador_inicial():
    reqinit = Requisicao(id=str(uuid.uuid4()), dados=[""])
    eleicoes.append(reqinit.id)
    if info.tipo_de_eleicao_ativa == 'anel':
        ring(reqinit)
    else:
        bully(reqinit)



def main():
    loop = asyncio.new_event_loop()
    config = Config(app=app, host='0.0.0.0', port=int(PORT), debug=True)
    server = Server(config=config)
    loop.create_task(server.serve())
    loop.create_task(coordenador_inicial())
    loop.create_task(verify_event())
    loop.run_forever()



if __name__ == '__main__':
    main()
