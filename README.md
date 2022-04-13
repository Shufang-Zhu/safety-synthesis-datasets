## Generate Datasets
### Basic setup
  1. Python3
     
  2. [Syfco](https://github.com/reactive-systems/syfco)
  
  3. Python package from [spot](https://spot.lrde.epita.fr/install.html)

  4. Generate datasets
  ```sh
  bash scripts/generate-all-datasets.sh
  ```
  This generates benchmarks of 3 dataset families: 
  - Conjunction, under folder Conjunction/..  
  - Random_Conjunction, under folder Random/..
  - EBR_LTL, under folder EBR_LTL/..

### Conjuncted benchmarks
  via python file `scripts/random_conjunction.py`.
  - scripts/random_conjunction.py
  ```sh
  python3 random_conjunction.py options formula_seeds_folder partition_seeds_folder
  ```
  Example of Conjuncted benchmarks:
  ```sh
  python3 random_conjunction.py --no-random --conjuncts 5 --number 50 Dataset_seeds/SSyft_1 Dataset_seeds/SSyft_part
  ```
  This will take 1-5 (random) formulas from `Dataset_seeds/SSyft_1` and `Dataset_seeds/SSyft_part` as seeds, 
  then generates (50) conjuncted formulas, and store the genrated formulas in `Conjunction/SSyft_1/case_01_50`
  to `Conjunction/SSyft_1/case_05_50`, respectively.
  
### Randomly Conjuncted benchmarks
  via python file `scripts/random_conjunction.py`.
  ```sh
  python3 random_conjunction.py --random --conjuncts 5 --number 50 Dataset_seeds/SSyft_1 Dataset_seeds/SSyft_part
  ```
  This will take 1-5 (random) formulas from `Dataset_seeds/SSyft_1` and `Dataset_seeds/SSyft_part` as seeds, 
  then generates (50) randomly conjuncted formulas, and store the genrated formulas in `Random_Conjunction/SSyft_1/case_01_50`
  to `Random_Conjunction/SSyft_1/case_05_50`, respectively.


### Datasets from EBR_LTL
  This dataset family is from [paper](https://link.springer.com/article/10.1007/s10703-021-00383-3), and consists of two sets of benchmarks: Scalable and Syntcomp_benchmarks
#### Scalable
  via python file `scripts/ebr_ltl_scalable.py`.
  This set of benchmarks is divided in four categories (the propo-
  sitional atoms starting with the letter `c` are controllable, i.e., agent variable, while those starting with the letter `u`
  are uncontrollable, i.e., environment variable). See [paper](https://link.springer.com/article/10.1007/s10703-021-00383-3) for more details.

  ```sh
  python3 scripts/ebr_ltl_scalable.py
  ```
  This will generate scalable benchmarks and store the genrated ones in `EBR_LTL/Scalable/..`.
  Note that in order to modify the number of generated benchmarks of each category, please change the parameters in `scripts/ebr_ltl_scalable.py`.
  ```shell
  generate_tlsf_seeds(40, 10, 50, 50)
  ```
  This will generate 40 real_1 benchmarks, 10 real_2 benchmarks, 50 unreal_1 benchmarks, and 50 unreal_2 benchmarks.

#### Syntcomp Datasets
  via python file `scripts/syntcomp_benchmarks.py`.
  Selected benchmarks from [SYNTCOMP](http://www.syntcomp.org/).
  

  
## Other folders
Original datasets are from SSyft, under folder `Basic/..`, but not recognized as safety LTL formula by Syft, 
since `G` in proposition `Grant` is parsed as temporal connective `Always`. The processed ones are under folder
`Dataset_seeds/..`, through script `scripts/process_basic_formula.py`.


  

 