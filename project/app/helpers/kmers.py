from typing import List

def find_kmers(seq: str, k: int) -> List[str]:
    """Find k-mers in string"""

    n = len(seq) - k + 1
    return [] if n < 1 else [seq[i:i+k] for i in range(n)]
