import json
import urllib.request
import urllib.error
from typing import Dict, List, Optional

def analyze_stats_with_ai(
    summary: Dict, 
    api_base: str = "http://localhost:1234/v1", 
    model: str = "local-model"
) -> str:
    """
    Sends stylometric summary to a local LLM (like LM Studio) for interpretation.
    """
    
    # Construct the prompt
    stats_json = json.dumps(summary, indent=2)
    prompt = f"""
You are a Stylometrics & Forensic Linguistics Expert. Analyze the following quantitative stylometric data and provide a professional, qualitative "Stylistic Fingerprint" report.

Quantitative Data (Summary):
{stats_json}

Your analysis MUST include:
1. **Linguistic Texture**: Analyze MATTR and Yule's K to determine the richness and range of the vocabulary. Is it expansive or repetitive?
2. **Syntactic Architecture**: Interpret sentence length and complexity. Does the author use punchy, direct sentences or elaborate, subordinating structures?
3. **Habitual Markers**: Examine punctuation rates (commas, semicolons, etc.) and function word usage. These are the "unconscious" signals of authorship.
4. **Distance & Attribution**: Interpret Burrows' Delta and Semantic Similarity. Do the stylistic differences suggest distinct authorship, or are they consistent with topic-based shifts within the same voice?
5. **Key Identifying Traits**: For each corpus, list 2-3 defining stylistic "fingerprints".
6. **Executive Conclusion**: Summarize the likelihood of shared vs. distinct authorship based on the synthesis of all markers.

Format the output with clear Markdown headers. Keep it data-driven, analytical, and under 600 words.
"""

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a professional linguistic analyst specializing in stylometry."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{api_base.rstrip('/')}/chat/completions", data=data)
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data["choices"][0]["message"]["content"]
    except urllib.error.URLError as e:
        return f"AI Analysis failed: Could not connect to LM Studio at {api_base}. Ensure the server is running. (Error: {e})"
    except Exception as e:
        return f"AI Analysis encountered an error: {e}"
