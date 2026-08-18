# API de Gestão Escolar com FastAPI e Docker

API REST para gerenciar alunos, cursos e matrículas de uma instituição de ensino. O projeto foi desenvolvido durante a Imersão DevOps da Alura com Google Cloud e organizado para execução local com Python ou Docker.

## Tecnologias

- Python 3.13
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Docker e Docker Compose

## Funcionalidades

- Cadastrar, listar, consultar, atualizar e excluir alunos.
- Cadastrar, listar, consultar e atualizar cursos.
- Matricular alunos em cursos.
- Consultar cursos de um aluno.
- Consultar alunos matriculados em um curso.
- Verificar a disponibilidade da API pelo endpoint `/health`.

## Como executar com Docker

### Pré-requisitos

- [Git](https://git-scm.com/downloads)
- [Docker](https://www.docker.com/get-started/)

```bash
git clone https://github.com/jessicatrindadeads/docker.git
cd docker
docker compose up --build
```

Acesse a documentação interativa em [http://localhost:8000/docs](http://localhost:8000/docs).

Para encerrar os contêineres:

```bash
docker compose down
```

## Como executar com Python

### Pré-requisitos

- Python 3.10 ou superior
- Git

```bash
git clone https://github.com/jessicatrindadeads/docker.git
cd docker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

No Windows, ative o ambiente virtual com:

```powershell
venv\Scripts\activate
```

## Principais endpoints

| Método | Endpoint | Descrição |
| --- | --- | --- |
| `GET` | `/health` | Verifica a disponibilidade da API |
| `GET` | `/alunos` | Lista os alunos |
| `POST` | `/alunos` | Cadastra um aluno |
| `GET` | `/alunos/{id}` | Consulta um aluno pelo ID |
| `PUT` | `/alunos/{id}` | Atualiza um aluno |
| `DELETE` | `/alunos/{id}` | Exclui um aluno |
| `GET` | `/cursos` | Lista os cursos |
| `POST` | `/cursos` | Cadastra um curso |
| `GET` | `/cursos/{codigo}` | Consulta um curso pelo código |
| `PUT` | `/cursos/{codigo}` | Atualiza um curso |
| `POST` | `/matriculas` | Matricula um aluno em um curso |
| `GET` | `/matriculas/aluno/{nome}` | Lista os cursos de um aluno |
| `GET` | `/matriculas/curso/{codigo}` | Lista os alunos de um curso |

Todos os endpoints e seus formatos de entrada e saída estão disponíveis também em `/docs`.

## Estrutura do projeto

```text
.
├── routers/
│   ├── alunos.py
│   ├── cursos.py
│   └── matriculas.py
├── app.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

O banco SQLite é criado automaticamente como `escola.db` na primeira execução. Esse arquivo é ignorado pelo Git para evitar o versionamento de dados locais.

## Origem

Projeto baseado no conteúdo educacional da [Imersão DevOps da Alura](https://github.com/guilhermeonrails/imersao-devops), com ajustes de organização, documentação e configuração Docker.
