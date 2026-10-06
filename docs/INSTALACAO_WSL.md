# Guia de instalação — WSL Ubuntu (do zero ao projeto rodando)

Este guia lista **tudo** que precisa ser instalado num **WSL Ubuntu** para
rodar este projeto: a **API de Gestão de Alunos** (CRUD completo com FastAPI +
PostgreSQL). Ele serve de **base/template** — você usa este repositório como
ponto de partida e continua o projeto a partir daqui.

É escrito passo a passo, para quem **nunca** configurou um ambiente Linux.
Copie e cole cada bloco de comando na ordem. Onde algo pode dar errado, há uma
seção de **Solução de problemas** no final.

> **O que é WSL?** "Windows Subsystem for Linux" — é um Ubuntu de verdade
> rodando dentro do Windows, sem máquina virtual pesada nem dual boot. Você
> abre um terminal Linux e trabalha nele.

> **Estrutura esperada do projeto** (tudo na raiz do repositório):
>
> ```
> seu-projeto/
> ├── main.py            # rotas FastAPI
> ├── db.py              # conexão e queries SQL
> ├── schemas.py         # modelos Pydantic (validação)
> ├── esquema.sql        # o SQL das tabelas (referência)
> ├── testar_api.sh      # roteiro de teste com curl
> ├── requirements.txt   # bibliotecas do projeto
> ├── .env.example       # modelo de credenciais (copie para .env)
> ├── .gitignore
> └── README.md
> ```

---

## Resumo do que vamos instalar

| Item | Para quê |
|---|---|
| WSL + Ubuntu | O sistema Linux dentro do Windows |
| Git | Baixar e versionar o código |
| Python 3 + `venv` + `pip` | Rodar o programa Python |
| PostgreSQL | Banco de dados onde os dados ficam salvos |
| Bibliotecas Python | `fastapi`, `uvicorn`, `psycopg2-binary`, `python-dotenv` |

---

## Passo 0 — Instalar o WSL e o Ubuntu (feito uma vez, no Windows)

Abra o **PowerShell como Administrador** (menu Iniciar → digite "PowerShell" →
"Executar como administrador") e rode:

```powershell
wsl --install -d Ubuntu
```

Isso instala o WSL e a distribuição Ubuntu. **Reinicie o computador** quando
ele pedir. Ao abrir o Ubuntu pela primeira vez, ele pede para você criar um
**usuário e senha do Linux** (não precisa ser igual ao do Windows). Guarde essa
senha: é ela que o `sudo` vai pedir.

> A partir daqui, **todos os comandos** são digitados **dentro do terminal do
> Ubuntu** (procure "Ubuntu" no menu Iniciar), não no PowerShell.

Confira a versão (o ideal é WSL 2):

```powershell
wsl --list --verbose
```

---

## Passo 1 — Atualizar o Ubuntu

Primeira coisa a fazer sempre num sistema novo: atualizar a lista de pacotes.

```bash
sudo apt update && sudo apt upgrade -y
```

- `apt` é o "instalador de programas" do Ubuntu.
- `sudo` = "faça isso como administrador" (vai pedir sua senha do Linux).

---

## Passo 2 — Git

O Git provavelmente já vem instalado. Garanta a versão mais recente e configure
seu nome e e-mail (aparecem nos seus commits):

```bash
sudo apt install -y git
git config --global user.name "Seu Nome"
git config --global user.email "seu-email@exemplo.com"
```

---

## Passo 3 — Python 3, venv e pip

O Ubuntu já traz o Python 3, mas precisamos garantir dois complementos:
`venv` (para criar ambientes isolados) e `pip` (para instalar bibliotecas).

```bash
sudo apt install -y python3 python3-venv python3-pip
```

Confira que instalou:

```bash
python3 --version      # deve mostrar algo como Python 3.10+
pip3 --version
```

> **Por que `venv`?** Um "ambiente virtual" é uma caixinha isolada por projeto,
> onde as bibliotecas ficam guardadas sem bagunçar o resto do sistema.

---

## Passo 4 — PostgreSQL (o banco de dados)

Instale o servidor e os utilitários:

```bash
sudo apt install -y postgresql postgresql-contrib
```

### 4.1 — Iniciar o serviço (IMPORTANTE no WSL)

No WSL, o PostgreSQL **não sobe sozinho** ao ligar o computador (diferente do
Linux comum). Você precisa iniciá-lo em cada sessão:

```bash
sudo service postgresql start
```

Para conferir se está no ar:

```bash
sudo service postgresql status
```

