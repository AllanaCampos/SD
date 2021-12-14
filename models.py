from pydantic import BaseModel
from datetime import datetime

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
    valor: int


class Codigo(BaseModel):
    codigo_de_acesso: str

class Validade(BaseModel):
    validade: datetime

class Coordenador(BaseModel):
    coordenador: bool
    coordenador_atual: str

class Coordenador_eleito(BaseModel):
    coordenador: str
    id_eleicao: str

class Requisicao(BaseModel):
    id: str
    dados: list