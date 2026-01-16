"""
Core functionality for Calign package.

This module provides the main epitope alignment functionality, including:
- Reading FASTA files with protein and epitope sequences
- Finding epitope positions in protein sequences
- Organizing epitopes into non-overlapping layers
- Generating text output with aligned epitopes
- Creating heatmap visualizations

Author: André Luiz Caliari Costa (biologist and bioinformatician)
License: Proprietary - All rights reserved. Please read the EULA to know how to use it.
"""

import numpy as np
from Bio import SeqIO
import re
import heapq
import sys
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for compatibility
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Tuple, Optional, Union, Dict


def _ler_sequencias_fasta(nome_arquivo: Union[str, Path]) -> List[str]:
    
    arquivo_path = Path(nome_arquivo)
    
    # Check if file exists
    if not arquivo_path.exists():
        raise FileNotFoundError(
            f"File not found: {nome_arquivo}\n"
            f"Please check if the file exists and the path is correct."
        )
    
    # Check if file is empty
    if arquivo_path.stat().st_size == 0:
        raise ValueError(f"File {nome_arquivo} is empty.")
    
    try:
        sequencias = [str(registro.seq) for registro in SeqIO.parse(str(arquivo_path), "fasta")]
        
        if not sequencias:
            raise ValueError(
                f"File {nome_arquivo} contains no valid sequences.\n"
                f"Please ensure the file is in valid FASTA format."
            )
        
        return sequencias
        
    except Exception as e:
        if isinstance(e, (FileNotFoundError, ValueError)):
            raise
        raise RuntimeError(
            f"Error reading file {nome_arquivo}: {str(e)}\n"
            f"Please ensure the file is in valid FASTA format."
        )


def _encontrar_posicoes_epitopos(sequencia_proteina: str, 
                                  epitopos: List[str]) -> List[Tuple[int, int, str]]:
    posicoes = []
    
    for epitopo in epitopos:
        # Use re.escape to handle special regex characters in epitope sequences
        pattern = re.escape(epitopo)
        
        # Find all occurrences
        for match in re.finditer(pattern, sequencia_proteina):
            inicio = match.start()
            fim = match.end()
            posicoes.append((inicio, fim, epitopo))
    
    return posicoes


def _organizar_epitopos_em_camadas_otimizado(sequencia_proteina: str, 
                                              posicoes_epitopos: List[Tuple[int, int, str]]) -> List[str]:
    
    # Sort epitopes by starting position
    posicoes_ordenadas = sorted(posicoes_epitopos, key=lambda x: x[0])
    
    camadas = []                # List of layers (each is a list of characters)
    heap_ativo = []             # Min-heap of active intervals [(end_position, layer_id)]
    
    for inicio, fim, epitopo in posicoes_ordenadas:
        # Release layers whose intervals have ended
        while heap_ativo and heap_ativo[0][0] <= inicio:
            heapq.heappop(heap_ativo)
        
        # Find an available layer
        camadas_ocupadas = {camada_id for _, camada_id in heap_ativo}
        camada_livre = None
        
        for i in range(len(camadas)):
            if i not in camadas_ocupadas:
                camada_livre = i
                break
        
        # If no layer is available, create a new one
        if camada_livre is None:
            camada_livre = len(camadas)
            camadas.append([" "] * len(sequencia_proteina))
        
        # Place the epitope in the chosen layer
        for i, letra in enumerate(epitopo):
            camadas[camada_livre][inicio + i] = letra
        
        # Mark the end of this epitope in the heap
        heapq.heappush(heap_ativo, (fim, camada_livre))
    
    # Remove completely empty layers and convert to strings
    return ["".join(linha) for linha in camadas if any(c != " " for c in linha)]


