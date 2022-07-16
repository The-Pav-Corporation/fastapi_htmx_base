import logging

from functools import partial
from typing import List, Callable
from collections import Counter
from itertools import chain

_logger = logging.getLogger("uvicorn.error")

def binary_search(f: Callable, low: int, high: int):
    """Binary search"""

    hi, lo = f(high), f(low)
    mid = (high + low) // 2

    if hi and lo:
        return high

    if lo:
        return binary_search(f, low, mid)

    if hi:
        return binary_search(f, mid, high)
    
    return -1

def get_kmers(seq: str, k: int) -> List[str]:
    """Get all k-mers in string"""

    n = len(seq) - k + 1
    return [] if n < 1 else [seq[i:i+k] for i in range(n)]

def common_kmers(seqs: List[str], k: int):
    """Get all k-mers common to all sequences"""
    kmers = [set(get_kmers(seq, k)) for seq in seqs]
    counts = Counter(chain.from_iterable(kmers))
    n = len(seqs)
    return [kmer for kmer, freq in counts.items() if freq == n]

def common_kmer(seqs: List[str]) -> str:
    """Get first common kmer in all records"""

    shortest_len = min(len(seq) for seq in seqs)

    # find starting point
    common = partial(common_kmers, seqs)
    _logger.debug(common)
    start = binary_search(common, 1, shortest_len)
    _logger.debug(f"start - {start}")

    if start >= 0:
        # Hill climb to find max
        candidates = []
        for k in range(start, shortest_len+1):
            if kmers := common(k):
                candidates.append(kmers[0])
                _logger.debug(f"{k} - {candidates}")
            else:
                break
        return f"{max(candidates, key=len)}"
    else:
        return "No common sequence"