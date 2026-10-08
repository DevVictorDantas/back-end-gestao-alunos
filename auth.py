import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()  # carrega variáveis do .env
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    # Sem a chave, nenhum token pode ser assinado: melhor falhar já no startup.
    raise RuntimeError("Defina SECRET_KEY no .env (ou nas variáveis do servidor).")

LIMITE_BCRYPT = 72

def criar_token(username: str) -> str:
    agora = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "exp": agora + timedelta(minutes=60),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def ler_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def _en_bytes(senha: str) -> bytes:
    return senha.encode("utf-8")[:LIMITE_BCRYPT]

def gerar_hash(senha: str) -> bytes:
    return bcrypt.hashpw(_en_bytes(senha), bcrypt.gensalt()).decode("utf-8")

def conferir_senha(senha: str, hash_guardado: str) -> bool:
    try:
        return bcrypt.checkpw(_en_bytes(senha), hash_guardado.encode("utf-8"))
    except ValueError:
        return False
    
HASH_FALSO = "$2b$12$eImiTXuWVxfM37uY4JANjOL.s88bh9M.D.7M.r39R4M7W1J.7m6vK"