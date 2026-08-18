from typing import List


from pydantic import BaseModel, ConfigDict, EmailStr


class Matricula(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    aluno_id: int
    curso_id: int


Matriculas = List[Matricula]


class Aluno(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
    email: EmailStr
    telefone: str


Alunos = List[Aluno]


class Curso(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
    codigo: str
    descricao: str


Cursos = List[Curso]
