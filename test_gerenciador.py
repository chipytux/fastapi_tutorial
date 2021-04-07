from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK
from gerenciador_tarefas.gerenciador import app, TAREFAS


def test_quando_listar_tarefas_devo_ter_como_retorno_codigo_status_200():
    client = TestClient(app)
    resposta = client.get('/tarefas')
    assert resposta.status_code == HTTP_200_OK


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
    TAREFAS.clear()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_titulo():
    TAREFAS.append({'titulo': 'titulo 1'})
    client = TestClient(app)
    resposta = client.get('/tarefas')
    assert 'titulo' in resposta.json().pop()
    TAREFAS.clear()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_descricao():
    TAREFAS.append({'descricao': 'descricao 1'})
    client = TestClient(app)
    resposta = client.get('/tarefas')
    assert 'descricao' in resposta.json().pop()
    TAREFAS.clear()

def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_estado():
    TAREFAS.append({'estado':  'finalizado'})
    client = TestClient(app)
    resposta = client.get('/tarefas')
    assert 'estado' in resposta.json().pop()
    TAREFAS.clear()
