# attacks

Contains libraries and attacks for generating GDA Scores (General Data Anonyization Score). The intent is to make it relatively easy for people to develop new attacks.

# Code Documentation

See https://gda-score.github.io/ for code documentation of the underlying libraries.

See https://www.gda-score.org/quick-guide-to-writing-attacks/ for an overview of how to write an attack.

# To Use

To run the tools, you must first install the package `gda-score-code`

#### Installing via `pip`:    
   - step 1: `$ pip install gda-score-code`    
            
   - step 2: If you would like to stick to default configuration (common case) then skip this step. Otherwise execute `$ gdascore_init` in your console to modify the configuration.    

This folder contains attacks as well as examples of how to design an attack. Best to just take one of the existing attacks as a template and work from there.  The `examples` folder contains additional snippits of code showing how to use different aspects of the attack API (class `gdaAttack()`, class `gdaScores()` etc.)

To run an attack, a `results` folder must be placed in the path where the attack is being executed.

# Main components

The main folder contains the attacks themselves. Typically each attack consists of the basic attack code (python) and the configuration for the attack (corresponding .json with the same file name).

Each .json config file contains the set of anonymization methods to attack (`anonTypes`), the set of datasets to attack (`tables`), and basic parameters (`basic`). It is important to set `criteria` to the correct type of attack measure (singlingOut, inference, or linkability).

## attacks/examples

Contains simple examples of how to use the gda-score APIs.

