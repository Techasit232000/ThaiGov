# AI Virus Defender

**Defensive project**: a simple, readable example of a local "AI-assisted" virus scanner.
It is designed for educational and defensive use only — it **does not** include any malware, and it won't attempt to remove system files.

Features:
- Heuristic scanner (entropy, file size, extension checks)
- Optional ML model training (uses scikit-learn) to classify files based on simple features
- CLI to scan directories and quarantine suspicious files
- Safe synthetic dataset generator for demo/training

**Important**
- Run on a copy of files you control.
- Do **not** run as Administrator/root on a production system.
- This tool is a starting point — not a substitute for professional antivirus software.

## Quick start

1. Create a Python virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Train a demo model (optional):
```bash
python train_model.py --output model.joblib
```

3. Scan a directory:
```bash
python cli.py scan --path ./test_samples --model model.joblib
```

4. Quarantine suspicious files (scan will show suggested quarantine path).

## Repository layout
- `scanner.py` — main scanning and feature extraction logic
- `train_model.py` — trains a RandomForest on synthetic data (benign vs synthetic-malicious)
- `cli.py` — command-line interface
- `test_samples/` — small synthetic files used for demo
- `requirements.txt`, `LICENSE`, `.gitignore`

## License
MIT — see LICENSE file.
