import pytest
from fastapi.testclient import TestClient
from fastapi import status
from gerenciador_tarefas.gerenciador import app, TAREFAS


@pytest.fixture(scope='module')
def client():
    return TestClient(app)


def test_quando_listar_tarefas_devo_ter_como_retorno_codigo_status_200(client):
    resposta = client.get('/tarefas')
    assert resposta.status_code == status.HTTP_200_OK


def test_quando_listar_tarefas_formato_de_retorno_dev_ser_uma_lista(client):
    resposta = client.get('/tarefas')
    assert isinstance(resposta.json(), list)


def test_quando_listar_tarefas_retorno_deve_ser_uma_json(client):
    resposta = client.get('/tarefas')
    print(resposta)
    assert resposta.headers["Content-Type"] == "application/json"


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_id(client):
    TAREFAS.append({'id': 1})
    resposta = client.get('/tarefas')
    assert 'id' in resposta.json().pop()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_titulo(client):
    TAREFAS.append({'titulo': 'titulo 1'})
    resposta = client.get('/tarefas')
    assert 'titulo' in resposta.json().pop()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_descricao(client):
    TAREFAS.append({'descricao': 'descricao 1'})
    resposta = client.get('/tarefas')
    assert 'descricao' in resposta.json().pop()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_estado(client):
    TAREFAS.append({'estado': 'finalizado'})
    resposta = client.get('/tarefas')
    assert 'estado' in resposta.json().pop()
    TAREFAS.clear()


def test_listagem_deve_ser_ordenada_por_estado(client):
    tarefa1 = {
        'titulo': 'titulo1',
        'descricao': 'descricao1',
        'estado': 'não finalizado'
    }
    tarefa2 = {
        'titulo': 'titulo2',
        'descricao': 'descricao2',
        'estado': 'finalizado'
    }
    tarefa3 = {
        'titulo': 'titulo3',
        'descricao': 'descricao3',
        'estado': 'não finalizado'
    }
    tarefa4 = {
        'titulo': 'titulo4',
        'descricao': 'descricao4',
        'estado': 'finalizado'
    }

    TAREFAS.append(tarefa1)
    TAREFAS.append(tarefa2)
    TAREFAS.append(tarefa3)
    TAREFAS.append(tarefa4)
    resposta = client.get('/tarefas')
    assert resposta.json() == [tarefa2, tarefa4, tarefa1, tarefa3]
    TAREFAS.clear()


def test_recurso_tarefas_deve_aceita_verbo_post(client):
    resposta = client.post('/tarefas')
    assert resposta.status_code != status.HTTP_405_METHOD_NOT_ALLOWED
    TAREFAS.clear()


def test_quando_uma_tarefa_e_submetida_deve_possuir_um_titulo(client):
    resposta = client.post('/tarefas', json={})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    TAREFAS.clear()


def test_titulo_da_tarefa_deve_conter_entre_3_e_50_caracteres(client):
    resposta = client.post('/tarefas', json={'titulo': 2 * '*'})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    resposta = client.post('/tarefas', json={'titulo': 51 * '*'})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    TAREFAS.clear()


def test_quando_uma_tarefa_e_submetida_deve_possuir_uma_descricao(client):
    resposta = client.post('/tarefas', json={'titulo': 'titulo'})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    TAREFAS.clear()


def test_descrição_da_tarefa_pode_conter_no_maximo_140_caracteres(client):
    resposta = client.post('/tarefas',
                           json={
                               "titulo": "titulo",
                               "descricao": "*" * 141
                           })
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    TAREFAS.clear()


def test_quando_criar_uma_tarefa_a_mesma_deve_ser_retornada(client):
    tarefa = {'titulo': 'titulo', 'descricao': 'descricao'}
    resposta = client.post('/tarefas', json=tarefa)
    resposta_sem_id = resposta.json()
    del resposta_sem_id['id']
    del resposta_sem_id['estado']
    assert tarefa == resposta_sem_id
    TAREFAS.clear()


def test_quando_criar_uma_tarefa_seu_id_deve_ser_unico(client):
    tarefa1 = {'titulo': 'titulo1', 'descricao': 'descricao1'}
    tarefa2 = {'titulo': 'titulo2', 'descricao': 'descricao2'}
    resposta1 = client.post('/tarefas', json=tarefa1)
    resposta2 = client.post('/tarefas', json=tarefa2)
    assert resposta1.json()['id'] != resposta2.json()['id']
    TAREFAS.clear()


def test_quando_criar_uma_tarefa_seu_estado_padrao_e_nao_finalizado(client):
    tarefa = {'titulo': 'titulo', 'descricao': 'descricao'}
    resposta = client.post('/tarefas', json=tarefa)
    assert resposta.json()['estado'] == 'não finalizado'
    TAREFAS.clear()


def test_quando_criar_uma_tarefa_codigo_de_status_retornado_deve_ser_201(client):
    tarefa = {'titulo': 'titulo', 'descricao': 'descricao'}
    resposta = client.post('/tarefas', json=tarefa)
    assert resposta.status_code == status.HTTP_201_CREATED
    TAREFAS.clear()


