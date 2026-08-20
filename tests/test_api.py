ALUNO = {
    "nome": "Ana Souza",
    "email": "ana@example.com",
    "telefone": "11999999999",
}

CURSO = {
    "nome": "Python para APIs",
    "codigo": "PY-API",
    "descricao": "Desenvolvimento de APIs REST com Python.",
}


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_crud_de_aluno(client):
    create_response = client.post("/alunos", json=ALUNO)
    assert create_response.status_code == 201
    aluno = create_response.json()
    assert aluno["id"] == 1
    assert aluno["email"] == ALUNO["email"]

    read_response = client.get(f"/alunos/{aluno['id']}")
    assert read_response.status_code == 200
    assert read_response.json() == aluno

    atualizado = {**ALUNO, "nome": "Ana Oliveira"}
    update_response = client.put(f"/alunos/{aluno['id']}", json=atualizado)
    assert update_response.status_code == 200
    assert update_response.json()["nome"] == "Ana Oliveira"

    delete_response = client.delete(f"/alunos/{aluno['id']}")
    assert delete_response.status_code == 200
    assert client.get(f"/alunos/{aluno['id']}").status_code == 404


def test_impede_email_duplicado(client):
    assert client.post("/alunos", json=ALUNO).status_code == 201

    response = client.post("/alunos", json={**ALUNO, "nome": "Outra Pessoa"})

    assert response.status_code == 409
    assert "e-mail" in response.json()["detail"]


def test_crud_de_curso(client):
    create_response = client.post("/cursos", json=CURSO)
    assert create_response.status_code == 201
    curso = create_response.json()
    assert curso["id"] == 1

    read_response = client.get(f"/cursos/{CURSO['codigo']}")
    assert read_response.status_code == 200
    assert read_response.json() == curso

    update_payload = {**CURSO, "nome": "APIs com FastAPI"}
    update_response = client.put(f"/cursos/{CURSO['codigo']}", json=update_payload)
    assert update_response.status_code == 200
    assert update_response.json()["nome"] == "APIs com FastAPI"

    delete_response = client.delete(f"/cursos/{CURSO['codigo']}")
    assert delete_response.status_code == 200
    assert client.get(f"/cursos/{CURSO['codigo']}").status_code == 404


def test_impede_codigo_de_curso_duplicado(client):
    assert client.post("/cursos", json=CURSO).status_code == 201

    response = client.post("/cursos", json={**CURSO, "nome": "Outro Curso"})

    assert response.status_code == 409


def test_fluxo_de_matricula_e_consultas(client):
    aluno = client.post("/alunos", json=ALUNO).json()
    curso = client.post("/cursos", json=CURSO).json()
    payload = {"aluno_id": aluno["id"], "curso_id": curso["id"]}

    create_response = client.post("/matriculas", json=payload)
    assert create_response.status_code == 201
    assert create_response.json() == {"id": 1, **payload}

    duplicate_response = client.post("/matriculas", json=payload)
    assert duplicate_response.status_code == 409

    aluno_response = client.get("/matriculas/aluno/Ana")
    assert aluno_response.status_code == 200
    assert aluno_response.json() == {
        "aluno": ALUNO["nome"],
        "cursos": [CURSO["nome"]],
    }

    curso_response = client.get(f"/matriculas/curso/{CURSO['codigo']}")
    assert curso_response.status_code == 200
    assert curso_response.json() == {
        "curso": CURSO["nome"],
        "alunos": [ALUNO["nome"]],
    }


def test_exclusao_de_aluno_remove_matricula(client):
    aluno = client.post("/alunos", json=ALUNO).json()
    curso = client.post("/cursos", json=CURSO).json()
    client.post(
        "/matriculas",
        json={"aluno_id": aluno["id"], "curso_id": curso["id"]},
    )

    assert client.delete(f"/alunos/{aluno['id']}").status_code == 200

    response = client.get(f"/matriculas/curso/{CURSO['codigo']}")
    assert response.status_code == 404


def test_validacoes_e_recursos_inexistentes(client):
    assert client.post("/alunos", json={**ALUNO, "email": "invalido"}).status_code == 422
    assert client.get("/alunos/999").status_code == 404
    assert client.get("/cursos/INEXISTENTE").status_code == 404
    assert (
        client.post("/matriculas", json={"aluno_id": 1, "curso_id": 1}).status_code
        == 404
    )
