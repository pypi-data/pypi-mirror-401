# HOW TO USE CALIGN IN YOU WORFLOW

# Example usage of Calign package (PYTHON).


## This script demonstrates different ways to use the align_epitopes function.

# ==================================
# EXAMPLE 1: Basic Usage (Default settings)
# ==================================

from calign import align_epitopes

print("=" * 80)
print("EXAMPLE 1: Basic Usage")
print("=" * 80)

# variable that receives the epitope alignment function and a file with the target protein and a file containing all the predicted epitopes. 
result = align_epitopes(
    proteina_file="protein.fasta", 
    epitopos_file="epitopes.fasta"
)

# It only returns some data related to protein alignments and results.
print(f"Protein length: {len(result['protein_sequence'])} amino acids")
print(f"Number of epitopes in file: {len(result['epitopes'])}")
print(f"Number of matches found: {len(result['positions'])}")
print(f"Output files generated:")
print(f"  - {result['output_txt']}")
print(f"  - {result['output_png']}")

# ==============================
# EXAMPLE 2: Custom Output Paths
# ==============================
print("\n" + "=" * 80)
print("EXAMPLE 2: Custom Output Paths")
print("=" * 80)

result = align_epitopes(
    proteina_file="protein.fasta",
    epitopos_file="epitopes.fasta",
    output_txt="results/my_alignment.txt",
    output_png="results/my_heatmap.png",
    dpi=600,
    figsize=(16, 8)
)

print(f"✓ High-resolution outputs saved to 'results/' folder")

# ===========================
# EXAMPLE 3: Programmatic Access (No Files Generated)
# ===========================
print("\n" + "=" * 80)
print("EXAMPLE 3: Programmatic Access (No Files)")
print("=" * 80)

result = align_epitopes(
    proteina_file="protein.fasta",
    epitopos_file="epitopes.fasta",
    output_txt=None,
    output_png=None
)

print("\nEpitope positions found:")
for i, (start, end, epitope) in enumerate(result['positions'], 1):
    print(f"  {i}. Epitope '{epitope}' at position {start}-{end}")

print("\nAligned layers:")
for i, layer in enumerate(result['aligned_layers'], 1):
    print(f"  Layer {i}: {layer[:50]}...")  # Show first 50 characters

# =========================
# EXAMPLE 4: Display Plot
# =========================
print("\n" + "=" * 80)
print("EXAMPLE 4: Display Plot Interactively")
print("=" * 80)

result = align_epitopes(
    proteina_file="protein.fasta",
    epitopos_file="epitopes.fasta",
    show_plot=True  # This will display the plot window
)

print("✓ Plot displayed (close the window to continue)")

# ========================
# EXAMPLE 5: Using with Pathlib
# ========================
print("\n" + "=" * 80)
print("EXAMPLE 5: Using with Pathlib")
print("=" * 80)

from pathlib import Path

data_dir = Path("data")
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

result = align_epitopes(
    proteina_file=data_dir / "protein.fasta",
    epitopos_file=data_dir / "epitopes.fasta",
    output_txt=output_dir / "alignment.txt",
    output_png=output_dir / "heatmap.png"
)

print(f"✓ Files saved to: {output_dir.absolute()}")

# ==========================
# EXAMPLE 6: Error Handling
# ==========================
print("\n" + "=" * 80)
print("EXAMPLE 6: Error Handling")
print("=" * 80)

try:
    result = align_epitopes(
        proteina_file="nonexistent.fasta",
        epitopos_file="epitopes.fasta"
    )
except FileNotFoundError as e:
    print(f"✓ Correctly caught error: {e}")

try:
    result = align_epitopes(
        proteina_file="protein.fasta",
        epitopos_file="empty.fasta"  # File with no sequences
    )
except ValueError as e:
    print(f"✓ Correctly caught error: {e}")

# =========================
# EXAMPLE 7: Using in a Loop (Multiple Analyses)
# =========================
print("\n" + "=" * 80)
print("EXAMPLE 7: Batch Processing")
print("=" * 80)

proteins = ["protein1.fasta", "protein2.fasta", "protein3.fasta"]
epitopes_file = "epitopes.fasta"

for i, protein_file in enumerate(proteins, 1):
    try:
        result = align_epitopes(
            proteina_file=protein_file,
            epitopos_file=epitopes_file,
            output_txt=f"batch_results/alignment_{i}.txt",
            output_png=f"batch_results/heatmap_{i}.png"
        )
        print(f"✓ Processed {protein_file}: {len(result['positions'])} matches")
    except FileNotFoundError:
        print(f"✗ Skipped {protein_file}: File not found")

print("\n" + "=" * 80)
print("All examples completed!")
print("=" * 80)

#   How to use in jupyter notebook
[see a notebook](https://github.com/labiomol/Calign-development/blob/main/notebooks/how_to_use_calign.ipynb)
