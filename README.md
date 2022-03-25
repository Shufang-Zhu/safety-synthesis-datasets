## Generate Datasets
  ```sh
  bash scripts/generate-all-datasets.sh
  ```
  This calls the python file `scripts/random_conjunction.py`.
  - scripts/random_conjunction.py
  ```sh
  python3 random_conjunction.py options formula_seeds_folder partition_seeds_folder
  ```
  Example of Conjuncted benchmarks:
  ```sh
  PYTHONPATH="." python3 --no-random --conjuncts 5 --number 100 Processed/SSyft_1 Processed/SSyft_part
  ```
  This will take 1-5 (random) formulas from `Processed/SSyft_1` and `Processed/SSyft_part` as seeds, 
  then generates (100) conjuncted formulas, and store the genrated formulas in `Conjunction/SSyft_1/case_01_100`
  to `Conjunction/SSyft_1/case_05_100`, respectively.
  
  Example of Randomly Conjuncted benchmarks:
  ```sh
  PYTHONPATH="." python3 random --conjuncts 5 --number 100 Processed/SSyft_1 Processed/SSyft_part
  ```
  This will take 1-5 (random) formulas from `Processed/SSyft_1` and `Processed/SSyft_part` as seeds, 
  then generates (100) randomly conjuncted formulas, and store the genrated formulas in `Conjunction/SSyft_1/case_01_100`
  to `Conjunction/SSyft_1/case_05_100`, respectively.

## Datasets
- ### Conjuncted benchmarks
  Under folder Conjunction/..
  
- ### Randomly Conjuncted benchmarks
  Under folder Random/..

  
## Formula Seeds
Original datasets are from SSyft, under folder `Basic/..`, but not recognized as safety LTL formula by Syft, 
since `G` in proposition `Grant` is parsed as temporal connective `Always`. The processed ones are under folder
`Processed/..`, by script file `scripts/Random/process_basic_formula.py`.


  

 