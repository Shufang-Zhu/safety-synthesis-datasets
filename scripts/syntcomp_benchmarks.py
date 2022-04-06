import random
import re
import  os
import click
from click import IntRange
from pathlib import Path
import subprocess as sp
import spot

def syntcomp(formula_seeds_folder, tlsf_formula_seeds_folder, save):
    save_str = save

    save = Path(save) / Path(formula_seeds_folder).stem
    save.mkdir(parents=True, exist_ok=True)
    formula_seeds_folder_str = formula_seeds_folder
    formula_seeds_folder = Path(formula_seeds_folder)

    tlsf_formula_seeds_folder_str = tlsf_formula_seeds_folder
    tlsf_formula_seeds_folder = Path(tlsf_formula_seeds_folder)

    files = list(formula_seeds_folder.glob("./*.smv"))
    for file in files:
        smv_formula_file = formula_seeds_folder_str+"/"+file.name
        smv_formula = Path(smv_formula_file).read_text()

        tlsf_formula_file = tlsf_formula_seeds_folder_str + "/" + file.stem + "_canonized.tlsf"

        formula_file = save_str + "/" + file.parent.stem + "/" + file.stem + ".ltl"
        part_file = save_str + "/" + file.parent.stem + "/" + file.stem + ".part"


        spot_formula = spot.formula(smv_formula)
        props = spot.atomic_prop_collect(spot_formula)

        rename_props = {}
        for prop in props:
            new_name = prop.to_str().lower()
            rename_props[prop.to_str()] = new_name

        formula_str = "(" + "{0:p}".format(spot_formula) + ")"
        # print(formula_str)
        for prop in rename_props.keys():
            formula_str = formula_str.replace("("+prop+")", rename_props[prop])


        formula_str = formula_str.replace("|", "||")
        formula_str = formula_str.replace("&", "&&")
        formula_str = formula_str.replace("X", "X ")
        formula_str = formula_str.replace("F", "F ")
        formula_str = formula_str.replace("G", "G ")
        formula_str = formula_str.replace("U", "U ")
        formula_str = formula_str.replace("R", "R ")

        Path(formula_file).write_text(formula_str)

        ins_cmd = "syfco -f ltl -m fully " + tlsf_formula_file + " -ins"
        # print(ins_cmd)
        ins = sp.getoutput(ins_cmd)
        # print(ins)
        ins_vec = ins.split(", ")
        # print(ins_vec)
        part_ins = ".inputs "
        for input in ins_vec:
            if input in rename_props.keys():
                part_ins = part_ins + input + " "
        for prop in rename_props.keys():
            part_ins = part_ins.replace(prop, rename_props[prop])


        outs_cmd = "syfco -f ltl -m fully " + tlsf_formula_file + " -outs"
        # print(outs_cmd)
        outs = sp.getoutput(outs_cmd)
        # print(outs)
        # print(rename_props)

        outs_vec = outs.split(", ")
        part_outs = ".outputs "
        for output in outs_vec:
            if output in rename_props.keys():
                part_outs = part_outs + output + " "
        for prop in rename_props.keys():
            part_outs = part_outs.replace(prop, rename_props[prop])

        part_str = part_ins[:-1] + "\n" + part_outs[:-1] + "\n"
        Path(part_file).write_text(part_str)

def syntcomp_env(formula_seeds_folder, tlsf_formula_seeds_folder, save):
    save_str = save

    save = Path(save) / Path(formula_seeds_folder).stem
    save.mkdir(parents=True, exist_ok=True)
    formula_seeds_folder_str = formula_seeds_folder
    formula_seeds_folder = Path(formula_seeds_folder)

    tlsf_formula_seeds_folder_str = tlsf_formula_seeds_folder
    tlsf_formula_seeds_folder = Path(tlsf_formula_seeds_folder)

    files = list(formula_seeds_folder.glob("./*.smv"))
    for file in files:
        smv_formula_file = formula_seeds_folder_str+"/"+file.name
        smv_formula = Path(smv_formula_file).read_text()

        tlsf_formula_file = tlsf_formula_seeds_folder_str + "/" + file.stem + "_canonized.tlsf"

        formula_file = save_str + "/" + file.parent.stem + "/" + file.stem + ".ltl"
        part_file = save_str + "/" + file.parent.stem + "/" + file.stem + ".part"


        spot_formula = spot.formula(smv_formula)
        props = spot.atomic_prop_collect(spot_formula)

        rename_props = {}
        for prop in props:
            new_name = prop.to_str().lower()
            rename_props[prop.to_str()] = new_name

        formula_str = "(" + "{0:p}".format(spot_formula) + ")"
        # print(formula_str)
        for prop in rename_props.keys():
            formula_str = formula_str.replace("("+prop+")", "("+rename_props[prop]+")")


        formula_str = formula_str.replace("|", "||")
        formula_str = formula_str.replace("&", "&&")
        formula_str = formula_str.replace("X", "X ")
        formula_str = formula_str.replace("F", "F ")
        formula_str = formula_str.replace("G", "G ")
        formula_str = formula_str.replace("U", "U ")
        formula_str = formula_str.replace("R", "R ")


        ins_cmd = "syfco -f ltl -m fully " + tlsf_formula_file + " -ins"
        # print(ins_cmd)
        ins = sp.getoutput(ins_cmd)
        # print(ins)
        ins_vec = ins.split(", ")

        part_ins = ".inputs "
        for input in ins_vec:
            if input in rename_props.keys():
                part_ins = part_ins + rename_props[input] + " "
                formula_str = formula_str.replace("(" + rename_props[input] + ")", "(X(" + rename_props[input] + "))")
        # for prop in rename_props.keys():
        #     part_ins = part_ins.replace(prop, rename_props[prop])

        Path(formula_file).write_text(formula_str)

        outs_cmd = "syfco -f ltl -m fully " + tlsf_formula_file + " -outs"
        # print(outs_cmd)
        outs = sp.getoutput(outs_cmd)
        # print(outs)
        # print(rename_props)

        outs_vec = outs.split(", ")
        part_outs = ".outputs "
        for output in outs_vec:
            if output in rename_props.keys():
                part_outs = part_outs + output + " "
        for prop in rename_props.keys():
            part_outs = part_outs.replace(prop, rename_props[prop])

        part_str = part_ins[:-1] + "\n" + part_outs[:-1] + "\n"
        Path(part_file).write_text(part_str)

if __name__ == "__main__":
    syntcomp("scripts/syntcomp-benchmarks/smv_formulas", "scripts/syntcomp-benchmarks/tlsf_canonized", "Syntcomp_benchmarks")
    syntcomp_env("scripts/syntcomp-benchmarks/smv_formulas", "scripts/syntcomp-benchmarks/tlsf_canonized", "Syntcomp_benchmarks_env")