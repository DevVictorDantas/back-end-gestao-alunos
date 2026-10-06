#!/usr/bin/env bash
# =====================================================================
# Teste de aceitação da API — este é o SEU ALVO.
#
# Enquanto você não implementar o projeto, os testes vão falhar (conexão
# recusada ou 404). Conforme for concluindo os desafios, mais testes vão
# passar. Quando TODOS passarem com os status indicados, o projeto está
# completo.
#
# NÃO sobe servidor. Rode a API em um terminal:
#     uvicorn main:app --reload
# E este script em OUTRO terminal:
#     bash testar_api.sh
#
# A flag -i mostra os cabeçalhos HTTP (incluindo o status code).
# =====================================================================
set -u
BASE="http://127.0.0.1:8000"

echo "== 1) Criar aluno (esperado: 201 Created) =="
curl -s -i -X POST "$BASE/alunos" \
  -H "Content-Type: application/json" \
  -d '{"nome":"Ana","idade":20,"matricula":"2026001"}'
echo -e "\n"

echo "== 2) Criar de novo com a MESMA matrícula (esperado: 409 Conflict) =="
curl -s -i -X POST "$BASE/alunos" \
  -H "Content-Type: application/json" \
  -d '{"nome":"Outra","idade":21,"matricula":"2026001"}'
echo -e "\n"

echo "== 3) Listar alunos (esperado: 200 + lista) =="
curl -s "$BASE/alunos"
echo -e "\n"

echo "== 4) [Desafio 1] Filtrar por idade mínima (esperado: 200; só idade >= 18) =="
curl -s "$BASE/alunos?idade_minima=18"
echo -e "\n"

echo "== 5) Buscar aluno inexistente (esperado: 404 Not Found) =="
curl -s -i "$BASE/alunos/9999"
echo -e "\n"

echo "== 6) Atualizar parcialmente a média do aluno 1 (esperado: 200) =="
curl -s -X PATCH "$BASE/alunos/1" \
  -H "Content-Type: application/json" \
  -d '{"media": 9.5}'
echo -e "\n"

echo "== 7) [Desafio 2] Criar disciplina (esperado: 201) =="
curl -s -X POST "$BASE/disciplinas" \
  -H "Content-Type: application/json" \
  -d '{"nome":"Python","carga_horaria":40}'
echo -e "\n"

echo "== 8) [Desafio 2] Listar disciplinas (esperado: 200 + lista) =="
curl -s "$BASE/disciplinas"
echo -e "\n"

echo "== 9) [Desafio 3] Matricular aluno 1 na disciplina 1 (esperado: 201) =="
curl -s -X POST "$BASE/alunos/1/matricular/1"
echo -e "\n"

echo "== 10) [Desafio 3] Disciplinas do aluno 1 (esperado: 200 + [Python]) =="
curl -s "$BASE/alunos/1/disciplinas"
echo -e "\n"

echo "== 11) Deletar aluno 1 (esperado: 204 No Content) =="
curl -s -i -X DELETE "$BASE/alunos/1"
echo -e "\n"
