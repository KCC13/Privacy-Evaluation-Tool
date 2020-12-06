# PETools

A privacy evaluation program which is composed of several privacy evaluation algorithms, including three algorithms in “Data-Driven Approach for Evaluating Risk of Disclosure and Utility in Diﬀerentially Private Data Release”. The aim is to provide the people without background knowledge with simpliﬁed privacy scores of synthetic datasets.

## OS & Language Version Requirement
- MacOS or Linux
- Python 2.7.X

## Execution
Run `python main.py` and input the path of original dataset, anonymized dataset(synthetic dataset), and domain file respectively, after that you will see the menu. The program might ask you to input some additional parameters or file path when running some algorithms.

## 2020-12-07 Updates
- Fix some bugs
- Add requirements.txt
- Add sample data (in "sample_data" folder)
  - original dataset: ori_100.csv
  - anonymized dataset: ano_100.csv
  - domain file: domain.txt
  - p file: p.txt

## Warning
This repository is immature and deprecated, please use at your own risk.