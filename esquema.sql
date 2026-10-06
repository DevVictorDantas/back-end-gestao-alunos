-- =====================================================================
-- Esquema do banco "gestao_alunos" (Módulo 08 — CRUD Completo)
-- ---------------------------------------------------------------------
-- A API cria estas tabelas sozinha no startup (db.criar_tabelas).
-- Este arquivo serve para DEMONSTRAR o SQL na aula e para quem quiser
-- criar/inspecionar as tabelas manualmente no psql.
--
-- Criar o banco e o usuário (rode como superusuário, ex.: postgres):
--   CREATE DATABASE gestao_alunos;
--   CREATE USER curso WITH PASSWORD 'senha123';
--   GRANT ALL PRIVILEGES ON DATABASE gestao_alunos TO curso;
-- =====================================================================

CREATE TABLE IF NOT EXISTS alunos (
    id        SERIAL PRIMARY KEY,       -- id automático, único
    nome      VARCHAR(100) NOT NULL,
    idade     INTEGER,
    matricula VARCHAR(20) UNIQUE NOT NULL,  -- não pode repetir
    media     NUMERIC(4,2) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS disciplinas (
    id            SERIAL PRIMARY KEY,
    nome          VARCHAR(100) NOT NULL UNIQUE,
    carga_horaria INTEGER NOT NULL
);

-- Tabela de JUNÇÃO: modela o "muitos-para-muitos".
-- Um aluno cursa várias disciplinas; uma disciplina tem vários alunos.
CREATE TABLE IF NOT EXISTS matriculas (
    id            SERIAL PRIMARY KEY,
    -- FOREIGN KEY: aluno_id precisa apontar para um aluno que existe.
    -- ON DELETE CASCADE: apagou o aluno -> apaga as matrículas dele.
    aluno_id      INTEGER REFERENCES alunos(id) ON DELETE CASCADE,
    disciplina_id INTEGER REFERENCES disciplinas(id) ON DELETE CASCADE,
    UNIQUE (aluno_id, disciplina_id)     -- mesma matrícula só uma vez
);

-- Consulta de exemplo: quais disciplinas o aluno de id=1 cursa?
--   SELECT d.nome
--   FROM disciplinas d
--   JOIN matriculas m ON m.disciplina_id = d.id
--   WHERE m.aluno_id = 1;
