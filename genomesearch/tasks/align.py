import os

from Bio import SeqIO
from Bio.Align import PairwiseAligner
from Bio.Seq import Seq
from celery import group
from celery.result import allow_join_result

from genome_finder import genomes
from genomesearch.celery import app


@app.task
def align_to_all(sequence: str):
    """
    Aligns a sequence to all genomes in the database, returning information on the first close
    match.Calls the celery "align" task for each genome, and returns the first alignment found,
    canceling any pending tasks. If no alignment is found, returns an error message.

    Args:
        sequence: DNA sequence to align to all genomes in the database.
    
    Returns:
        Dictionary with information on the first close match, or an error message if no alignment
        is found.
    
    """
    subtasks = [
        align.s(sequence, genome_name).set(queue='subtask_queue')
        for genome_name in get_genome_filenames()
    ]
    group_results = group(subtasks).apply_async()
    with allow_join_result():
        for i, result in enumerate(group_results.join()):
            if result: # we found a match
                for result in group_results: # don't search anywhere else after alignment is found
                    app.control.revoke(result.task_id, terminate=True)
                return group_results[i].result
    return {"sequence": sequence, "error": "No alignment found"} # no alignment found

@app.task
def align(sequence: str, genome_name: str):
    """
    Business logic for sequence alignment of a DNA sequence against a provided genome Genbank file.
    Aligns each gene to the target sequence, returning the first close match found. Note: This does
    not necessarily search all genes, and stops at the first close match found. 

    Args:
        sequence: DNA sequence to align to the genome. 
        genome_name: Filename of the Gernbank file genome to align against.
    
    Returns:
        result_data: {
            "input_sequence": str,
            "genome": str,
            "gene_name": str,
            "score": float,
            "startbp_sample": int,
            "endbp_sample": int,
            "startbp_genome": int,
            "endbp_genome": int
        }
        
    """
    nucleotide_sequence = Seq(sequence)
    path = f"genome_finder/genomes/{genome_name}"
    genome = SeqIO.read(os.path.join(os.getcwd(), path), "genbank")
    aligner = PairwiseAligner()
    aligner.mode = 'local'
    aligner.open_gap_score = -30
    aligner.extend_gap_score = -10
    aligner.mismatch_score = -1
    aligner.match_score = 1
    minimum_match_pct = 0.95

    for feature in genome.features:
        if feature.type == "CDS":
            gene_name = feature.qualifiers.get("gene", [""])[0]
            gene_sequence = feature.extract(genome.seq)
            alignments = aligner.align(nucleotide_sequence, gene_sequence)
            if alignments: # return only first found alignment
                score = alignments[0].score
                if score > len(nucleotide_sequence) * minimum_match_pct:
                    result_data =  {
                        "input_sequence": sequence,
                        "genome": genome_name,
                        "gene_name": gene_name,
                        "score": float(alignments[0].score)
                    }
                    indices = get_indices(alignments[0].indices, feature.location.start)
                    result_data.update(indices)
                    return result_data
    return None

def get_genome_filenames():
    """
    Fetch all genomes to align against. Replace this with a database query in a real application.
    """
    directory = os.path.dirname(genomes.__file__)
    return [filename for filename in os.listdir(directory) if filename.endswith('.gb')]

def get_indices(indices, start_bp):
    """
    Helper function to get only the relevant indices for the alignment return value. 
    """
    return {
        "startbp_sample": int(indices[0][0]) + 1,
        "endbp_sample": int(indices[0][-1]) + 1,
        "startbp_genome": int(indices[1][0]) + start_bp + 1,
        "endbp_genome": int(indices[1][-1]) + start_bp + 1,
    }
