import argparse
import random
import sys
from pathlib import Path
from typing import List, Optional, Sequence, Tuple
import numpy as np
import pandas as pd
import shutil

from .models import DocRecord, ChunkRecord
from .loaders import load_corpus, chunk_doc, safe_read_text
from .normalizer import NormalizerConfig
from .metrics import (
    DEFAULT_FUNCTION_WORDS, 
    compute_metrics_for_text, 
    build_char_ngram_similarity,
    compute_stylistic_pca,
    compute_sm_vectors,
    _mp_compute_metrics
)
from .utils import (
    utc_now_iso, 
    ensure_dir, 
    write_json, 
    maybe_make_plots
)
from .boilerplate import find_boilerplate, strip_boilerplate
from .reporting import generate_report
from .ai_interface import analyze_stats_with_ai
from .delta import calculate_burrows_delta
from .semantic import calculate_semantic_similarity_matrix

import concurrent.futures
import multiprocessing

# Optional dependencies
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):
        return iterable

def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Stylometric artifact extraction + comparison (offline)."
    )
    parser.add_argument("--task", choices=["normalize", "characterize", "compare", "profile_build", "anomaly_scan"], default="characterize")
    parser.add_argument("--corpus", action="append", required=True, help="LABEL=PATH")
    parser.add_argument("--output", default=None)
    parser.add_argument("--chunk-words", type=int, default=1200)
    parser.add_argument("--chunk-overlap", type=int, default=0, help="Overlap between chunks in words.")
    parser.add_argument("--mattr-window", type=int, default=500)
    
    # Normalization & Boilerplate
    parser.add_argument("--remove-stage-directions", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--remove-speaker-labels", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--remove-quote-blocks", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--min-quote-block-lines", type=int, default=2)
    parser.add_argument("--strip-urls", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--dedupe-paragraphs", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--boilerplate-threshold", type=float, default=0.0, help="0.0 to disable, else e.g. 0.5")
    parser.add_argument("--normalize-before-analysis", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--emit-clean-corpus", action=argparse.BooleanOptionalAction, default=False)
    
    # Delta
    parser.add_argument("--delta-mfw", type=int, default=150, help="Number of Top Most Frequent Words for Burrows' Delta.")
    
    parser.add_argument("--function-words-file", default=None)
    parser.add_argument("--include-chunk-text", action=argparse.BooleanOptionalAction, default=False)

    # Performance
    parser.add_argument("--parallel", type=int, default=1, help="Number of worker processes (default 1).")

    # char n-gram params
    parser.add_argument("--ngram-min", type=int, default=3)
    parser.add_argument("--ngram-max", type=int, default=5)
    parser.add_argument("--char-lowercase", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--char-analyzer", choices=["char", "char_wb"], default="char_wb")
    parser.add_argument("--max-features", type=int, default=50000)
    parser.add_argument("--min-df", type=int, default=2)
    parser.add_argument("--seed", type=int, default=1337)

    # AI Analysis
    parser.add_argument("--ai-analyze", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--ai-api-base", default="http://localhost:1234/v1")
    parser.add_argument("--ai-model", default="local-model")

    # Semantic Analysis
    parser.add_argument("--semantic-analyze", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--embedding-model", default="local-model")
    
    # StyloMetrix
    parser.add_argument("--stylo-metrix", action=argparse.BooleanOptionalAction, default=True, help="Enable heavy linguistic feature extraction via StyloMetrix.")

    args = parser.parse_args(argv)

    random.seed(args.seed)
    np.random.seed(args.seed)

    norm_cfg = NormalizerConfig(
        remove_stage_directions=args.remove_stage_directions,
        remove_quote_blocks=args.remove_quote_blocks,
        min_quote_block_lines=args.min_quote_block_lines,
        remove_speaker_labels=args.remove_speaker_labels,
        strip_urls=args.strip_urls,
        dedupe_paragraphs=args.dedupe_paragraphs
    )

    function_words = DEFAULT_FUNCTION_WORDS
    if args.function_words_file:
        fw_path = Path(args.function_words_file).expanduser()
        lines = [ln.strip().lower() for ln in safe_read_text(fw_path).splitlines()]
        function_words = [ln for ln in lines if ln and not ln.startswith("#")]
        if not function_words:
            print("Function word file was empty; using default.", file=sys.stderr)
            function_words = DEFAULT_FUNCTION_WORDS

    run_id = utc_now_iso().replace("Z", "").replace(":", "").replace("-", "")
    out_dir = Path(args.output) if args.output else Path(f"stylometry_out_{run_id}")
    ensure_dir(out_dir)

    corpora_specs: List[Tuple[str, str]] = []
    for spec in args.corpus:
        if "=" not in spec: raise ValueError(f"Invalid spec: {spec}")
        label, path = spec.split("=", 1)
        corpora_specs.append((label.strip(), path.strip().strip('"').strip("'")))

    all_docs: List[DocRecord] = []
    temp_roots: List[Path] = []
    print(f"Loading {len(corpora_specs)} corpora...")
    for label, path in tqdm(corpora_specs, desc="Corpora"):
        docs, temp_root = load_corpus(label, path, norm_cfg=norm_cfg)
        all_docs.extend(docs)
        if temp_root: temp_roots.append(temp_root)

    if not all_docs:
        print("No documents loaded.", file=sys.stderr)
        return 2

    # Normalization logic (task normalize or flag)
    if args.task == "normalize" or args.normalize_before_analysis:
        print("Running advanced normalization...")
        # (This applies to d.text; re-tokenize below)
        from .loaders import tokenize_words, split_sentences
        for d in all_docs:
            d.word_tokens = tokenize_words(d.text)
            d.sentences = split_sentences(d.text)

    # Boilerplate detection
    if args.boilerplate_threshold > 0:
        print(f"Detecting boilerplate at threshold {args.boilerplate_threshold}...")
        bp_hashes = find_boilerplate(all_docs, threshold=args.boilerplate_threshold)
        if bp_hashes:
            print(f"Stripping {len(bp_hashes)} boilerplate paragraphs...")
            strip_boilerplate(all_docs, bp_hashes)
            # Re-tokenize after stripping
            from .loaders import tokenize_words, split_sentences
            for d in all_docs:
                d.word_tokens = tokenize_words(d.text)
                d.sentences = split_sentences(d.text)

    # Emit clean corpus if requested
    if args.emit_clean_corpus:
        clean_root = out_dir / "clean_corpus"
        ensure_dir(clean_root)
        for d in all_docs:
            c_dir = clean_root / d.corpus
            ensure_dir(c_dir)
            (c_dir / f"{d.doc_id}.txt").write_text(d.text, encoding="utf-8")
        from .utils import zip_dir
        zip_dir(clean_root, out_dir / "clean_corpus.zip")
        print(f"Clean corpus saved to {out_dir}/clean_corpus.zip")

    if args.task == "normalize":
        print("Normalization complete.")
        return 0

    print(f"Chunking {len(all_docs)} documents...")
    all_chunks: List[ChunkRecord] = []
    for d in tqdm(all_docs, desc="Chunking"):
        all_chunks.extend(chunk_doc(d, chunk_words=args.chunk_words, overlap=args.chunk_overlap))

    # Process Metrics with optional parallelism
    def process_items(items, desc):
        if not items: return []
        rows = []
        payloads = [
            (i.word_tokens, i.sentences, i.text, function_words, args.mattr_window)
            for i in items
        ]
        
        if args.parallel > 1:
             with concurrent.futures.ProcessPoolExecutor(max_workers=args.parallel) as executor:
                results = list(tqdm(executor.map(_mp_compute_metrics, payloads), total=len(payloads), desc=desc))
        else:
            results = []
            for p in tqdm(payloads, desc=desc):
                results.append(_mp_compute_metrics(p))
                
        for i, m in zip(items, results):
            row = {"corpus": str(i.corpus), "doc_id": str(i.doc_id)}
            if hasattr(i, "path"): row["path"] = str(i.path)
            if hasattr(i, "chunk_id"): row["chunk_id"] = str(i.chunk_id)
            row.update(m)
            rows.append(row)
        return rows

    doc_rows = process_items(all_docs, "Doc Metrics")
    doc_df = pd.DataFrame(doc_rows) if doc_rows else pd.DataFrame(columns=["corpus", "doc_id"])

    chunk_rows = process_items(all_chunks, "Chunk Metrics")
    
    if args.stylo_metrix and chunk_rows:
        print("Extracting StyloMetrix signatures (this may take a moment)...")
        try:
            sm_texts = [c.text for c in all_chunks]
            sm_vectors = compute_sm_vectors(sm_texts)
            for i, sv in enumerate(sm_vectors):
                if i < len(chunk_rows):
                    chunk_rows[i].update(sv)
            summary["notes"].append("Integrated StyloMetrix signatures.")
        except Exception as e:
            print(f"Warning: StyloMetrix signatures failed: {e}", file=sys.stderr)

    if args.include_chunk_text and chunk_rows:
        for i, row in enumerate(chunk_rows):
            row["chunk_text"] = all_chunks[i].text
    chunk_df = pd.DataFrame(chunk_rows) if chunk_rows else pd.DataFrame(columns=["corpus", "doc_id", "chunk_id"])

    doc_df.to_csv(out_dir / "doc_metrics.csv", index=False, encoding="utf-8")
    chunk_df.to_csv(out_dir / "chunk_metrics.csv", index=False, encoding="utf-8")

    corpus_manifest = {
        "corpus_id": f"local-{run_id}",
        "retrieved_at": utc_now_iso(),
        "docs": [{"doc_id": d.doc_id, "corpus": d.corpus, "word_count_est": len(d.word_tokens)} for d in all_docs]
    }
    write_json(out_dir / "manifest.json", corpus_manifest)

    corpus_order = [c for c, _ in corpora_specs]
    plot_files = maybe_make_plots(out_dir, doc_df, corpus_order)

    summary = {"corpora": {}, "notes": []}
    for corp in corpus_order:
        try:
            sub_doc = doc_df[doc_df["corpus"] == corp] if not doc_df.empty else pd.DataFrame()
            sub_chunk = chunk_df[chunk_df["corpus"] == corp] if not chunk_df.empty else pd.DataFrame()
            summary["corpora"][corp] = {
                "docs": int(sub_doc.shape[0]) if not sub_doc.empty else 0,
                "chunks": int(sub_chunk.shape[0]) if not sub_chunk.empty else 0,
                "total_words_docs": int(sub_doc["word_count"].sum()) if not sub_doc.empty and "word_count" in sub_doc else 0,
                "avg_mattr": float(sub_doc["mattr"].mean()) if not sub_doc.empty and "mattr" in sub_doc else 0.0,
                "avg_yules_k": float(sub_doc["yules_k"].mean()) if not sub_doc.empty and "yules_k" in sub_doc else 0.0,
                "avg_sentence_len": float(sub_doc["avg_sentence_len"].mean()) if not sub_doc.empty and "avg_sentence_len" in sub_doc else 0.0,
                "avg_hapax_rate": float(sub_doc["hapax_rate"].mean()) if not sub_doc.empty and "hapax_rate" in sub_doc else 0.0,
                "avg_commas_per_1000w": float(sub_doc["commas_per_1000w"].mean()) if not sub_doc.empty and "commas_per_1000w" in sub_doc else 0.0,
            }
        except Exception as e:
            print(f"Warning: could not summarize corpus {corp}: {e}", file=sys.stderr)

    if len(set([d.corpus for d in all_docs])) >= 2 and len(all_chunks) >= 4:
        print("Building char n-gram similarity matrix...")
        sim_df, assign_df = build_char_ngram_similarity(
            all_chunks, 
            ngram_min=args.ngram_min, ngram_max=args.ngram_max,
            lowercase=args.char_lowercase, analyzer=args.char_analyzer,
            max_features=args.max_features, min_df=args.min_df, random_seed=args.seed
        )
        if not sim_df.empty:
            sim_df.to_csv(out_dir / "corpus_similarity_char_ngrams.csv", encoding="utf-8")
            assign_df.to_csv(out_dir / "chunk_assignments_char_ngrams.csv", index=False, encoding="utf-8")
            
            write_json(out_dir / "ResultBundle_Comparator.json", {
                "bundle_id": f"rb-comparator-{run_id}",
                "produced_by": "Comparator",
                "artifacts": {"files": ["corpus_similarity_char_ngrams.csv", "chunk_assignments_char_ngrams.csv"]}
            })
            summary["notes"].append("Computed char n-gram similarities.")

    # Burrows' Delta
    if len(corpus_order) > 1:
        print(f"Calculating Burrows' Delta (MFW={args.delta_mfw})...")
        try:
            delta_df, mfw_list = calculate_burrows_delta(all_docs, mfw_limit=args.delta_mfw)
            if not delta_df.empty:
                delta_df.to_csv(out_dir / "burrows_delta_matrix.csv")
                # Convert matrix to a list-of-lists format for easier JS/HTML handling if needed, 
                # or just keep as dict for now.
                summary["burrows_delta"] = delta_df.to_dict(orient="index")
                summary["notes"].append(f"Computed Burrows' Delta using {len(mfw_list)} MFW.")
        except Exception as e:
            print(f"Warning: Burrows' Delta calculation failed: {e}", file=sys.stderr)

    # Semantic Analysis
    if args.semantic_analyze and len(corpus_order) > 1:
        print(f"Calculating Semantic Similarity via {args.ai_api_base}...")
        try:
            sem_df, centroids = calculate_semantic_similarity_matrix(all_docs, args.ai_api_base, args.embedding_model)
            if not sem_df.empty:
                sem_df.to_csv(out_dir / "semantic_similarity_matrix.csv")
                summary["semantic_similarity"] = sem_df.to_dict(orient="index")
                summary["notes"].append(f"Computed semantic similarity for {len(all_docs)} documents.")
        except Exception as e:
            print(f"Warning: Semantic analysis failed: {e}", file=sys.stderr)

    # PCA Clustering
    if not chunk_df.empty:
        print("Computing Stylistic Identity Map (PCA)...")
        try:
            pca_df = compute_stylistic_pca(all_chunks, chunk_rows)
            if not pca_df.empty:
                pca_df.to_csv(out_dir / "stylistic_pca.csv", index=False)
                summary["pca_data"] = pca_df.to_dict(orient="records")
                summary["notes"].append("Generated Stylistic Identity Map (PCA).")
        except Exception as e:
            print(f"Warning: PCA projection failed: {e}", file=sys.stderr)

    artifact_bundle = {
        "bundle_id": f"rb-artifacts-{run_id}",
        "produced_by": "ArtifactExtractor",
        "artifacts": {
            "files": ["manifest.json", "doc_metrics.csv", "chunk_metrics.csv"] + plot_files,
        },
        "key_findings": [f"Processed {len(all_docs)} docs.", summary["corpora"]]
    }
    write_json(out_dir / "ResultBundle_ArtifactExtractor.json", artifact_bundle)

    write_json(out_dir / "run_metadata.json", {"run_id": run_id, "timestamp_utc": utc_now_iso(), "task": args.task})

    ai_insights = None
    if args.ai_analyze:
        print(f"Requesting AI interpretation from {args.ai_api_base}...")
        ai_insights = analyze_stats_with_ai(summary, args.ai_api_base, args.ai_model)
        write_json(out_dir / "ai_insights.json", {"insights": ai_insights})

    report_path = generate_report(out_dir, run_id, utc_now_iso(), summary, plot_files, ai_insights=ai_insights, doc_df=doc_df, chunk_df=chunk_df)
    print(f"Report generated: {report_path.resolve()}")

    for tr in temp_roots: shutil.rmtree(tr, ignore_errors=True)
    print(f"Done. Output: {out_dir.resolve()}")
    return 0
