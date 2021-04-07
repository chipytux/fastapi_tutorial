from fastapi.testclient import TestClient
from fastapi import status
from gerenciador_tarefas.gerenciador import app, TAREFAS


def test_quando_listar_tarefas_devo_ter_como_retorno_codigo_status_200():
    client = TestClient(app)
    resposta = client.get('/tarefas')
    assert resposta.status_code == status.HTTP_200_OK


def test_quando_listar_tarefas_formato_de_retorno_dev_ser_uma_lista():
    client = TestClient(app)
    resposta = client.get('/tarefas')
    assert isinstance(resposta.json(), list)


def test_quando_listar_tarefas_retorno_deve_ser_uma_json():
    client = TestClient(app)
    resposta = client.get('/tarefas')
    print(resposta)
    assert resposta.headers["Content-Type"] == "application/json"


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_id():
    TAREFAS.append({'id': 1})
    client = TestClient(app)
    resposta = client.get('/tarefas')
    assert 'id' in resposta.json().pop()



def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_titulo():
    TAREFAS.append({'titulo': 'titulo 1'})
    client = TestClient(app)
    resposta = client.get('/tarefas')
    assert 'titulo' in resposta.json().pop()



def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_descricao():
    TAREFAS.append({'descricao': 'descricao 1'})
    client = TestClient(app)
    resposta = client.get('/tarefas')
    assert 'descricao' in resposta.json().pop()



def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_estado():
    TAREFAS.append({'estado': 'finalizado'})
    client = TestClient(app)
    resposta = client.get('/tarefas')
    assert 'estado' in resposta.json().pop()
    TAREFAS.clear()


def test_recurso_tarefas_deve_aceita_verbo_post():
    client = TestClient(app)
    resposta = client.post('/tarefas')
    assert resposta.status_code != status.HTTP_405_METHOD_NOT_ALLOWED
    TAREFAS.clear()

def test_quando_uma_tarefa_e_submetida_deve_possuir_um_titulo():
    client = TestClient(app)
    resposta = client.post('/tarefas', json={})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    TAREFAS.clear()

def test_titulo_da_tarefa_deve_conter_entre_3_e_50_caracteres():
    client = TestClient(app)
    resposta = client.post('/tarefas', json={'titulo': 2 * '*'})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    resposta = client.post('/tarefas', json={'titulo': 51 * '*'})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    TAREFAS.clear()


def test_quando_uma_tarefa_e_submetida_deve_possuir_uma_descricao():
    client = TestClient(app)
    resposta = client.post('/tarefas', json={'titulo': 'titulo'})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    TAREFAS.clear()

def test_descrição_da_tarefa_pode_conter_no_maximo_140_caracteres():
    client = TestClient(app)
    resposta = client.post('/tarefas',
                           json={
                               "titulo": "titulo",
                               "descricao": "*" * 141
                           })
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    TAREFAS.clear()

def test_quando_criar_uma_tarefa_a_mesma_deve_ser_retornada():
    client = TestClient(app)
    tarefa = {'titulo': 'titulo', 'descricao': 'descricao'}
    resposta = client.post('/tarefas', json=tarefa)
    resposta_sem_id = resposta.json()
    del resposta_sem_id['id']
    del resposta_sem_id['estado']
    assert tarefa == resposta_sem_id
    TAREFAS.clear()

def test_quando_criar_uma_tarefa_seu_id_deve_ser_unico():
    client = TestClient(app)
    tarefa1 = {'titulo': 'titulo1', 'descricao': 'descricao1'}
    tarefa2 = {'titulo': 'titulo2', 'descricao': 'descricao2'}
    resposta1 = client.post('/tarefas', json=tarefa1)
    resposta2 = client.post('/tarefas', json=tarefa2)
    assert resposta1.json()['id'] != resposta2.json()['id']
    TAREFAS.clear()

def test_quando_criar_uma_tarefa_seu_estado_padrao_e_nao_finalizado():
    client = TestClient(app)
    tarefa = {'titulo': 'titulo', 'descricao': 'descricao'}
    resposta = client.post('/tarefas', json=tarefa)
    assert resposta.json()['estado'] == 'não finalizado'
    TAREFAS.clear()

def test_quando_criar_uma_tarefa_codigo_de_status_retornado_deve_ser_201():
    client = TestClient(app)
    tarefa = {'titulo': 'titulo', 'descricao': 'descricao'}
    resposta = client.post('/tarefas', json=tarefa)
    assert resposta.status_code == status.HTTP_201_CREATED
    TAREFAS.clear()


def test_quando_criar_uma_tarefa_esta_deve_ser_persistida():
    client = TestClient(app)
    tarefa = {'titulo': 'titulo', 'descricao': 'descricao'}
    resposta = client.post('/tarefas', json=tarefa)
    assert resposta.status_code == status.HTTP_201_CREATED
    assert len(TAREFAS) == 1
    TAREFAS.clear()