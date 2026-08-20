from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Curso as ModelCurso
from schemas import CursoCreate, CursoResponse

cursos_router = APIRouter()

@cursos_router.get("/cursos", response_model=List[CursoResponse])
def read_cursos(db: Session = Depends(get_db)):
    cursos = db.query(ModelCurso).all()
    return cursos

@cursos_router.post(
    "/cursos", response_model=CursoResponse, status_code=status.HTTP_201_CREATED
)
def create_curso(curso: CursoCreate, db: Session = Depends(get_db)):
    codigo_existente = (
        db.query(ModelCurso).filter(ModelCurso.codigo == curso.codigo).first()
    )
    if codigo_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um curso cadastrado com este código",
        )

    db_curso = ModelCurso(**curso.model_dump())
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    return db_curso

@cursos_router.put("/cursos/{codigo_curso}", response_model=CursoResponse)
def update_curso(codigo_curso: str, curso: CursoCreate, db: Session = Depends(get_db)):
    db_curso = db.query(ModelCurso).filter(ModelCurso.codigo == codigo_curso).first()
    if db_curso is None:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    codigo_existente = (
        db.query(ModelCurso)
        .filter(ModelCurso.codigo == curso.codigo, ModelCurso.id != db_curso.id)
        .first()
    )
    if codigo_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um curso cadastrado com este código",
        )

    for key, value in curso.model_dump(exclude_unset=True).items():
        setattr(db_curso, key, value)

    db.commit()
    db.refresh(db_curso)
    return db_curso

@cursos_router.get("/cursos/{codigo_curso}", response_model=CursoResponse)
def read_curso_por_codigo(codigo_curso: str, db: Session = Depends(get_db)):
    db_curso = db.query(ModelCurso).filter(ModelCurso.codigo == codigo_curso).first()
    if db_curso is None:
        raise HTTPException(status_code=404, detail="Nenhum curso encontrado com esse código")
    return db_curso


@cursos_router.delete("/cursos/{codigo_curso}", response_model=CursoResponse)
def delete_curso(codigo_curso: str, db: Session = Depends(get_db)):
    db_curso = db.query(ModelCurso).filter(ModelCurso.codigo == codigo_curso).first()
    if db_curso is None:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    curso_deletado = CursoResponse.model_validate(db_curso)
    db.delete(db_curso)
    db.commit()
    return curso_deletado
