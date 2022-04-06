import random
import re
import  os
import click
from click import IntRange
from pathlib import Path

def ebr_ltl_scalable(formula_seeds_folder, save):
    save_str = save
    save = Path(save) / Path(formula_seeds_folder).stem
    save.mkdir(parents=True, exist_ok=True)
    formula_seeds_folder_str = formula_seeds_folder
    formula_seeds_folder = Path(formula_seeds_folder)
    files = list(formula_seeds_folder.glob("./*.tlsf"))
    for file in files:
        original_formula_file = formula_seeds_folder_str+"/"+file.name
        formula_file = save_str+"/"+file.parent.stem+"/"+file.stem+".ltl"
        part_file = save_str+"/"+file.parent.stem+"/"+file.stem+".part"
        cmd = "syfco -f ltl -m fully "+original_formula_file+" -o "+formula_file+" -pf "+part_file
        tlsf_formula = Path(original_formula_file).read_text()
        tlsf_file = save_str+"/"+file.parent.stem+"/"+file.stem+".tlsf"
        Path(tlsf_file).write_text(tlsf_formula)
        print(cmd)
        os.system(cmd)


if __name__ == "__main__":
    ebr_ltl_scalable("scripts/scalable-benchmarks/real_1_tlsf", "EBR_LTL_scalable")
    ebr_ltl_scalable("scripts/scalable-benchmarks/real_2_tlsf", "EBR_LTL_scalable")
    ebr_ltl_scalable("scripts/scalable-benchmarks/unreal_1_tlsf", "EBR_LTL_scalable")
    ebr_ltl_scalable("scripts/scalable-benchmarks/unreal_2_tlsf", "EBR_LTL_scalable")