"""
CAMADA DE ROTAS (main.py)  —  ESQUELETO, implemente você mesmo
==============================================================

É o "cardápio" da API: cada rota é um endpoint. Mantenha as rotas FINAS —
elas só devem:
  1. receber/validar a entrada (via schemas do Pydantic);
  2. chamar UMA função do db.py;
  3. traduzir o resultado em resposta HTTP (status code + corpo).

Nenhuma regra de negócio ou SQL mora aqui.

Depois de implementar, rode (com o venv ativado e o PostgreSQL no ar):
    uvicorn main:app --reload
E explore em: http://127.0.0.1:8000/docs
"""

# DICA — o que você vai importar:
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status # type: ignore
from fastapi.responses import RedirectResponse # type: ignore
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # type: ignore
from psycopg2.errors import UniqueViolation   # type: ignore # para tratar duplicidade
import db
from schemas import AlunoEntrada, AlunoAtualizacao, AlunoSaida, UsuarioEntrada, UsuarioLogin, UsuarioSaida, Token
import auth

seguranca = HTTPBearer()  # para extrair o token do header Authorization

def usuario_logado(token: HTTPAuthorizationCredentials = Depends(seguranca)) -> dict:
    username = auth.ler_token(token.credentials)
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado", headers={"WWW-Authenticate": "Bearer"})
    
    usuario = db.buscar_usuario_por_username(username)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")
    return usuario

# TODO: crie a aplicação -> app = FastAPI(title="Gestão de Alunos")
#       (a variável PRECISA se chamar `app` — é o que o uvicorn procura.)
app = FastAPI(title="Gestão de Alunos")

# TODO: registre o startup para criar as tabelas:
#   @app.on_event("startup")
#   def ao_iniciar():
#       db.criar_tabelas()

@app.on_event("startup")
def ao_iniciar():
    db.criar_tabelas()

# TODO: GET /  -> uma mensagem de boas-vindas (ex.: aponte para /docs).

@app.get("/")
def boas_vindas():
    return RedirectResponse(url="/docs")



# ========================= ALUNOS =========================
# Verbo/rota/status que você deve implementar (o "coração" do REST):
#
#   POST   /alunos            -> 201 Created; devolva o objeto criado.
#                                Trate matrícula duplicada com 409 Conflict
#                                (except UniqueViolation).
#   GET    /alunos            -> 200; lista. (Filtros = Desafio 1.)
#   GET    /alunos/{id}       -> 200 com o aluno, ou 404 se não existir.
#   PATCH  /alunos/{id}       -> 200; atualização parcial. Dica:
#                                payload.model_dump(exclude_unset=True).
#   DELETE /alunos/{id}       -> 204 No Content; 404 se não existir.
#
# Lembre: use response_model=AlunoSaida e status_code=status.HTTP_201_CREATED etc.
@app.post("/alunos", response_model=AlunoSaida, status_code=status.HTTP_201_CREATED)
def criar_aluno(payload: AlunoEntrada, usuario: dict = Depends(usuario_logado)):
  try:
    aluno_criado = db.inserir_aluno(payload.nome, payload.idade, payload.matricula, payload.media)
    return aluno_criado
  except UniqueViolation:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Matrícula duplicada.")
  
@app.get("/alunos", response_model=List[AlunoSaida])
def listar_alunos(
    idade_minima: int | None = None,
    media_minima: float | None = None,
    q: str | None = None
):
    return db.listar_alunos(idade_minima, media_minima, q)

@app.get("/alunos/{id}", response_model=AlunoSaida)
def buscar_aluno(id: int):
  aluno = db.buscar_aluno(id)
  if aluno is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado.")
  return aluno
  
@app.patch("/alunos/{id}", response_model=AlunoSaida)
def atualizar_aluno(id: int, payload: AlunoAtualizacao, usuario: dict = Depends(usuario_logado)):
    if not db.buscar_aluno(id):
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return db.atualizar_aluno(id, **payload.model_dump(exclude_unset=True))
    
  
@app.delete("/alunos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_aluno(id: int, usuario: dict = Depends(usuario_logado)):
  if not db.excluir_aluno(id):
    raise HTTPException(status_code=404, detail="Aluno não encontrado")

# ========================= USUÁRIOS =========================
@app.post("/registrar", response_model=UsuarioSaida, status_code=status.HTTP_201_CREATED)
def registrar(payload: UsuarioEntrada, usuario: dict = Depends(usuario_logado)):
    senha_hash = auth.gerar_hash(payload.senha)
    try:
        usuario_criado = db.inserir_usuario(payload.nome, payload.username, senha_hash)
        return usuario_criado
    except UniqueViolation:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username já registrado.")
    
@app.post("/login", response_model=Token)
def login(payload: UsuarioLogin):
    usuario = db.buscar_usuario_por_username(payload.username)
    
    if usuario is None:
        auth.conferir_senha(payload.senha, auth.HASH_FALSO)  # para não vazar tempo de resposta
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos")
    
    if not auth.conferir_senha(payload.senha, usuario["senha_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos")
    
    return {"access_token": auth.criar_token(payload.username), "token_type": "bearer"}

@app.get("/eu", response_model=UsuarioSaida)
def eu(usuario: dict = Depends(usuario_logado)):
    return usuario