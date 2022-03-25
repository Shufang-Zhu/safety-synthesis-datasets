import random
import re

import click
from click import IntRange
from pathlib import Path


import spot

def _nb_digits(i: int):
    """Return number of digits."""
    return len(str(i))


def preprocess(raw_formula_str: str):
    """Preprocess 'randltl' output."""
    result = raw_formula_str
    result = re.sub("(\W)0|^()0", "\g<1>ff", result)
    result = re.sub("(\W)1|^()1", "\g<1>tt", result)
    result = re.sub("xor", "|", result)
    result = result.replace("W", "U")
    result = result.replace("M", "R")
    if random.random() > 0.5:
        result = result.replace("X", "X[!]")
    return result


@click.command()
@click.argument("formula_seeds_folder", default=None, type=click.Path(dir_okay=True, writable=False))
@click.argument("partition_seeds_folder", default=None, type=click.Path(dir_okay=True, writable=False))
@click.option("--random/--no-random", default=False, help="If true, do random conjunction.")
@click.option(
    "--conjuncts", type=IntRange(min=1,max=5), default=1, help="The number of conjuncts."
)
@click.option(
    "--number", type=IntRange(min=1,max=50), default=50, help="The number of generated formulas."
)
def generate(formula_seeds_folder, partition_seeds_folder, random, conjuncts, number):
    formula_seeds_folder = Path(formula_seeds_folder)
    partition_seeds_folder = Path(partition_seeds_folder)
    if random:
        save = Path("Random")
    else:
        save = Path("Conjunction")
    dataset_folder = save / Path(str(formula_seeds_folder.stem))
    dataset_folder.mkdir(parents=True, exist_ok=True)
    for c in range(1, conjuncts+1):
        benchmark_folder = dataset_folder / Path("case_"+f"{c:02d}"+"_"+str(number))
        benchmark_folder.mkdir(parents=True, exist_ok=True)
        for i in range(1, number+1):
            if random:
                formula, partition = random_conjunction(formula_seeds_folder, partition_seeds_folder, c)
            else:
                formula, partition = conjunction(formula_seeds_folder, partition_seeds_folder, c)
            formula_file = benchmark_folder / Path(f"{i:02d}"+".ltl")
            formula_file.write_text(formula)

            partition_file = benchmark_folder / Path(f"{i:02d}"+".part")
            partition_file.write_text(partition)


def conjunction(formula_seeds_folder, partition_seeds_folder, conjuncts):
    print(formula_seeds_folder)
    """
    Generate random conjunction Safety LTL formula.
    """

    files = list(formula_seeds_folder.glob("./*.ltl"))
    conjuncted_formula = spot.formula("true")
    inputs = []
    outputs = []
    for i in range(1, conjuncts + 1):
        formula_file = random.choice(files)
        print(formula_file.stem)
        part_file = partition_seeds_folder / f"{formula_file.stem}.part"
        content = Path(formula_file).read_text()
        content = re.sub("Request", "request", content)
        content = re.sub("Grant", "grant", content)
        spot_formula = spot.formula(content)
        curr_inputs, curr_outputs = read_partitions(part_file)
        props = spot.atomic_prop_collect(spot_formula)
        for var in curr_inputs:
            if var not in props:
                curr_inputs.remove(var)
        for var in curr_outputs:
            if var not in props:
                curr_outputs.remove(var)

        inputs_relabel = {}
        outputs_relabel = {}
        rename_label = {}
        inputs_relabeled = []
        outputs_relabeled = []
        for var in curr_inputs:
            new_name = "p" + str(i) + "_" + var
            inputs_relabel[var] = new_name
            rename_label[var] = new_name
            inputs_relabeled.append(new_name)
        for var in curr_outputs:
            new_name = "p" + str(i) + "_" + var
            outputs_relabel[var] = new_name
            rename_label[var] = new_name
            outputs_relabeled.append(new_name)

        formula_str = spot_formula.to_str()
        print(formula_str)
        for var in rename_label.keys():
            formula_str = formula_str.replace(var, "(" + rename_label[var] + ")")


        inputs.extend(inputs_relabeled)
        outputs.extend(outputs_relabeled)

        conjuncted_formula = spot.formula.And([conjuncted_formula, spot.formula(formula_str)])
        print(conjuncted_formula)
    formula_str = conjuncted_formula.to_str()
    partition = ".inputs:"
    for var in inputs:
        partition = partition + " " + var
    partition = partition + "\n.outputs:"
    for var in outputs:
        partition = partition + " " + var

    return formula_str, partition



def random_conjunction(formula_seeds_folder, partition_seeds_folder, conjuncts):
    print(formula_seeds_folder)
    """
    Generate random conjunction Safety LTL formula.
    """

    files = list(formula_seeds_folder.glob("./*.ltl"))
    conjuncted_formula = spot.formula("true")
    inputs = []
    outputs = []
    for i in range(1, conjuncts+1):
        formula_file = random.choice(files)
        print(formula_file.stem)
        part_file = partition_seeds_folder / f"{formula_file.stem}.part"
        content = Path(formula_file).read_text()
        content = re.sub("Request", "request", content)
        content = re.sub("Grant", "grant", content)
        spot_formula = spot.formula(content)
        conjuncted_formula = spot.formula.And([conjuncted_formula, spot_formula])
        print(conjuncted_formula)
        curr_inputs, curr_outputs = read_partitions(part_file)
        props = spot.atomic_prop_collect(spot_formula)
        for var in curr_inputs:
            if var not in props:
                curr_inputs.remove(var)
        for var in curr_outputs:
            if var not in props:
                curr_outputs.remove(var)
        inputs.extend(curr_inputs)
        outputs.extend(curr_outputs)
    nvars = 20
    inputs_relabel = {}
    outputs_relabel = {}
    rename_label = {}
    for var in inputs:
        new_name = "p" + str(random.randint(1, 10))
        inputs_relabel[var] = new_name
        rename_label[var] = new_name
    for var in outputs:
        new_name = "p" + str(random.randint(11, 20))
        outputs_relabel[var] = new_name
        rename_label[var] = new_name

    formula_str = conjuncted_formula.to_str()
    print(formula_str)
    for var in rename_label.keys():
        formula_str = formula_str.replace(var, "(" + rename_label[var] + ")")
    print(formula_str)
    print(rename_label)
    partition_inputs = []
    partition_outputs = []
    partition = ".inputs:"
    for var in inputs_relabel.keys():
        new_name = inputs_relabel[var]
        if new_name not in partition_inputs:
            partition_inputs.append(new_name)
            partition = partition + " " + new_name
    partition = partition + "\n.outputs:"
    for var in outputs_relabel.keys():
        new_name = outputs_relabel[var]
        if new_name not in partition_outputs:
            partition_outputs.append(new_name)
            partition = partition + " " + new_name

    return formula_str, partition


def read_partitions(part_file):
    part_file = Path(part_file)
    content = part_file.read_text()
    lines = content.split('\n')
    input_line = lines[0].strip()
    output_line = lines[1].strip()
    inputs = list(map(lambda x: x.lower(), input_line.split(' ')[1:]))
    outputs = list(map(lambda x: x.lower(), output_line.split(' ')[1:]))
    return inputs, outputs



if __name__ == "__main__":
    generate()