def align_epitopes(proteina_file: Union[str, Path],
                   epitopos_file: Union[str, Path],
                   output_txt: Optional[Union[str, Path]] = "resultado_epitopos.txt",
                   output_png: Optional[Union[str, Path]] = "heatmap_epitopos.png",
                   dpi: int = 300,
                   figsize: Tuple[int, int] = (12, 6),
                   show_plot: bool = False) -> Dict[str, any]:
    
    # ==========================================================================
    # PHASE 1: Read and validate input files
    # ==========================================================================
    
    try:
        # Read protein sequence (expect exactly one sequence)
        sequencias_proteina = _ler_sequencias_fasta(proteina_file)
        if len(sequencias_proteina) > 1:
            print(f"Warning: Protein file contains {len(sequencias_proteina)} sequences. Using only the first one.")
        sequencia_proteina = sequencias_proteina[0]
        
        # Read epitopes (can be multiple)
        epitopos = _ler_sequencias_fasta(epitopos_file)
        
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"{str(e)}\n\n"
            f"Please ensure both files exist:\n"
            f"  - Protein file: {proteina_file}\n"
            f"  - Epitopes file: {epitopos_file}"
        )
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise RuntimeError(f"Unexpected error reading input files: {str(e)}")
    
    # Validate sequences
    if not sequencia_proteina:
        raise ValueError("Protein sequence is empty.")
    
    if len(sequencia_proteina) < 1:
        raise ValueError("Protein sequence is too short (minimum length: 1).")
    
    # ==========================================================================
    # PHASE 2: Find epitope positions
    # ==========================================================================
    
    posicoes_epitopos = _encontrar_posicoes_epitopos(sequencia_proteina, epitopos)
    
    if not posicoes_epitopos:
        raise ValueError(
            f"No epitopes found in the protein sequence.\n"
            f"Protein length: {len(sequencia_proteina)} amino acids\n"
            f"Number of epitopes searched: {len(epitopos)}\n"
            f"Please verify that the epitope sequences are present in the protein."
        )
    
    # ==========================================================================
    # PHASE 3: Organize epitopes into non-overlapping layers
    # ==========================================================================
    
    linhas_epitopos = _organizar_epitopos_em_camadas_otimizado(sequencia_proteina, posicoes_epitopos)
    
    # ==========================================================================
    # PHASE 4: Generate text output 
    # ==========================================================================
    
    output_txt_path = None
    if output_txt is not None:
        try:
            output_txt_path = Path(output_txt)
            
            # Create parent directories if they don't exist
            output_txt_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_txt_path, "w", encoding="utf-8") as arquivo_saida:
                arquivo_saida.write("Sequência da Proteína:\n")
                arquivo_saida.write(sequencia_proteina + "\n")
                arquivo_saida.write("\nEpítopos Alinhados:\n")
                for linha in linhas_epitopos:
                    arquivo_saida.write(linha + "\n")
                
                # Add summary statistics
                arquivo_saida.write(f"\n{'='*80}\n")
                arquivo_saida.write("RESUMO / SUMMARY\n")
                arquivo_saida.write(f"{'='*80}\n")
                arquivo_saida.write(f"Comprimento da proteína / Protein length: {len(sequencia_proteina)} aminoácidos\n")
                arquivo_saida.write(f"Número de epítopos / Number of epitopes: {len(epitopos)}\n")
                arquivo_saida.write(f"Total de matches encontrados / Total matches found: {len(posicoes_epitopos)}\n")
                arquivo_saida.write(f"Número de camadas / Number of layers: {len(linhas_epitopos)}\n")
            
            print(f"✓ Results saved to '{output_txt_path}'")
            
        except Exception as e:
            raise RuntimeError(f"Error writing text output file: {str(e)}")
    
    # ==========================================================================
    # PHASE 5: Generate heatmap visualization
    # ==========================================================================
    
    output_png_path = None
    if output_png is not None:
        try:
            output_png_path = Path(output_png)
            
            # Create parent directories if they don't exist
            output_png_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create heatmap matrix
            heatmap = np.zeros((len(epitopos), len(sequencia_proteina)), dtype=int)
            
            # Fill matrix with epitope positions
            epitopo_counts = {ep: 0 for ep in epitopos}
            for inicio, fim, epitopo in posicoes_epitopos:
                idx = epitopos.index(epitopo)
                heatmap[idx, inicio:fim] = 1
                epitopo_counts[epitopo] += 1
            
            # Create figure
            fig, ax = plt.subplots(figsize=figsize)
            
            # Plot heatmap
            im = ax.imshow(heatmap, aspect="auto", cmap="Reds", interpolation="nearest")
            
            # Set labels
            ax.set_xlabel("Protein Sequence Position", fontsize=12, fontweight='bold')
            #ax.set_ylabel("Epitopes", fontsize=12, fontweight='bold')
            ax.set_title(f"Epitope Alignment Heatmap\n({len(posicoes_epitopos)} matches, {len(linhas_epitopos)} layers)", 
                        fontsize=14, fontweight='bold', pad=20)
            
            # Set y-axis labels with epitope names (truncated if too long)
            y_labels = [ep[:20] + "..." if len(ep) > 20 else ep for ep in epitopos]
            ax.set_yticks([])
            ax.set_yticklabels([])
            
            # Add grid for better readability
            ax.set_xticks(np.arange(0, len(sequencia_proteina), max(1, len(sequencia_proteina)//10)))
            ax.grid(False)
            
            # Adjust layout
            plt.tight_layout()
            
            # Save figure
            plt.savefig(output_png_path, dpi=dpi, bbox_inches="tight", transparent=False)
            print(f"✓ Heatmap saved to '{output_png_path}'")
            
            # Show plot if requested
            if show_plot:
                plt.show()
            else:
                plt.close(fig)
                
        except Exception as e:
            plt.close('all')  # Clean up any open figures
            raise RuntimeError(f"Error generating heatmap: {str(e)}")
    
    # ==========================================================================
    # PHASE 6: Return results
    # ==========================================================================
    
    return {
        'protein_sequence': sequencia_proteina,
        'epitopes': epitopos,
        'positions': posicoes_epitopos,
        'aligned_layers': linhas_epitopos,
        'output_txt': str(output_txt_path) if output_txt_path else None,
        'output_png': str(output_png_path) if output_png_path else None,
        'num_matches': len(posicoes_epitopos),
        'num_layers': len(linhas_epitopos)
    }


# =============================================================================
# Additional utility functions for advanced users
# =============================================================================

def get_epitope_coverage(result: Dict[str, any]) -> float:
    protein_length = len(result['protein_sequence'])
    covered_positions = set()
    
    for start, end, _ in result['positions']:
        covered_positions.update(range(start, end))
    
    coverage = (len(covered_positions) / protein_length) * 100
    return round(coverage, 2)


def get_epitope_statistics(result: Dict[str, any]) -> Dict[str, any]:
    protein_length = len(result['protein_sequence'])
    positions = result['positions']
    epitopes = result['epitopes']
    
    # Count occurrences per epitope
    epitope_counts = {}
    for _, _, ep in positions:
        epitope_counts[ep] = epitope_counts.get(ep, 0) + 1
    
    # Calculate coverage
    coverage = get_epitope_coverage(result)
    
    # Find overlapping epitopes
    sorted_positions = sorted(positions, key=lambda x: x[0])
    overlaps = 0
    for i in range(len(sorted_positions) - 1):
        if sorted_positions[i][1] > sorted_positions[i+1][0]:
            overlaps += 1
    
    return {
        'protein_length': protein_length,
        'total_epitopes': len(epitopes),
        'total_matches': len(positions),
        'unique_matches': len(epitope_counts),
        'coverage_percentage': coverage,
        'overlapping_pairs': overlaps,
        'layers_needed': result['num_layers'],
        'epitope_counts': epitope_counts,
        'average_epitope_length': round(sum(len(ep) for ep in epitopes) / len(epitopes), 2)
    }


# =============================================================================
# Module-level constants
# =============================================================================

__all__ = ['align_epitopes', 'get_epitope_coverage', 'get_epitope_statistics']