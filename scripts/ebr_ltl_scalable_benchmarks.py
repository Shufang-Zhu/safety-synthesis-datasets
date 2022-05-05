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
    files = list(formula_seeds_folder.glob("./*.conjtlsf"))
    for file in files:
        original_formula_file = formula_seeds_folder_str+"/"+file.name
        formula_file = save_str+"/"+file.parent.stem+"/"+file.stem+".conjltl"
        part_file = save_str+"/"+file.parent.stem+"/"+file.stem+".part"
        cmd = "syfco -f ltl -m fully "+original_formula_file+" -o "+formula_file+" -pf "+part_file
        tlsf_formula = Path(original_formula_file).read_text()
        tlsf_file = save_str+"/"+file.parent.stem+"/"+file.stem+".conjtlsf"
        Path(tlsf_file).write_text(tlsf_formula)
        print(cmd)
        os.system(cmd)

    files = list(formula_seeds_folder.glob("./*.Xtlsf"))
    for file in files:
        original_formula_file = formula_seeds_folder_str + "/" + file.name
        formula_file = save_str + "/" + file.parent.stem + "/" + file.stem + ".Xltl"
        part_file = save_str + "/" + file.parent.stem + "/" + file.stem + ".part"
        cmd = "syfco -f ltl -m fully " + original_formula_file + " -o " + formula_file + " -pf " + part_file
        tlsf_formula = Path(original_formula_file).read_text()
        tlsf_file = save_str + "/" + file.parent.stem + "/" + file.stem + ".Xtlsf"
        Path(tlsf_file).write_text(tlsf_formula)

        formula = Path(formula_file).read_text()
        partition = Path(part_file).read_text()
        partition.strip("\n")
        substr = partition.split("\n")
        ins = substr[0].split(" ")[1:]
        outs = substr[1].split(" ")[1:]
        strix_ins = ""
        for prop in ins:
            strix_ins = strix_ins + prop + ","
        strix_ins = strix_ins[:-1]
        strix_outs = ""
        for prop in outs:
            strix_outs = strix_outs + prop + ","
        strix_outs = strix_outs[:-1]
        singularity_file = save_str + "/" + file.parent.stem + "/" + file.stem + "_strix.sh"
        singularity_cmd = "time -p bin/strix -f \""+ formula+"\" --ins="+strix_ins+" --outs="+strix_outs
        Path(singularity_file).write_text(singularity_cmd)
        print(cmd)
        os.system(cmd)


def generate_tlsf_seeds(real_1, real_2, unreal_1, unreal_2):
    cmd_real_1 = "python3 scripts/scalable-benchmarks/gen_real_1.py -f tlsf -s 2 -e "+str(real_1)
    os.system(cmd_real_1)

    cmd_real_2 = "python3 scripts/scalable-benchmarks/gen_real_2.py -f tlsf -s 2 -e " + str(real_2)
    os.system(cmd_real_2)

    cmd_unreal_1 = "python3 scripts/scalable-benchmarks/gen_unreal_1.py -f tlsf -s 2 -e " + str(unreal_1)
    os.system(cmd_unreal_1)

    cmd_unreal_2 = "python3 scripts/scalable-benchmarks/gen_unreal_2.py -f tlsf -s 2 -e " + str(unreal_2)
    os.system(cmd_unreal_2)

def generate_dataset():
    ebr_ltl_scalable("Dataset_seeds/scalable-benchmarks/real_1", "EBR_LTL/Scalable")
    ebr_ltl_scalable("Dataset_seeds/scalable-benchmarks/real_2", "EBR_LTL/Scalable")
    ebr_ltl_scalable("Dataset_seeds/scalable-benchmarks/unreal_1", "EBR_LTL/Scalable")
    ebr_ltl_scalable("Dataset_seeds/scalable-benchmarks/unreal_2", "EBR_LTL/Scalable")


if __name__ == "__main__":
    generate_tlsf_seeds(200, 200, 200, 200)
    generate_dataset()
