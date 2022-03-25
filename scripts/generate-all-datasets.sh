#!/usr/bin/env bash

set -e

formula_seeds_set="Processed/SSyft_1 Processed/SSyft_2 Processed/SSyft_3 Processed/SSyft_4 Processed/SSyft_5"
partition_seeds="Processed/SSyft_part"

for formula_seeds in ${formula_seeds_set}; do
    python3 "scripts/random_conjunction.py" "--random" "--conjuncts" "5" "--number" "50" "${formula_seeds}" "${partition_seeds}"
done

for formula_seeds in ${formula_seeds_set}; do
    python3 "scripts/random_conjunction.py" "--conjuncts" "5" "--number" "50" "${formula_seeds}" "${partition_seeds}"
done

set +e