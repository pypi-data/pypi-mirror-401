from pathlib import Path
import json
import pandas as pd
from typing import Dict, List, Optional

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stylometry Dashboard | {{run_id}}</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js" charset="utf-8"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --primary-light: #818cf8;
            --accent: #f43f5e;
            --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            --card-bg: rgba(30, 41, 59, 0.7);
            --glass-border: rgba(255, 255, 255, 0.1);
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --stat-val: #ffffff;
        }

        * { box-sizing: border-box; transition: all 0.2s ease; }

        body {
            font-family: 'Outfit', sans-serif;
            background: var(--bg-gradient);
            background-attachment: fixed;
            color: var(--text-main);
            margin: 0;
            padding: 2rem;
            min-height: 100vh;
        }

        .container { max-width: 1400px; margin: 0 auto; }

        .header {
            margin-bottom: 3rem;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--glass-border);
        }

        .header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(to right, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header-meta { text-align: right; color: var(--text-muted); font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; }

        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .glass-card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        .stat-card { text-align: center; }
        .stat-card h3 { margin: 0 0 0.5rem 0; font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }
        .stat-value { font-size: 2.5rem; font-weight: 700; color: var(--stat-val); }

        .section-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin: 2.5rem 0 1.5rem 0;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .section-title::before {
            content: '';
            display: inline-block;
            width: 4px;
            height: 1.5rem;
            background: var(--primary);
            border-radius: 2px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }

        th {
            text-align: left;
            padding: 1rem;
            color: var(--text-muted);
            font-weight: 600;
            border-bottom: 1px solid var(--glass-border);
        }

        td {
            padding: 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        tr:hover { background: rgba(255, 255, 255, 0.03); }

        .ai-insights-box {
            line-height: 1.7;
            font-size: 1rem;
            color: #cbd5e1;
            padding: 2rem;
            border-left: 4px solid var(--primary);
            background: rgba(99, 102, 241, 0.05);
        }

        .ai-insights-box h3, .ai-insights-box h2 {
            color: var(--primary-light);
            margin-top: 1.5rem;
        }

        .plots-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.5rem;
        }

        .plot-container { min-height: 450px; }

        .badge {
            padding: 0.25rem 0.6rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .badge-primary { background: rgba(99, 102, 241, 0.2); color: #a5b4fc; border: 1px solid rgba(99, 102, 241, 0.3); }

        .matrix-cell {
            font-family: 'JetBrains Mono', monospace;
            text-align: center;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: var(--glass-border); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.2); }

    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div>
                <h1>Stylometry Analysis</h1>
                <p style="margin: 0.5rem 0 0 0; color: var(--text-muted);">Quantitative author fingerprinting & linguistic depth analysis</p>
            </div>
            <div class="header-meta">
                ID: {{run_id}}<br>
                TS: {{timestamp}}
            </div>
        </header>

        <div class="dashboard-grid">
            <div class="glass-card stat-card">
                <h3>Documents</h3>
                <div class="stat-value">{{total_docs}}</div>
            </div>
            <div class="glass-card stat-card">
                <h3>Text Segments</h3>
                <div class="stat-value">{{total_chunks}}</div>
            </div>
            <div class="glass-card stat-card">
                <h3>Corpora</h3>
                <div class="stat-value">{{num_corpora}}</div>
            </div>
            <div class="glass-card stat-card">
                <h3>Analysis State</h3>
                <div class="stat-value" style="font-size: 1.5rem; color: #4ade80;">COMPLETE</div>
            </div>
        </div>

        <div class="glass-card" style="margin-bottom: 2rem;">
            <div class="section-title" style="margin-top: 0;">Corpus Overview</div>
            <table>
                <thead>
                    <tr>
                        <th>CORPUS LABEL</th>
                        <th>DOCS</th>
                        <th>CHUNKS</th>
                        <th>TOTAL WORDS</th>
                    </tr>
                </thead>
                <tbody>
                    {{corpus_rows}}
                </tbody>
            </table>
        </div>

        <div id="ai-insights-section" style="display: {{ai_display}};">
            <div class="section-title">AI Forensic Interpretation</div>
            <div class="glass-card ai-insights-box">
                {{ai_insights}}
            </div>
        </div>

        <div class="plots-grid">
            <div class="glass-card plot-container">
                <div class="section-title" style="margin-top: 0;">Lexical Diversity (MATTR)</div>
                <div id="mattr-boxplot" style="height: 400px;"></div>
            </div>
            <div class="glass-card plot-container">
                <div class="section-title" style="margin-top: 0;">Syntactic Complexity</div>
                <div id="slen-boxplot" style="height: 400px;"></div>
            </div>
        </div>

        <div class="plots-grid">
            <div class="glass-card plot-container">
                <div class="section-title" style="margin-top: 0;">Punctuation Fingerprint (DNA)</div>
                <div id="punct-radar" style="height: 400px;"></div>
            </div>
            <div class="glass-card plot-container">
                <div class="section-title" style="margin-top: 0;">Sentence Rhythm (Velocity Map)</div>
                <div id="rhythm-waveform" style="height: 400px;"></div>
                <p style="color: var(--text-muted); font-size: 0.75rem; text-align: center;">Showing sentence-by-sentence word counts (Chunk 0 trajectory)</p>
            </div>
        </div>

        <div id="pca-section">
            <div class="section-title">Stylistic Identity Map (Fingerprint Clustering)</div>
            <div class="glass-card plot-container" style="min-height: 600px;">
                <div id="pca-scatter" style="height: 550px;"></div>
                <p style="color: var(--text-muted); font-size: 0.8rem; margin-top: 1rem; text-align: center;">
                    * Each dot represents a 1,200-word segment. Clusters indicate shared stylistic DNA. Outliers are "voices" that deviate from the corpus norm.
                </p>
            </div>
        </div>
        
        <div id="delta-container" style="display: {{delta_display}};">
            <div class="section-title">Burrows' Delta (Stylistic Distance)</div>
            <div class="plots-grid">
                <div class="glass-card">
                    <div id="delta-heatmap" style="height: 450px;"></div>
                </div>
                <div class="glass-card" style="overflow-x: auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>CORPUS</th>
                                {{delta_headers}}
                            </tr>
                        </thead>
                        <tbody>
                            {{delta_rows}}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div id="semantic-container" style="display: {{semantic_display}};">
            <div class="section-title">Semantic Proximity (Embeddings)</div>
            <div class="plots-grid">
                <div class="glass-card">
                    <div id="semantic-heatmap" style="height: 450px;"></div>
                </div>
                <div class="glass-card" style="overflow-x: auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>CORPUS</th>
                                {{semantic_headers}}
                            </tr>
                        </thead>
                        <tbody>
                            {{semantic_rows}}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div id="sm-section">
            <div class="section-title">Linguistic Signature Matrix (StyloMetrix)</div>
            <div class="glass-card plot-container" style="min-height: 500px;">
                <div id="sm-heatmap" style="height: 500px;"></div>
                <p style="color: var(--text-muted); font-size: 0.75rem; text-align: center;">Heatmap of 100+ fine-grained linguistic features (normalized Z-scores per corpus)</p>
            </div>
        </div>

        <footer style="margin-top: 4rem; padding: 2rem; text-align: center; color: var(--text-muted); font-size: 0.8rem; border-top: 1px solid var(--glass-border);">
            <p>Stylometric artifacts generated via <strong>Stylometry CLI v1.0</strong></p>
            <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
                <span>Markers: MATTR, Yule's K, Burrows' Delta, Cosine Similarity, PCA Identity Mapping</span>
            </div>
        </footer>
    </div>

    <script id="doc-data" type="application/json">{{doc_json}}</script>
    <script id="chunk-data" type="application/json">{{chunk_json}}</script>
    <script id="delta-data" type="application/json">{{delta_json}}</script>
    <script id="semantic-data" type="application/json">{{semantic_json}}</script>
    <script id="pca-data" type="application/json">{{pca_json}}</script>

    <script>
        const docs = JSON.parse(document.getElementById('doc-data').textContent);
        const chunks = JSON.parse(document.getElementById('chunk-data').textContent);
        const delta = JSON.parse(document.getElementById('delta-data').textContent);
        const semantic = JSON.parse(document.getElementById('semantic-data').textContent);
        const pcaData = JSON.parse(document.getElementById('pca-data').textContent);

        const theme = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { family: 'Outfit, sans-serif', color: '#94a3b8' },
            xaxis: { gridcolor: 'rgba(255,255,255,0.05)', zerolinecolor: 'rgba(255,255,255,0.1)' },
            yaxis: { gridcolor: 'rgba(255,255,255,0.05)', zerolinecolor: 'rgba(255,255,255,0.1)' }
        };

        function createBoxPlot(target, dataSrc, yKey, title, color) {
            const corpora = [...new Set(dataSrc.map(d => d.corpus))];
            const data = corpora.map(c => ({
                y: dataSrc.filter(d => d.corpus === c).map(d => d[yKey]).filter(y => y !== null && !isNaN(y)),
                type: 'box',
                name: c,
                boxpoints: 'all',
                jitter: 0.3,
                marker: { color: color, size: 4 },
                line: { width: 1.5 }
            }));

            const layout = {
                ...theme,
                title: { text: title, font: { size: 14, color: '#f1f5f9' } },
                margin: { l: 50, r: 20, t: 60, b: 60 },
                showlegend: false
            };

            Plotly.newPlot(target, data, layout, {responsive: true, displayModeBar: false});
        }

        // Use chunks for distributions, or docs if no chunks
        if (chunks.length > 0) {
            createBoxPlot('mattr-boxplot', chunks, 'mattr', 'MATTR Lexical Richness (Distribution)', '#818cf8');
            createBoxPlot('slen-boxplot', chunks, 'avg_sentence_len', 'Sentence Length Distribution', '#f43f5e');
        } else if (docs.length > 0) {
            createBoxPlot('mattr-boxplot', docs, 'mattr', 'MATTR Lexical Richness', '#818cf8');
            createBoxPlot('slen-boxplot', docs, 'avg_sentence_len', 'Sentence Length Distribution', '#f43f5e');
        }

        function createHeatmap(target, matrix, title, colorscale) {
            if (Object.keys(matrix).length === 0) return;
            const labels = Object.keys(matrix).sort();
            const z = labels.map(l => labels.map(c => matrix[l][c]));
            
            const data = [{
                z: z,
                x: labels,
                y: labels,
                type: 'heatmap',
                colorscale: colorscale,
                showscale: true,
                ygap: 2,
                xgap: 2
            }];

            const layout = {
                ...theme,
                title: { text: title, font: { size: 14, color: '#f1f5f9' } },
                margin: { l: 100, r: 20, t: 60, b: 80 }
            };

            Plotly.newPlot(target, data, layout, {responsive: true, displayModeBar: false});
        }

        createHeatmap('delta-heatmap', delta, "Burrows' Delta Distance", 'Viridis');
        createHeatmap('semantic-heatmap', semantic, "Semantic Similarity", 'Electric');

        // Punctuation Radar
        const punctKeys = Object.keys(chunks[0] || {}).filter(k => k.startsWith('punct_'));
        if (punctKeys.length > 0) {
            const corpora = [...new Set(chunks.map(d => d.corpus))];
            const data = corpora.map(c => {
                const subset = chunks.filter(d => d.corpus === c);
                return {
                    type: 'scatterpolar',
                    r: punctKeys.map(k => {
                        const vals = subset.map(d => d[k]).filter(v => v != null);
                        return vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : 0;
                    }),
                    theta: punctKeys.map(k => k.replace('punct_', '').replace('_per_1000w', '')),
                    fill: 'toself',
                    name: c
                };
            });

            const layout = {
                ...theme,
                polar: {
                    radialaxis: { visible: true, range: [0, Math.max(...data.flatMap(d => d.r)) * 1.1], gridcolor: 'rgba(255,255,255,0.1)' },
                    angularaxis: { gridcolor: 'rgba(255,255,255,0.1)' },
                    bgcolor: 'rgba(0,0,0,0)'
                },
                margin: { l: 40, r: 40, t: 40, b: 40 },
                showlegend: true,
                legend: { orientation: 'h', y: -0.2 }
            };
            Plotly.newPlot('punct-radar', data, layout, {responsive: true});
        }

        // Sentence Rhythm Waveform
        if (chunks.length > 0) {
            const corpora = [...new Set(chunks.map(d => d.corpus))];
            const colors = ['#818cf8', '#f43f5e', '#10b981', '#fbbf24', '#8b5cf6'];
            const data = corpora.map((c, i) => {
                const firstChunk = chunks.find(d => d.corpus === c);
                const lens = firstChunk ? firstChunk.sent_lens : [];
                return {
                    x: lens.map((_, idx) => idx),
                    y: lens,
                    type: 'scatter',
                    mode: 'lines',
                    name: c,
                    line: { shape: 'spline', smoothing: 1.3, color: colors[i % colors.length] },
                    opacity: 0.8
                };
            });

            const layout = {
                ...theme,
                xaxis: { ...theme.xaxis, title: 'Sentence Sequence' },
                yaxis: { ...theme.yaxis, title: 'Words' },
                margin: { l: 50, r: 20, t: 40, b: 60 },
                hovermode: 'x unified'
            };
            Plotly.newPlot('rhythm-waveform', data, layout, {responsive: true});
        }

        // StyloMetrix Heatmap
        if (chunks.length > 0) {
            const smKeys = Object.keys(chunks[0]).filter(k => 
                !['corpus', 'doc_id', 'chunk_id', 'mattr', 'avg_sentence_len', 'word_count', 'yules_k', 'path', 'sent_lens', 'chunk_text', 'assigned_corpus'].includes(k) &&
                !k.startsWith('fw_') && !k.startsWith('punct_')
            );

            if (smKeys.length > 0) {
                const corpora = [...new Set(chunks.map(d => d.corpus))];
                const matrix = corpora.map(c => {
                    const subset = chunks.filter(d => d.corpus === c);
                    return smKeys.map(k => {
                        const vals = subset.map(d => d[k]).filter(v => typeof v === 'number');
                        return vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : 0;
                    });
                });

                const data = [{
                    z: matrix,
                    x: smKeys.map(k => k.split('.').pop()), // Shorten names for display
                    y: corpora,
                    type: 'heatmap',
                    colorscale: 'Portland',
                    showscale: true
                }];

                const layout = {
                    ...theme,
                    xaxis: { ...theme.xaxis, tickangle: 45, tickfont: { size: 10 } },
                    yaxis: { ...theme.yaxis },
                    margin: { l: 120, r: 20, t: 20, b: 150 }
                };
                Plotly.newPlot('sm-heatmap', data, layout, {responsive: true});
            } else {
                document.getElementById('sm-section').style.display = 'none';
            }
        }

        // PCA Plot
        if (pcaData.length > 0) {
            const corpora = [...new Set(pcaData.map(d => d.corpus))];
            const colors = ['#818cf8', '#f43f5e', '#10b981', '#fbbf24', '#8b5cf6'];
            const data = corpora.map((c, i) => {
                const subset = pcaData.filter(d => d.corpus === c);
                return {
                    x: subset.map(d => d.pc1),
                    y: subset.map(d => d.pc2),
                    mode: 'markers',
                    type: 'scatter',
                    name: c,
                    text: subset.map(d => `${d.doc_id} | ${d.chunk_id}`),
                    marker: { size: 8, opacity: 0.7, color: colors[i % colors.length] }
                };
            });

            const layout = {
                ...theme,
                title: { text: 'Identity Clustering (PCA)', font: { size: 16, color: '#f1f5f9' } },
                xaxis: { ...theme.xaxis, title: 'Stylistic Component 1' },
                yaxis: { ...theme.yaxis, title: 'Stylistic Component 2' },
                margin: { l: 60, r: 40, t: 80, b: 60 },
                hovermode: 'closest'
            };

            Plotly.newPlot('pca-scatter', data, layout, {responsive: true});
        } else {
            document.getElementById('pca-section').style.display = 'none';
        }

    </script>
</body>
</html>
"""

def generate_report(out_dir: Path, run_id: str, timestamp: str, summary: Dict, plot_files: List[str], 
                    ai_insights: Optional[str] = None, doc_df: Optional[pd.DataFrame] = None,
                    chunk_df: Optional[pd.DataFrame] = None):
    corpus_rows = ""
    total_docs = 0
    total_chunks = 0
    
    for name, data in summary.get("corpora", {}).items():
        total_docs += data.get("docs", 0)
        total_chunks += data.get("chunks", 0)
        corpus_rows += f"<tr><td>{name}</td><td>{data.get('docs', 0)}</td><td>{data.get('chunks', 0)}</td><td>{data.get('total_words_docs', 0):,}</td></tr>"
        
    findings = ""
    for note in summary.get("notes", []):
        findings += f"<li>{note}</li>"
    if not findings:
        findings = "<li>Numerical metrics extracted successfully.</li>"

    content = HTML_TEMPLATE
    content = content.replace("{{run_id}}", run_id)
    content = content.replace("{{timestamp}}", timestamp)
    content = content.replace("{{total_docs}}", str(total_docs))
    content = content.replace("{{total_chunks}}", str(total_chunks))
    content = content.replace("{{num_corpora}}", str(len(summary.get("corpora", {}))))
    content = content.replace("{{corpus_rows}}", corpus_rows)
    content = content.replace("{{findings}}", findings)
    
    # AI section
    if ai_insights:
        content = content.replace("{{ai_display}}", "block")
        content = content.replace("{{ai_insights}}", ai_insights)
    else:
        content = content.replace("{{ai_display}}", "none")
        content = content.replace("{{ai_insights}}", "")
    
    # Delta Matrix section
    delta_matrix = summary.get("burrows_delta", {})
    if delta_matrix:
        content = content.replace("{{delta_display}}", "block")
        headers = sorted(delta_matrix.keys())
        content = content.replace("{{delta_headers}}", "".join(f"<th>{h}</th>" for h in headers))
        
        rows_html = ""
        for row_label in headers:
            row_data = delta_matrix[row_label]
            row_cells = f"<td><strong>{row_label}</strong></td>"
            for col_label in headers:
                val = row_data.get(col_label, 0)
                style = ""
                if row_label != col_label:
                    if val < 0.8: style = 'style="background: #dcfce7;"'
                    elif val > 1.5: style = 'style="background: #fee2e2;"'
                row_cells += f"<td {style}>{val:.4f}</td>"
            rows_html += f"<tr>{row_cells}</tr>"
        content = content.replace("{{delta_rows}}", rows_html)
        content = content.replace("{{delta_json}}", json.dumps(delta_matrix))
    else:
        content = content.replace("{{delta_display}}", "none")
        content = content.replace("{{delta_headers}}", "")
        content = content.replace("{{delta_rows}}", "")
        content = content.replace("{{delta_json}}", "{}")

    # Semantic Matrix section
    semantic_matrix = summary.get("semantic_similarity", {})
    if semantic_matrix:
        content = content.replace("{{semantic_display}}", "block")
        headers = sorted(semantic_matrix.keys())
        content = content.replace("{{semantic_headers}}", "".join(f"<th>{h}</th>" for h in headers))
        
        rows_html = ""
        for row_label in headers:
            row_data = semantic_matrix[row_label]
            row_cells = f"<td><strong>{row_label}</strong></td>"
            for col_label in headers:
                val = row_data.get(col_label, 0)
                # Highlight high values (Semantic Similarity)
                style = ""
                if row_label != col_label:
                    if val > 0.85: style = 'style="background: #dcfce7;"'
                    elif val < 0.70: style = 'style="background: #fee2e2;"'
                row_cells += f"<td {style}>{val:.4f}</td>"
            rows_html += f"<tr>{row_cells}</tr>"
        content = content.replace("{{semantic_rows}}", rows_html)
        content = content.replace("{{semantic_json}}", json.dumps(semantic_matrix))
    else:
        content = content.replace("{{semantic_display}}", "none")
        content = content.replace("{{semantic_headers}}", "")
        content = content.replace("{{semantic_rows}}", "")
        content = content.replace("{{semantic_json}}", "{}")

    # Interactive Data
    cols = ["corpus", "doc_id", "mattr", "avg_sentence_len", "word_count", "yules_k"]
    if doc_df is not None:
        doc_json = doc_df[cols].to_json(orient="records")
        content = content.replace("{{doc_json}}", doc_json)
    else:
        content = content.replace("{{doc_json}}", "[]")

    if chunk_df is not None:
        chunk_cols = cols + ["chunk_id", "sent_lens"]
        # Add StyloMetrix keys
        exclude_core = ["corpus", "doc_id", "chunk_id", "mattr", "avg_sentence_len", "word_count", "yules_k", "path", "sent_lens", "chunk_text", "assigned_corpus"]
        sm_cols = [c for c in chunk_df.columns if c not in exclude_core and not c.startswith("fw_") and not c.startswith("punct_")]
        chunk_cols += sm_cols
        
        chunk_json = chunk_df[chunk_cols].to_json(orient="records")
        content = content.replace("{{chunk_json}}", chunk_json)
    else:
        content = content.replace("{{chunk_json}}", "[]")

    pca_data = summary.get("pca_data", [])
    content = content.replace("{{pca_json}}", json.dumps(pca_data))

    report_path = out_dir / "report.html"
    report_path.write_text(content, encoding="utf-8")
    return report_path
