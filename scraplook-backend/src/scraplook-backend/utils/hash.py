"""
Utility module to provide methods linked to hash strategy.
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_str_chain(str_chain: str) -> str:
    """
    Hash str chain.

    Args:
        str_chain: String chain to hash.

    Returns: Hash str.

    """
    return pwd_context.hash(str_chain)
