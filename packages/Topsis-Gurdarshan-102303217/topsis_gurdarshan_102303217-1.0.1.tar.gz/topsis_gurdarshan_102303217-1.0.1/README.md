Here is the professional Markdown text. Copy this exact text and replace everything currently in your `README.md` file.

```markdown
# Topsis-Gurdarshan-102303217

`Topsis-Gurdarshan-102303217` is a Python library for dealing with **Multiple Criteria Decision Making (MCDM)** problems by using the **Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS)**.

## Installation

Use the package manager pip to install Topsis-Gurdarshan-102303217.

```bash
pip install Topsis-Gurdarshan-102303217

```

## Usage

Enter csv filename followed by `.csv` extension, then enter the *weights* vector with vector values separated by commas, followed by the *impacts* vector with comma separated signs (+,-).

```bash
topsis <InputDataFile> <Weights> <Impacts> <ResultFileName>

```

### Example

**sample.csv**

A csv file showing data for different mobile handsets having varying features.

| Model | Storage space(in gb) | Camera(in MP) | Price(in $) | Looks(out of 5) |
| --- | --- | --- | --- | --- |
| M1 | 16 | 12 | 250 | 5 |
| M2 | 16 | 8 | 200 | 3 |
| M3 | 32 | 16 | 300 | 4 |
| M4 | 32 | 8 | 275 | 4 |
| M5 | 16 | 16 | 225 | 2 |

**Input:**

```bash
topsis sample.csv "1,1,1,1" "+,-,+,+" result.csv

```

**Output:**

```text
      TOPSIS RESULTS
-----------------------------
    P-Score  Rank
1  0.534277     3
2  0.308368     5
3  0.691632     1
4  0.534737     2
5  0.401046     4

```

The output file will contain the original data with two additional columns: **Topsis Score** and **Rank**.

## License

[MIT](https://choosealicense.com/licenses/mit/)
