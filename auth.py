import bcrypt

LIMITE_BCRYPT = 72

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