"""
CAMADA DE BANCO (db.py)  —  ESQUELETO, implemente você mesmo
============================================================

Esta é a ÚNICA parte do projeto que "fala SQL". As rotas (main.py) nunca
escrevem SQL: elas chamam as funções daqui. Essa separação em camadas é o
coração do módulo.

REGRA DE OURO (segurança): os VALORES que vêm do cliente vão SEMPRE como %s
+ tupla de parâmetros. Nunca concatene dados do usuário na string SQL
(isso abre SQL Injection).

Ordem sugerida de implementação:
  1. Configuração + conectar()      -> abrir conexão com o PostgreSQL
  2. criar_tabelas()                -> criar alunos, disciplinas, matriculas
  3. CRUD de alunos                 -> inserir / listar / buscar / atualizar / excluir
  4. CRUD de disciplinas            (Desafio 2)
  5. matrículas + JOIN              (Desafio 3)

O modelo de dados (as 3 tabelas) está definido em `esquema.sql` — use como
referência ao escrever criar_tabelas().
"""

# DICA — bibliotecas que você provavelmente vai usar:
import os
from contextlib import closing
import psycopg2  # type: ignore[reportMissingModuleSource]
from typing import Optional
from psycopg2.extras import RealDictCursor  # type: ignore[reportMissingModuleSource]
from dotenv import load_dotenv # type: ignore

# TODO: carregue as variáveis do .env (load_dotenv) e monte um CONFIG lendo
#       DB_HOST, DB_NAME, DB_USER, DB_PASSWORD (dica: os.getenv com um padrão).

load_dotenv()

# Em produção (Render, Railway, Neon, Supabase...) o banco costuma vir como
# uma URL única em DATABASE_URL. Se ela existir, tem prioridade sobre o CONFIG.
DATABASE_URL = os.getenv("DATABASE_URL")

CONFIG = {
  "host": os.getenv("DB_HOST"),
  "database": os.getenv("DB_NAME"),
  "user": os.getenv("DB_USER"),
  "password": os.getenv("DB_PASSWORD"),
  "port": os.getenv("DB_PORT"),
  # bancos gerenciados exigem SSL ("require"); localmente "prefer" funciona sem.
  "sslmode": os.getenv("DB_SSLMODE", "prefer"),
}

# TODO: def conectar():
#   Abra e devolva uma conexão psycopg2 usando o CONFIG.
#   Dica: passe cursor_factory=RealDictCursor para as linhas virem como dicts.
def conectar():
  if DATABASE_URL:
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
  return psycopg2.connect(**CONFIG, cursor_factory=RealDictCursor)

def executar_sql(sql, params=None, fetchone=False):
  # closing() fecha a conexão no fim: o "with" do psycopg2 sozinho só faz
  # commit/rollback e deixaria a conexão aberta (estoura o limite do banco).
  with closing(conectar()) as con, con, con.cursor() as cur:
    cur.execute(sql, params)
    sql_limpo = sql.strip().upper()
    
    if "RETURNING" in sql_limpo:
      dados = cur.fetchone()
      con.commit()
      return dados
    
    if sql_limpo.startswith(("CREATE", "INSERT", "UPDATE", "DELETE", "DROP")):
      con.commit()
      
      if sql_limpo.startswith("DELETE"):
        return cur.rowcount > 0
      return "Alteração realizada com sucesso."
         
    
    else:
      if fetchone:
          return  cur.fetchone()   
      else:
          return  cur.fetchall()

# TODO: def criar_tabelas():
#   Crie as 3 tabelas com "CREATE TABLE IF NOT EXISTS ..." (veja esquema.sql).
#   Esta função é chamada no startup da API (main.py).
def criar_tabelas():
  sql = """ CREATE TABLE IF NOT EXISTS alunos (
    id        SERIAL PRIMARY KEY,
    nome      VARCHAR(100) NOT NULL,
    idade     INTEGER,
    matricula VARCHAR(20) UNIQUE NOT NULL,  
    media     NUMERIC(4,2) DEFAULT 0
  );
  
  CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    senha_hash VARCHAR(72) NOT NULL,
    criado_em TIMESTAMP NOT NULL DEFAULT NOW()
  );
  """
  executar_sql(sql)


