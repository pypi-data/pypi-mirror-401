import shutil
import datetime as _dt
import json
from pathlib import Path
import pandas as pd
from typing import List, Optional

# matplotlib is optional
try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

def zip_dir(in_dir: Path, out_zip: Path) -> None:
    shutil.make_archive(str(out_zip).replace(".zip", ""), "zip", str(in_dir))

def utc_now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")

def maybe_make_plots(out_dir: Path, doc_df: pd.DataFrame, corpus_order: List[str]) -> List[str]:
    if plt is None:
        return []
    plot_files = []

    # Sentence length boxplot by corpus (doc-level)
    try:
        data = []
        labels = []
        for c in corpus_order:
            vals = doc_df.loc[doc_df["corpus"] == c, "avg_sentence_len"].dropna().values.tolist()
            if vals:
                data.append(vals)
                labels.append(c)
        if len(data) >= 1:
            plt.figure()
            plt.boxplot(data, labels=labels, showfliers=False)
            plt.title("Average sentence length by corpus (doc-level)")
            plt.ylabel("Words per sentence")
            fn = "plot_avg_sentence_len_boxplot.png"
            plt.tight_layout()
            plt.savefig(out_dir / fn, dpi=150)
            plt.close()
            plot_files.append(fn)
    except Exception:
        pass

    # MATTR boxplot by corpus
    try:
        data = []
        labels = []
        for c in corpus_order:
            vals = doc_df.loc[doc_df["corpus"] == c, "mattr"].dropna().values.tolist()
            if vals:
                data.append(vals)
                labels.append(c)
        if len(data) >= 1:
            plt.figure()
            plt.boxplot(data, labels=labels, showfliers=False)
            plt.title("MATTR lexical diversity by corpus (doc-level)")
            plt.ylabel("MATTR")
            fn = "plot_mattr_boxplot.png"
            plt.tight_layout()
            plt.savefig(out_dir / fn, dpi=150)
            plt.close()
            plot_files.append(fn)
    except Exception:
        pass

    return plot_files
