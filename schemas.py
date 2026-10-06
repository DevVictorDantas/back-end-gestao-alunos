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
#   from typing import Optional
#   from pydantic import BaseModel, Field


# --------------------------------------------------------------------------
# ALUNO
# --------------------------------------------------------------------------
# TODO: AlunoEntrada  (POST) — campos: nome, idade, matricula, media (sem id)
#   Dica: valide com Field, ex.: nome=Field(min_length=1, max_length=100),
#   idade=Field(ge=0, le=120), media=Field(default=0, ge=0, le=10).
#
# TODO: AlunoAtualizacao  (PATCH) — mesmos campos, mas TODOS Optional (=None),
#   para o cliente enviar só o que quer mudar. (A matrícula não se altera.)
#
# TODO: AlunoSaida  — o que a API devolve, incluindo o id.


# --------------------------------------------------------------------------
# DISCIPLINA  (Desafio 2)
# --------------------------------------------------------------------------
# TODO: DisciplinaEntrada (nome, carga_horaria) e DisciplinaSaida (id, nome,
#   carga_horaria). Dica: carga_horaria=Field(gt=0) exige valor positivo.
