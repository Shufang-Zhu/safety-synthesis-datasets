#!/usr/bin/env bash

set -e

formula_seeds_set="Dataset_seeds/SSyft_1 Dataset_seeds/SSyft_2 Dataset_seeds/SSyft_3 Dataset_seeds/SSyft_4 Dataset_seeds/SSyft_5"
partition_seeds="Dataset_seeds/SSyft_part"

for formula_seeds in ${formula_seeds_set}; do
    python3 "scripts/random_conjunction.py" "--random" "--conjuncts" "5" "--number" "20" "${formula_seeds}" "${partition_seeds}"
done

for formula_seeds in ${formula_seeds_set}; do
    python3 "scripts/random_conjunction.py" "--conjuncts" "5" "--number" "20" "${formula_seeds}" "${partition_seeds}"
done

python3 "scripts/syntcomp_benchmarks.py"

python3 "scripts/ebr_ltl_scalable_benchmarks.py"

set +e