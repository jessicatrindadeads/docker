from pydantic import BaseModel, ConfigDict, EmailStr


class MatriculaCreate(BaseModel):
    aluno_id: int
    curso_id: int


class MatriculaResponse(MatriculaCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class AlunoCreate(BaseModel):
    nome: str
    email: EmailStr
    telefone: str


class AlunoResponse(AlunoCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CursoCreate(BaseModel):
    nome: str
    codigo: str
    descricao: str


class CursoResponse(CursoCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
