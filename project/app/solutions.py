import logging
from Bio.Seq import Seq

_logger = logging.getLogger("uvicorn.error")


### Solutions: remember to register solutions at the bottom ###
### Test Solution ###
test_solution_title = "Test".lower()
def test_solution_func(input: str):
    return f"Here's your input: {input}"

### Counting DNA Nucleotides ###
counting_dna_title = "Counting DNA Nucleotides".lower()
def counting_dna(dna: str):
    acgt = [str(dna.count('A')), str(dna.count('C')), str(dna.count('G')), str(dna.count('T'))]
    return " ".join(acgt)

### Transcribing DNA into RNA ###
transcribing_dna_title = "Transcribing DNA into RNA".lower()
def transcribe(dna: str):
    return dna.replace('T', 'U')

### Complementing a Strand of DNA ###
complementing_dna_title = "Complementing a Strand of DNA".lower()
def complement_dna(dna: str):
    sequence = Seq(dna)
    return str(sequence.reverse_complement())
    

### Add solutions to dict ###
solutions = {
    test_solution_title: test_solution_func,
    counting_dna_title: counting_dna,
    transcribing_dna_title: transcribe,
    complementing_dna_title: complement_dna,
}