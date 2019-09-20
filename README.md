# attacks

Contains libraries and attacks for generating GDA Scores (General Data Anonyization Score). The intent is to make it relatively easy for people to develop new attacks.

# Code Documentation

See https://gda-score.github.io/ for code documentation of the underlying libraries.

See https://www.gda-score.org/quick-guide-to-writing-attacks/ for an overview of how to write an attack.

# To Use

This folder contains attacks as well as examples of how to design an attack. Best to just take one of the existing attacks as a template and work from there.  The `examples` folder contains additional snippits of code showing how to use different aspects of the attack API (class `gdaAttack()`, class `gdaScores()` etc.)

To run an attack, a `results` folder must be placed in the path where the attack is being executed.

# Main components

The main folder contains the attacks themselves. Typically each attack consists of the basic attack code (python) and the configuration for the attack (corresponding .json with the same file name).

The .json config file contains the set of anonymization methods to attack (`anonTypes`), the set of datasets to attack (`tables`), and basic parameters (`basic`). It is important to set `criteria` to the correct type of attack measure (singlingOut, inference, or linkability).

## attacks/examples

Contains simple examples of how to use the gda-score APIs.

