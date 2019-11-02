from typing import List

def to_n_gram(target: str, n: int) -> List[str]:
    return [ target[idx:idx + n] for idx in range(len(target) - n + 1)]
