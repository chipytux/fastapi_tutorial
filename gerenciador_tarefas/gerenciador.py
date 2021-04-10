from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, constr
from uuid import uuid4, UUID
from enum import Enum
from typing import List, Optional
from operator import itemgetter

app = FastAPI(docs_url='/',
              title="TODO List",
              description="Implementa um Gerenciador de Tarefas TODO List")


class EstadosPossiveis(str, Enum):
    finalizado = 'finalizado'
    nao_finalizado = 'não finalizado'


class FinalizarEntrada(BaseModel):
    estado: EstadosPossiveis


class TarefaEntrada(BaseModel):
    titulo: constr(min_length=3, max_length=50)
    descricao: constr(max_length=140)


class Tarefa(TarefaEntrada):
    id: UUID
    estado: EstadosPossiveis = EstadosPossiveis.nao_finalizado


TAREFAS: List[Tarefa] = []


@app.get('/tarefas', name='Ordenar a listagem por estado', tags=['Tarefas'])
def listar():
    ''' Listar todas as tarefas 
    Já temos a listagem pronta mas não garantimos que sua ordenação está correta.
    Um teste que pode ser escrito aqui é adição de duas tarefas, sendo a primeira finalizada e a segunda não finalizada.
    A exibição da listagem de tarefas deve apresentar a segunda primeiro. Para fazer esta checagem, verifique a respost e a ordem das tarefas retornadas.
    A função sorted pode ser seu aliado para resolver este problema.
    Outra função bastante útil é a itemgetter que pode ser utilizada no parâmetro key da função sorted.
    Uma alteração que pode ser feita na listagem é utilização de List[Tarefa] como modelo de resposta( parâmetro response_model no decorador), esta mudança ajuda a melhorar a documentação autogerada.
    warning itemgetter pode ser obtido através do pacote operator.from operator import itemgetter
    '''
    try:
        return sorted(TAREFAS, key=itemgetter('estado'))
    except:
        return TAREFAS


@app.post('/tarefas', response_model=Tarefa, status_code=201, tags=['Tarefas'])
def criar(tarefa: TarefaEntrada):
    ''' Criar novas Tarefas '''
    nova_tarefa: Tarefa = tarefa.dict()
    nova_tarefa['id'] = uuid4()
    TAREFAS.append(nova_tarefa)
    return nova_tarefa


@app.delete('/tarefas/{id}',
            name='Remover Tarefa',
            response_model=None,
            status_code=204,
            tags=['Tarefas'])
def remover(id: str) -> None:
    '''
    A remoção e tarefas consiste em buscar uma tarefa e em seguida remove-la.
    O método utilizado é o DELETE.
    O código de status retornado mais comum é o 204 No Content.
    Você deve especificar o id da tarefa a ser removida na url /tarefas/86d92774-281c-4e5a-87f2-69029177bfd2.
    Caso não encontra uma tarefa, o código de status 404 Not Found deve ser retornado.
    '''
    tarefa_a_ser_removida = list(
        [elem for elem in TAREFAS if elem['id'] == id])
    if (not tarefa_a_ser_removida):
        raise HTTPException(status_code=404, detail="Item not found")
    TAREFAS.remove(tarefa_a_ser_removida[0])


@app.patch('/tarefas/{id}', name='Finalizar Tarefa', tags=['Tarefas'])
def finalizar(id: str, entrada: FinalizarEntrada):
    '''
    Finalizar uma tarefa, pode ser representado através do método PUT ou PATCH, modificando o valor de estado de uma tarefa.
    Devemos procurar uma tarefa e caso não seja encontrada, o código de status 404 Not Found deve ser retornado.
    Os campos a serem modificados podem ser inválidos, caso isto ocorra everemos avisar ao cliente o seu erro. O código de status 422 Unprocessable Entity pode ser utilizado aqui.
    Se bem sucedido o código de status 200 OK deve ser retornado e o corpo da resposta deve conter a trefa com o valor já modificado.
    Você deve especificar o id da tarefa a ser removida na url /tarefas/86d92774-281c-4e5a-87f2-69029177bfd2.
    '''
    try:
        lista_busca_tarefas = next(
            filter(lambda tarefa: tarefa['id'] == str(id), TAREFAS))
    except:
        raise HTTPException(status_code=404)
    else:
        tarefa_atualizada = lista_busca_tarefas
        indice_tarefa = TAREFAS.index(tarefa_atualizada)
        tarefa_atualizada.update(entrada)
        TAREFAS[indice_tarefa] = tarefa_atualizada
        return tarefa_atualizada


@app.get('/tarefas/{id}',
         response_model=Tarefa,
         name='Detalhar Tarefa',
         tags=['Tarefas'])
def detalhar(id: UUID):
    '''
    Detalhar uma tarefa é busca-la na lista de tarefas e exibir seu valor.
    Caso a tarefa não seja encontrada o código de status 404 Not Found deve ser retornado.
    Você deve especificar o id da tarefa a ser removida na url /tarefas/86d92774-281c-4e5a-87f2-69029177bfd2.
    O código de status retornado quando bem sucedido é 200 OK.
    '''
    try:
        tarefa_encontrada = next(
            filter(lambda tarefa: tarefa['id'] == id, TAREFAS))
    except:
        raise HTTPException(status_code=404)
    else:
        return tarefa_encontrada