def test_quando_criar_uma_tarefa_esta_deve_ser_persistida(client):
    tarefa = {'titulo': 'titulo', 'descricao': 'descricao'}
    resposta = client.post('/tarefas', json=tarefa)
    assert resposta.status_code == status.HTTP_201_CREATED
    assert len(TAREFAS) == 1
    TAREFAS.clear()


def test_quando_deletar_deve_retorna_status_code_204(client):
    id = '44bc2282-8735-4514-afb7-3f303b90d6bf'
    tarefa = {'id': id, 'titulo': 'titulo', 'descricao': 'descricao'}
    TAREFAS.append(tarefa)
    resposta = client.delete(f'/tarefas/{id}')
    assert resposta.status_code == status.HTTP_204_NO_CONTENT
    TAREFAS.clear()


def test_apagar_quando_não_houver_tarefa_com_o_código_retorna_status_code_404(client):
    id = '44bc2282-8735-4514-afb7-3f303b90d6bf'
    tarefa = {'id': id, 'titulo': 'titulo', 'descricao': 'descricao'}
    TAREFAS.append(tarefa)
    id_apagar = '12bc2282-8735-4514-afb7-3f303b90d6bf'
    resposta = client.delete(f'/tarefas/{id_apagar}')
    assert resposta.status_code == status.HTTP_404_NOT_FOUND
    TAREFAS.clear()


def test_finalizar_uma_tarefa_com_sucesso_deve_receber_codigo_200(client):
    id = '44bc2282-8735-4514-afb7-3f303b90d6bf'
    tarefa = {'id': id, 'titulo': 'titulo', 'descricao': 'descricao'}
    TAREFAS.append(tarefa)
    resposta = client.patch(f'/tarefas/{id}', json={'estado': 'finalizado'})
    assert resposta.status_code == status.HTTP_200_OK
    TAREFAS.clear()


def test_finalizar_uma_tarefa_com_erro_deve_receber_codigo_404(client):
    id = '44bc2282-8735-4514-afb7-3f303b90d6bf'
    resposta = client.patch(f'/tarefas/{id}', json={'estado': 'finalizado'})
    assert resposta.status_code == status.HTTP_404_NOT_FOUND
    TAREFAS.clear()


def test_finalizar_uma_tarefa_sem_enviar_um_estado_invalido_deve_retorna_codigo_422(client):
    id = '44bc2282-8735-4514-afb7-3f303b90d6bf'
    resposta = client.patch(f'/tarefas/{id}', json={'estado': 'invalido'})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    TAREFAS.clear()


def test_finalizar_uma_tarefa_com_sucesso_deve_receber_codigo_200(client):
    id = '44bc2282-8735-4514-afb7-3f303b90d6bf'
    tarefa = {'id': id, 'titulo': 'titulo', 'descricao': 'descricao'}
    TAREFAS.append(tarefa)
    resposta = client.patch(f'/tarefas/{id}', json={'estado': 'finalizado'})
    assert resposta.status_code == status.HTTP_200_OK
    TAREFAS.clear()


def test_finalizar_uma_tarefa_deve_retornar_tarefa_modificada(client):
    id = '44bc2282-8735-4514-afb7-3f303b90d6bf'
    tarefa = {'id': id, 'titulo': 'titulo', 'descricao': 'descricao'}
    TAREFAS.append(tarefa)
    resposta = client.patch(f'/tarefas/{id}', json={'estado': 'finalizado'})
    tarefa_esperada = tarefa
    tarefa_esperada.update({'estado': 'finalizado'})
    assert resposta.json() == tarefa_esperada
    TAREFAS.clear()
  

def test_finalizar_uma_tarefa_deve_modificar_a_lista_de_tarefas(client):
    id = '44bc2282-8735-4514-afb7-3f303b90d6bf'
    tarefa = {'id': id, 'titulo': 'titulo', 'descricao': 'descricao'}
    TAREFAS.append(tarefa)
    resposta = client.patch(f'/tarefas/{id}', json={'estado': 'finalizado'})
    tarefa_esperada = dict(tarefa)
    tarefa_esperada.update({'estado': 'finalizado'})
    assert tarefa_esperada in TAREFAS
    TAREFAS.clear()
  

def test_detalhar_uma_tarefa_deve_retornar_codigo_200_se_existir_uma_tarefa_valida(client):
    id = '44bc2282-8735-4514-afb7-3f303b90d6bf'
    tarefa = {'id': id, 'titulo': 'titulo', 'descricao': 'descricao'}
    TAREFAS.append(tarefa)
    resposta = client.get(f'/tarefas/{id}')
    assert resposta.status_code == status.HTTP_200_OK
    TAREFAS.clear()


def test_detalhar_uma_tarefa_deve_retornar_codigo_404_se_NAO_existir_uma_tarefa_valida(client):
    id = '44bc2282-8735-4514-afb7-3f303b90d6bf'
    resposta = client.get(f'/tarefas/{id}')
    assert resposta.status_code == status.HTTP_404_NOT_FOUND
    TAREFAS.clear()



def test_detalhar_uma_tarefa_deve_retornar_uma_tarefa(client):
    id = '44bc2282-8735-4514-afb7-3f303b90d6bf'
    tarefa = {'id': id, 'titulo': 'titulo', 'descricao': 'descricao'}
    TAREFAS.append(tarefa)
    resposta = client.get(f'/tarefas/{id}')
    assert resposta.json() == tarefa
    TAREFAS.clear()
