# Topsis-Raj-102317090

A Python package to implement the **Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS)**.

TOPSIS is a multi-criteria decision analysis method that compares a set of alternatives based on a set of criteria. It identifies the alternative that is closest to the ideal best solution and farthest from the ideal worst solution.

## Installation

You can install the package using pip:

```bash
pip install Topsis-Raj-102317090

Usage
This package can be used via the command line interface (CLI).

Command Syntax

topsis <InputDataFile> <Weights> <Impacts> <ResultFileName>

Parameters

InputDataFile: The path to the CSV file containing the data.

The first column must contain the object/variable names (e.g., M1, M2, M3).

From the 2nd column to the last, the file must contain numeric values only.

Weights: A comma-separated string of numbers representing the weights for each criterion (e.g., "1,1,1,2").

Impacts: A comma-separated string of + or - signs representing the impact of each criterion (e.g., "+,+,-,+").

+ implies a higher value is better (Profit).

- implies a lower value is better (Cost).

ResultFileName: The name of the output CSV file where the results (including TOPSIS Score and Rank) will be saved.

Example

topsis data.csv "1,1,1,1,1" "+,+,-,+,+" result.csv

Constraints:

The input file must contain three or more columns.

The number of weights, impacts, and numeric columns must be the same.

Impacts must be strictly either + or -.

Weights must be numeric and separated by commas.

License
This project is licensed under the MIT License.


### Reminder:
Since you are updating this, remember to change your version number in `setup.py` to **1.0.1** (or higher) before you run the build command again, otherwise PyPI will reject it.