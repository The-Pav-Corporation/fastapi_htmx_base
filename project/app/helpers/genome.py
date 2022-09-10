from typing import Generator

import logging

_logger = logging.getLogger("uvicorn.error")

def skew(genome: str) -> Generator[int, None, None]:
    difference = 0
    for nucleotide in genome.lower():
        if nucleotide == "g":
            difference += 1
        elif nucleotide == "c":
            difference -= 1
        _logger.debug(f"{nucleotide} - {difference}")
        yield difference

