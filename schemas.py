"""
CAMADA DE VALIDAÇÃO (schemas.py)  —  ESQUELETO, implemente você mesmo
====================================================================

"Schema" = o formato/contrato dos dados. Com Pydantic, você declara COMO os
dados devem ser quando ENTRAM e quando SAEM da API. O Pydantic valida sozinho:
se o cliente mandar idade=200 ou nome vazio, a API responde 422 automaticamente.

Boas práticas que você deve aplicar:
  - Separe ENTRADA (o que o cliente manda) de SAÍDA (o que a API devolve).
  - Na entrada de criação, NÃO inclua o id (quem gera é o banco).
  - Na saída, inclua o id.
  - Campos sensíveis (ex.: senha) podem entrar, mas NUNCA sair.
"""

# DICA — o que você vai importar:
from typing import Optional
from pydantic import BaseModel, Field # type: ignore
from datetime import datetime



# --------------------------------------------------------------------------
# ALUNO
# --------------------------------------------------------------------------
# TODO: AlunoEntrada  (POST) — campos: nome, idade, matricula, media (sem id)
#   Dica: valide com Field, ex.: nome=Field(min_length=1, max_length=100),
#   idade=Field(ge=0, le=120), media=Field(default=0, ge=0, le=10).

class AlunoEntrada(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    idade: int = Field(ge=0, le=120)
    matricula: str = Field(min_length=1, max_length=20)
    media: float = Field(default=0, ge=0, le=10)
    
#
# TODO: AlunoAtualizacao  (PATCH) — mesmos campos, mas TODOS Optional (=None),
#   para o cliente enviar só o que quer mudar. (A matrícula não se altera.)

class AlunoAtualizacao(BaseModel):
    nome: Optional[str] = Field(min_length=1, max_length=100)
    idade: Optional[int] = Field(ge=0, le=120)
    media: Optional[float] = Field(default=0, ge=0, le=10)
#
# TODO: AlunoSaida  — o que a API devolve, incluindo o id.
class AlunoSaida(BaseModel):
    id: int
    nome: str
    idade: Optional[int]
    matricula: str
    media: float

class UsuarioEntrada(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=1, max_length=50)
    senha: str = Field(min_length=8, max_length=72)  # Limite do bcrypt
    
class UsuarioLogin(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    senha: str = Field(min_length=8, max_length=72)  # Limite do bcrypt    

class UsuarioSaida(BaseModel):
    id: int
    nome: str
    username: str
    criado_em: datetime  # Timestamp de criação
    
class Login(BaseModel):
    message: str
    senha: str = Field(min_length=8, max_length=72)  # Limite do bcrypt