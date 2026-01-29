# Stylometry CLI (local/offline) — v1.0

This is a small, **offline** Python tool to extract **stylometric artifacts/patterns** from text
and optionally compute simple **similarity** signals between corpora using character n-grams.

It’s designed to slot into your **Stylometry Orchestrator** workflow by emitting SAO-style
`ResultBundle_*.json` files plus CSV artifacts.

## What it does

For each document (and each chunk of a document), it computes:

- **Lexical**
  - word count, unique word count
  - average word length
  - **MATTR** lexical diversity (more length-robust than raw TTR)

- **Syntactic (proxy)**
  - average sentence length
  - sentence length variation (population SD)

- **Habitual**
  - function word frequencies (configurable list)
  - punctuation rates (commas/semicolons/etc per 1000 words and per sentence)

If 2+ corpora are provided and there are enough chunks, it also computes:

- **Char n-gram TF-IDF centroid cosine similarity** across corpora (`corpus_similarity_char_ngrams.csv`)
- **Nearest-centroid chunk assignment** (`chunk_assignments_char_ngrams.csv`)

> Note: these are **signals**, not definitive authorship proof. Topic/genre/boilerplate can dominate.

## Requirements

- Windows, macOS, or Linux
- Python **3.12+**
- `pip` install of dependencies

## Install (Windows PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Quick check:

```powershell
python -c "import numpy, pandas, sklearn; print('ok')"
```

## Input formats

You provide one or more `--corpus LABEL=PATH` arguments.

`PATH` can be:
- a single `.txt` / `.md` file
- a folder containing `.txt` / `.md` files (recursively)
- a `.zip` archive containing `.txt` / `.md` files (recursively)

Examples of folder layouts that work:

**Single corpus**
```
my_corpus/
  speech1.txt
  speech2.txt
  speech3.txt
```

**Multiple corpora**
```
corpora/
  A/
    doc1.txt
    doc2.txt
  B/
    doc3.txt
    doc4.txt
```

You can point each corpus to its subfolder:
- `--corpus A=corpora/A --corpus B=corpora/B`

## Run examples

### 1) Characterize a single document

```powershell
python stylometry_run.py --task characterize --corpus TextA=./speech1.txt --output ./out_textA
```

### 2) Build a profile from many documents (single corpus)

```powershell
python stylometry_run.py --task profile_build --corpus PersonX=./my_corpus --output ./out_personx
```

### 3) Compare two corpora

```powershell
python stylometry_run.py --task compare --corpus A=./corpora/A --corpus B=./corpora/B --output ./out_compare
```

### 4) Use zip archives

```powershell
python stylometry_run.py --task compare --corpus A=./A.zip --corpus B=./B.zip --output ./out_compare_zip
```

## Outputs

The output folder contains:

- `manifest.json` — corpus manifest (doc list + word counts + local provenance paths)
- `doc_metrics.csv` — per-document metrics
- `chunk_metrics.csv` — per-chunk metrics
- `ResultBundle_ArtifactExtractor.json` — SAO-compatible bundle describing artifacts produced
- `run_metadata.json` — parameters and reproducibility info

If 2+ corpora and enough chunks:
- `corpus_similarity_char_ngrams.csv`
- `chunk_assignments_char_ngrams.csv`
- `ResultBundle_Comparator.json`

If matplotlib is installed and working, it also saves:
- `plot_avg_sentence_len_boxplot.png`
- `plot_mattr_boxplot.png`

## Useful options

- `--chunk-words 1200` — set chunk size (default 1200)
- `--mattr-window 500` — MATTR window size (default 500)
- `--function-words-file path.txt` — override function word list (newline-delimited)
- `--include-chunk-text` — include chunk text in `chunk_metrics.csv` (can be large)
- `--char-analyzer char_wb|char` — default `char_wb` (often better for stylometry)
- `--max-features 50000` and `--min-df 2` — control n-gram feature size

## Notes for political/public-figure corpora

Prepared remarks and official publications can reflect speechwriters, staff editing,
or transcript normalization. Use “channel-specific” corpora where possible
(e.g., floor speeches vs press releases vs prepared remarks).

## Troubleshooting

- If plots aren’t produced: ensure `matplotlib` installed and you have write permission.
- If Unicode errors: convert source files to UTF-8, or the script will fall back to forgiving decodes.
- If it’s slow on huge corpora: increase `--min-df`, reduce `--max-features`, or reduce corpus size.

