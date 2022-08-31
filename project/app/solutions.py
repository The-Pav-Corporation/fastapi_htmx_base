import logging
from Bio.Seq import Seq, translate
from Bio.SeqUtils import GC
from collections import defaultdict, Counter
from itertools import zip_longest
from itertools import product

from .helpers.fib import fib, mortal_fib
from .helpers.fasta import parse_fasta_string
from .helpers.kmers import get_kmers

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

### Rabbits and Recurrence Relations ###
rabbits_and_recurrence_title = "Rabbits and Recurrence Relations".lower()
def rabbits_fib(input: str):
    input_vals = [int(x) for x in input.split(" ")]
    generations = input_vals[0]
    litter = input_vals[1]
    gen = fib(litter)
    answer = 0
    for _ in range(generations + 1):
        answer = next(gen)
    return f'{answer}'

mortal_rabbits_title = "Mortal Fibonacci Rabbits".lower()
def mortal_rabbits_fib(input: str):
    input_vals = [int(x) for x in input.split(" ")]
    generations = input_vals[0]
    lifespan = input_vals[1]
    gen = mortal_fib(lifespan)
    answer = 0
    for _ in range(generations):
        answer = next(gen)
    return f'{answer}'

### Computing GC Content ###
gc_content_title = "Computing GC Content".lower()
def gc_content(input: str):
    records = parse_fasta_string(input)
    max_gc = 0.0
    max_gc_holder = ""
    for record in records:
        item_gc = GC(records[record])
        if item_gc > max_gc:
            max_gc, max_gc_holder = item_gc, record
    return f"{max_gc_holder} - {max_gc:.6f}"

### Counting Point Mutations ###
counting_point_mutations_title = "Counting Point Mutations".lower()
def point_mutations(input: str):
    dna_list = list(input.split(" "))
    return str(sum(n1 != n2 for n1, n2 in zip_longest(dna_list[0], dna_list[1])))

### Mendel's First Law ###
mendels_first_law = "Mendel's First Law".lower()
def pr_dom(input: str):
    """Three positive integers k, m, and n, representing a population containing
    k+m+n organisms: k individuals are homozygous dominant for a factor,
    m are heterozygous, and n are homozygous recessive."""
    input_list = list(input.split(" "))
    k, m, n = int(input_list[0]), int(input_list[1]), int(input_list[2])
    total = k + m + n
    pr_mate = sum([
        (k/total) * ((k-1)/(total-1)),  # kk
        (k/total) * (m/(total-1)),  # km
        (k/total) * (n/(total-1)),  # kn
        (m/total) * (k/(total-1)),  # mk
        ((m/total) * ((m-1)/(total-1))) * 3/4,  # mm
        ((m/total) * (n/(total-1))) * 1/2,  # mn
        (n/total) * (k/(total-1)),  # nk
        ((n/total) * (m/(total-1))) * 1/2,  # nm
        ((n/total) * ((n-1)/(total-1))) * 0,  # nn
    ])
    return f"{pr_mate:.5f}"

### Translating RNA into Protein ###
translating_rna_title = "Translating RNA into Protein".lower()
def translating_rna(input: str):
    return f"{translate(input).strip('*')}"

### Finding a Motif in DNA ###
motifs_title = "Finding a Motif in DNA".lower()
def get_motifs(input: str):
    input_list = list(input.split(" "))
    dna = input_list[0]
    motif = input_list[1]
    positions = [
        str(position)
        for position, n in enumerate(range(len(dna) - len(motif)), start=1)
        if dna[n : n + len(motif)] == motif
    ]

    return f"{' '.join(positions)}"

### Consensus and Profile ###
consensus_profile_title = "Consensus and Profile".lower()
def consensus_profile(input: str):
    recs = parse_fasta_string(input)
    records = list(recs.values())
    profile = {"A": [], "C": [], "G": [], "T": []}
    verticals = {
        i: [record[i] for record in records]
        for i in range(len(records[0]))
    }
    for v in verticals.values():
        profile['A'].append(v.count('A'))
        profile['C'].append(v.count('C'))
        profile['G'].append(v.count('G'))
        profile['T'].append(v.count('T'))

    consensus = ""
    for i in range(len(profile["A"])):
        max_score = max(profile["A"][i], profile["C"][i], profile["G"][i], profile["T"][i])
        for n in "ACGT":
            if profile[n][i] == max_score:
                consensus += n
                break

    profile_str = {"A": [], "C": [], "G": [], "T": []}
    for symbol, value in profile.items():
        for score in value:
            profile_str[symbol] += str(score)
    profile_format = f"""A: {' '.join(profile_str['A'])}
    C: {' '.join(profile_str['C'])}
    G: {' '.join(profile_str['G'])}
    T: {' '.join(profile_str['T'])}
    """
    return f"""{consensus}\n{profile_format}"""

# Overlap Graphs
overlap_graphs_title = "Overlap Graphs".lower()
def overlap_graphs(input: str):
    k = 3
    recs = parse_fasta_string(input)

    # get start and end kmers and list of records for them
    start, end = defaultdict(list), defaultdict(list)
    for key, rec in recs.items():
        if kmers := get_kmers(rec, k):
            start[kmers[0]].append(key)
            end[kmers[-1]].append(key)

    # for each common kmer in start and finish, exclude same record
    output = ""
    for kmer in set(start).intersection(set(end)):
        for pair in product(end[kmer], start[kmer]):
            if pair[0] != pair[1]:
                output += " ".join(pair) + "\n"
    return output

# Stepik problems
frequent_words_title = "Frequent Words Problem".lower()
def frequent_words(input: str):
    dna = input.split(" ")[0]
    k = input.split(" ")[1]
    kmers = get_kmers(dna, k)
    kmers_counts = Counter(kmers)
    most_common = kmers_counts.most_common(1)[0][0]
    return f"{most_common}"

pattern_matching_title = "Pattern Matching Problem".lower()
def pattern_matching(input: str):
    pattern = input.split(" ")[0].lower()
    genome = input.split(" ")[1].lower()
    limit = len(genome)-len(pattern)+1
    indexes = [str(i) for i in range(limit) if pattern == genome[i:i+len(pattern)]]
    return f"{', '.join(indexes) or 'Pattern not found.'}"

clump_finding_title = "Clump Finding Problem".lower()
def clump_finding(input: str):
    genome = input.split(" ")[0]
    k = int(input.split(" ")[1])
    L = int(input.split(" ")[2])
    t = int(input.split(" ")[3])
    clump = []
    for i in range(len(genome)-L):
        window = genome[i:i+L]
        kmers = get_kmers(window, k)
        kmers_counts = Counter(kmers)
        clump.extend(kmer for kmer, count in dict(kmers_counts).items() if count >= t)
    clump_set = set(clump)
    return f"{' '.join(clump_set)}"

### Add solutions to dict ###
solutions = {
    # Rosalind below
    test_solution_title: test_solution_func,
    counting_dna_title: counting_dna,
    transcribing_dna_title: transcribe,
    complementing_dna_title: complement_dna,
    rabbits_and_recurrence_title: rabbits_fib,
    gc_content_title: gc_content,
    counting_point_mutations_title: point_mutations,
    mendels_first_law: pr_dom,
    translating_rna_title: translating_rna,
    motifs_title: get_motifs,
    consensus_profile_title: consensus_profile,
    mortal_rabbits_title: mortal_rabbits_fib,
    overlap_graphs_title: overlap_graphs,
    # Stepik below
    frequent_words_title: frequent_words,
    pattern_matching_title: pattern_matching,
    clump_finding_title: clump_finding,
}