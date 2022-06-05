# See from Bio.SeqIO.FastaIO import SimpleFastaParser to make it faster
def parse_fasta_string(input: str) -> dict[str]:
    phrase = input.split(" ")
    records = {}
    for word in phrase:
        if word[0] == ">":
            title = word[1:]
            part = ""
        else:
            part += word
            records[title] = "".join(part)
    return records