> **Dica:** se cansar de rodar isso toda vez, veja
> [Iniciar o PostgreSQL automaticamente](#iniciar-o-postgresql-automaticamente)
> no final.

### 4.2 — Criar o banco e o usuário do projeto

O PostgreSQL cria um usuário administrador chamado `postgres`. Vamos entrar como
ele e criar o banco e o usuário que este projeto usa.

Entre no console do banco:

```bash
sudo -u postgres psql
```

O prompt muda para `postgres=#`. Cole os comandos abaixo. **Use as mesmas
credenciais que estarão no seu `.env`** (aqui usamos as do `.env.example`):

```sql
CREATE DATABASE gestao_alunos;
CREATE USER curso WITH PASSWORD 'senha123';
GRANT ALL PRIVILEGES ON DATABASE gestao_alunos TO curso;

-- No PostgreSQL 15+, dê também permissão no schema public do banco:
\c gestao_alunos
GRANT ALL ON SCHEMA public TO curso;
```

Para sair do console do banco:

```sql
\q
```

> **Comandos úteis dentro do `psql`:** `\l` lista os bancos, `\c nome` conecta a
> um banco, `\dt` lista as tabelas, `\q` sai.

---

## Passo 5 — Criar o seu projeto a partir deste template

Este repositório é um **template**. Em vez de cloná-lo diretamente, crie o
**seu próprio** repositório a partir dele — assim o seu trabalho fica no seu
GitHub.

### 5.1 — Gerar o seu repositório

Na página deste repositório no GitHub, clique no botão verde
**"Use this template" → "Create a new repository"**. Dê um nome ao seu projeto
e crie. O GitHub gera um repositório novo, idêntico a este, mas **seu**.

### 5.2 — Configurar uma chave SSH (para clonar e enviar seu trabalho)

Para o Git conversar com o GitHub sem ficar pedindo senha, use uma chave SSH.
Se ainda não tiver uma:

```bash
ssh-keygen -t ed25519 -C "seu-email@exemplo.com"
```

Aperte Enter para aceitar o local padrão. Depois mostre a **chave pública**:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copie todo o texto e cadastre no GitHub em
**Settings → SSH and GPG keys → New SSH key**. Teste:

```bash
ssh -T git@github.com
```

### 5.3 — Clonar o SEU repositório

Troque `SEU-USUARIO` e `SEU-REPOSITORIO` pelos seus:

```bash
mkdir -p ~/Projetos && cd ~/Projetos
git clone git@github.com:SEU-USUARIO/SEU-REPOSITORIO.git
cd SEU-REPOSITORIO
```

> **Alternativa sem SSH (HTTPS):** use
> `git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git`. Para dar
> `push`, o GitHub pede um *token* de acesso pessoal em vez de senha.

A partir daqui, todos os comandos rodam **dentro da pasta do projeto**.

---

## Passo 6 — Ambiente virtual e bibliotecas

Dentro da pasta do projeto:

```bash
# Cria o ambiente virtual (uma vez)
python3 -m venv venv

# Ativa o ambiente (toda vez que for trabalhar no projeto)
source venv/bin/activate
```

Quando ativo, o nome `(venv)` aparece no início da linha do terminal.

Instale as dependências listadas no `requirements.txt`:

```bash
pip install -r requirements.txt
```

Isso instala: `fastapi`, `uvicorn`, `psycopg2-binary` e `python-dotenv`.

> **Por que `psycopg2-binary` e não `psycopg2`?** A versão `-binary` já vem
> compilada, então **não** exige instalar compiladores no sistema. Se um dia
> precisar da versão que compila do zero, aí sim instale antes:
> `sudo apt install -y build-essential libpq-dev python3-dev`.

Para **sair** do ambiente virtual quando terminar: `deactivate`.

---

## Passo 7 — Configurar o arquivo `.env`

O `.env` guarda as credenciais do banco **fora do código** (e fora do Git).
Copie o modelo e ajuste se necessário:

```bash
cp .env.example .env
```

Conteúdo esperado (bata com o que você criou no Passo 4.2):

```env
DB_HOST=localhost
DB_NAME=gestao_alunos
DB_USER=curso
DB_PASSWORD=senha123
```

> O `.env` **não** é versionado (está no `.gitignore`). Nunca comite senhas.

---

## Passo 8 — Rodar o projeto

> **Atenção:** este é um template em forma de **esqueleto**. A API só sobe
> depois que você implementar o código (comece pela Etapa 0 do
> [DESAFIOS.md](DESAFIOS.md)). Enquanto o `main.py` não tiver a variável
> `app`, o `uvicorn` vai reclamar que não encontra a aplicação — é esperado.

Antes de tudo: ambiente ativo e banco no ar.

```bash
source venv/bin/activate            # se ainda não estiver ativo
sudo service postgresql start       # garante o PostgreSQL rodando
```

Depois de implementar, suba a API (o startup deve criar as tabelas):

```bash
uvicorn main:app --reload
```

Com o servidor no ar, abra no navegador do Windows:

- <http://127.0.0.1:8000/docs> — documentação interativa (Swagger UI): dá para
  testar **todos** os endpoints clicando, sem escrever código.
- <http://127.0.0.1:8000> — mensagem de boas-vindas.

Para parar: `Ctrl + C`.

### Testar pela linha de comando

Com a API rodando em um terminal, abra **outro** terminal e rode o roteiro:

```bash
cd ~/Projetos/SEU-REPOSITORIO
bash testar_api.sh
```

O script exercita o caminho feliz e os erros esperados (201, 409, 404, 204).

---

## (Opcional) PostgreSQL via Docker, em vez de nativo

Se preferir não instalar o PostgreSQL no Ubuntu, dá para subir um contêiner
descartável (exige o **Docker Desktop** instalado no Windows com integração
WSL ativada):

```bash
docker run --name pg-curso -e POSTGRES_DB=gestao_alunos \
  -e POSTGRES_USER=curso -e POSTGRES_PASSWORD=senha123 \
  -p 5432:5432 -d postgres:16
```

Neste caso, **pule** o Passo 4 (instalação nativa). O banco fica disponível em
`localhost:5432`, igual ao nativo.

---

## Checklist de verificação

Rode cada comando e confira a saída:

```bash
git --version                       # Git instalado
python3 --version                   # Python 3.10+
source venv/bin/activate            # (venv) aparece no prompt
pip list | grep -iE "fastapi|uvicorn|psycopg2|dotenv"   # libs instaladas
sudo service postgresql status      # active (running)
psql -h localhost -U curso -d gestao_alunos -c "\dt"    # conecta e lista tabelas
```

Se todos passarem, o ambiente está pronto.

---

## Solução de problemas

**`sudo service postgresql start` diz "unrecognized service" ou não sobe.**
Confirme que o pacote instalou (`sudo apt install -y postgresql`) e tente
`sudo service postgresql restart`.

**`psql: could not connect to server` / conexão recusada.**
O serviço não está no ar. Rode `sudo service postgresql start`.

**`FATAL: password authentication failed for user "curso"`.**
A senha do `.env` não bate com a definida no banco. Reveja o Passo 4.2 (ou
`ALTER USER curso WITH PASSWORD 'senha123';` dentro do `sudo -u postgres psql`).

**`permission denied for schema public` ao criar tabelas (PostgreSQL 15+).**
Falta a permissão no schema. Dentro do `psql`:
`\c gestao_alunos` e depois `GRANT ALL ON SCHEMA public TO curso;`.

**`ModuleNotFoundError: No module named 'fastapi'` (ou psycopg2 etc).**
O ambiente virtual não está ativo, ou as libs não foram instaladas. Rode
`source venv/bin/activate` e reinstale com `pip install -r requirements.txt`.

**`error: externally-managed-environment` ao usar o `pip`.**
Você está instalando fora do `venv`. **Ative o ambiente** (`source
venv/bin/activate`) antes do `pip install`. Nunca use `--break-system-packages`.

**A porta 8000 já está em uso.**
Outra instância do `uvicorn` está rodando. Feche-a (`Ctrl + C` no terminal
dela) ou suba em outra porta: `uvicorn main:app --reload --port 8001`.

**`git clone` pede senha ou dá "Permission denied (publickey)".**
Sua chave SSH não está cadastrada no GitHub. Refaça o Passo 5.2 ou use a URL
HTTPS.

### Iniciar o PostgreSQL automaticamente

Para não rodar `sudo service postgresql start` toda vez, habilite o **systemd**
no WSL. Edite (ou crie) o arquivo `/etc/wsl.conf`:

```bash
sudo nano /etc/wsl.conf
```

Adicione:

```ini
[boot]
systemd=true
```

Salve (`Ctrl+O`, Enter, `Ctrl+X`), e no **PowerShell do Windows** reinicie o
WSL:

```powershell
wsl --shutdown
```

Abra o Ubuntu de novo. Com systemd ativo, você pode usar
`sudo systemctl enable --now postgresql` para o banco subir sempre.
