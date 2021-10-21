import random
import re

import click
from click import  IntRange
from pathlib import Path

def process_formula(formula_seeds_folder, save):
    save = Path(save) / Path(formula_seeds_folder).stem
    save.mkdir(parents=True, exist_ok=True)
    formula_seeds_folder = Path(formula_seeds_folder)
    files = list(formula_seeds_folder.glob("./*.ltl"))
    for file in files:
        content = file.read_text()
        content = content.replace("Grant", "grant")
        content = content.replace("Request", "request")
        new_file = save / Path(file.stem + ".ltl")
        new_file.write_text(content)

def process_partition(partition_seeds_folder, save):
    save = Path(save) / Path(partition_seeds_folder).stem
    save.mkdir(parents=True, exist_ok=True)
    formula_seeds_folder = Path(partition_seeds_folder)
    files = list(formula_seeds_folder.glob("./*.part"))
    for file in files:
        content = file.read_text()
        content = content.lower()
        new_file = save / Path(file.stem + ".part")
        new_file.write_text(content)



if __name__ == "__main__":
    process_formula("Basic/SSyft_1", "Processed")
    process_formula("Basic/SSyft_2", "Processed")
    process_formula("Basic/SSyft_3", "Processed")
    process_formula("Basic/SSyft_4", "Processed")
    process_formula("Basic/SSyft_5", "Processed")
    process_partition("Basic/SSyft_part", "Processed")