
# PageRank Algorithm

This project implements the PageRank algorithm in Python using two approaches:

- **Sampling-based PageRank**
- **Iterative PageRank**

The algorithm estimates the importance of each page in a given corpus of interlinked HTML files.

## Files

- `pagerank.py`: Main script that loads a corpus and computes PageRank using both methods.
- `corpus2/`: Example folder containing test HTML files (corpus).

## How It Works

The script:
1. Parses all HTML files in a folder to extract links between pages.
2. Builds a dictionary representing the corpus (each page and the pages it links to).
3. Computes PageRank using:
   - A sampling method (based on random walks).
   - An iterative method (based on repeated updates until values converge).

## How to Run

Open a terminal in the project directory and run:

```bash
python pagerank.py corpus2
```

## Example Output

```bash
PageRank Results from Sampling (n = 10000)
  ai.html: 0.1866
  algorithms.html: 0.1050
  c.html: 0.1313
  inference.html: 0.1284
  logic.html: 0.0243
  programming.html: 0.2331
  python.html: 0.1196
  recursion.html: 0.0717
PageRank Results from Iteration
  ai.html: 0.1889
  algorithms.html: 0.1064
  c.html: 0.1238
  inference.html: 0.1289
  logic.html: 0.0264
  programming.html: 0.2301
  python.html: 0.1238
  recursion.html: 0.0717
```