# --------------------------------------------------------------------------
# CRUD de ALUNOS
# --------------------------------------------------------------------------
# TODO: inserir_aluno(nome, idade, matricula, media=0)
#   INSERT na tabela alunos. Dica: use "RETURNING *" para já receber de volta
#   a linha criada (com o id gerado pelo banco).
def inserir_aluno(nome, idade, matricula, media=0):
  sql = "INSERT INTO alunos (nome, idade, matricula, media) VALUES (%s, %s, %s, %s) RETURNING id, nome, idade, matricula, media;"
  aluno_criado = executar_sql(sql, (nome, idade, matricula, media))
  return aluno_criado
#
# TODO: listar_alunos()
#   SELECT de todos os alunos, ordenados por id.
#   (Fazer aceitar filtros é o Desafio 1 — comece simples.)
def listar_alunos(idade_minima=None, media_minima=None, q=None):
  sql = "SELECT id, nome, idade, matricula, media FROM alunos"
  condicoes = []
  parametros = []
  if idade_minima is not None:
    condicoes.append("idade >= %s")
    parametros.append(idade_minima)  
  if media_minima is not None:
    condicoes.append("media >= %s")
    parametros.append(media_minima)
  if q is not None:
    condicoes.append("(nome ILIKE %s OR matricula ILIKE %s)")
    parametros.extend([f"%{q}%", f"%{q}%"])  # um valor para cada %s
  if condicoes:
    sql += " WHERE " + " AND ".join(condicoes)
    
  sql += " ORDER BY id ASC"
  lista_alunos = executar_sql(sql, tuple(parametros) if parametros else None)
  return lista_alunos
#
# TODO: buscar_aluno(aluno_id)
#   SELECT de um aluno por id. Devolva None se não existir.

def buscar_aluno(id):
  sql = "SELECT id, nome, idade, matricula, media FROM alunos WHERE id = %s;"       
  aluno = executar_sql(sql, (id,), fetchone=True)
  return aluno

# TODO: atualizar_aluno(aluno_id, **campos)
#   UPDATE parcial: atualize só os campos recebidos. Dica: nomes de coluna
#   podem entrar por f-string (são do seu código); VALORES vão com %s.
def atualizar_aluno(id, **campos):
  if not campos:
    return buscar_aluno(id)
  sets = ", ".join(f"{coluna} = %s" for coluna in campos)
  sql = f"UPDATE alunos SET {sets} WHERE id = %s RETURNING *;"
  valores = list(campos.values()) + [id]
  return executar_sql(sql, valores)
#
# TODO: excluir_aluno(aluno_id)
#   DELETE por id. Devolva True/False (dica: cur.rowcount > 0).

def excluir_aluno(id):
  sql = "DELETE FROM alunos WHERE id = %s;"
  aluno_excluido = executar_sql(sql, (id,))
  return aluno_excluido

def inserir_usuario(nome, username, senha_hash):
  sql = "INSERT INTO usuarios (nome, username, senha_hash) VALUES (%s, %s, %s) RETURNING id, nome, username, criado_em;"
  usuario_criado = executar_sql(sql, (nome, username, senha_hash))
  return usuario_criado

def buscar_usuario_por_username(username):
  sql = "SELECT id, nome, username, senha_hash, criado_em FROM usuarios WHERE username = %s;"
  usuario = executar_sql(sql, (username,), fetchone=True)
  return usuario

def listar_usuarios():
  sql = "SELECT id, nome, username, criado_em FROM usuarios ORDER BY id ASC;"
  usuarios = executar_sql(sql)
  return usuarios

def excluir_usuario(id):
  sql = "DELETE FROM usuarios WHERE id = %s;"
  usuario_excluido = executar_sql(sql, (id,))
  return usuario_excluido
