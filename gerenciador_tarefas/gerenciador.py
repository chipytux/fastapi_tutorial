from fastapi import FastAPI
from pydantic import BaseModel, constr
from uuid import uuid4, UUID
from enum import Enum

app = FastAPI()

class EstadosPossiveis(str, Enum):
    finalizado: 'finalizado'
    nao_finalizado = 'não finalizado'

class TarefaEntrada(BaseModel):
    titulo: constr(min_length=3, max_length=50)
    descricao: constr(max_length=140)


class Tarefa(TarefaEntrada):
    id: UUID
    estado: EstadosPossiveis = EstadosPossiveis.nao_finalizado


TAREFAS = []


@app.get('/tarefas')
def listar():
    return TAREFAS


@app.post('/tarefas', response_model=Tarefa, status_code=201)
def criar(tarefa: TarefaEntrada) :
    nova_tarefa: Tarefa = tarefa.dict()
    nova_tarefa['id'] = uuid4()
    TAREFAS.append(nova_tarefa)
    print(TAREFAS)
    return nova_tarefa