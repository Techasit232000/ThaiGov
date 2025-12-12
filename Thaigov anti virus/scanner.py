"""scanner.py
Feature extraction and scanning logic for AI Virus Defender.
This code is defensive: it computes file features and marks suspicious files.
"""
import os
import math
import json
from collections import Counter

def file_entropy(path, block_size=1024):
    """Compute approximate Shannon entropy of file bytes."""
    try:
        with open(path, "rb") as f:
            data = f.read()
        if not data:
            return 0.0
        counts = Counter(data)
        length = len(data)
        ent = 0.0
        for c in counts.values():
            p = c / length
            ent -= p * math.log2(p)
        return ent
    except Exception as e:
        return 0.0

def byte_histogram(path, bins=16):
    """Return a normalized histogram of byte values grouped into bins."""
    try:
        with open(path, "rb") as f:
            data = f.read()
        if not data:
            return [0.0]*bins
        counts = [0]*bins
        for b in data:
            counts[b * bins // 256] += 1
        total = sum(counts)
        return [c/total for c in counts]
    except Exception:
        return [0.0]*bins

def extract_features(path):
    """Return a feature vector dict for a given file path."""
    try:
        size = os.path.getsize(path)
    except Exception:
        size = 0
    ent = file_entropy(path)
    hist = byte_histogram(path, bins=16)
    _, ext = os.path.splitext(path)
    ext = ext.lower().lstrip('.')
    # Simple one-hot for a few common extensions (others as 'other')
    common_ext = ['exe','dll','py','js','sh','bin','txt','doc','docx','pdf']
    ext_onehot = [1 if ext==e else 0 for e in common_ext]
    other_flag = 0 if ext in common_ext else 1
    features = {
        'size': size,
        'entropy': ent,
        'other_ext': other_flag,
        'ext': ext,
    }
    # add histogram and ext flags
    for i,v in enumerate(hist):
        features[f'hist_{i}'] = v
    for i,v in enumerate(ext_onehot):
        features[f'extflag_{i}'] = v
    return features

def heuristic_score(features):
    """Compute a simple heuristic suspicious score (0..1). Higher means more suspicious.""
    score = 0.0
    # entropy: executable-like files with very high entropy can be packed/encrypted
    score += max(0.0, (features['entropy'] - 6.0)/2.0) * 0.5
    # small executables or scripts under certain size ranges might be suspicious
    if features['size'] < 1024 and features['size'] > 0:
        score += 0.15
    # unknown extension increases suspicion slightly
    score += 0.1 * features['other_ext']
    # combine with some histogram signal (e.g., too-uniform distribution)
    avg_hist = sum(features[f'hist_{i}'] for i in range(16))/16.0
    uniformity = 1.0 - max(0.0, avg_hist - 1/16.0) # simplistic
    score += 0.05 * uniformity
    # clamp
    return min(max(score, 0.0), 1.0)

def scan_directory(path, model=None, threshold=0.6, recurse=True):
    """Scan files under path. If model provided (callable that accepts feature vector), use it to get prediction probability (malicious)."""
    results = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            fp = os.path.join(root, fn)
            features = extract_features(fp)
            heur = heuristic_score(features)
            ml_p = None
            if model is not None:
                try:
                    import numpy as np
                    # maintain feature ordering consistent with training script
                    feat_order = ['size','entropy'] + [f'hist_{i}' for i in range(16)] + [f'extflag_{i}' for i in range(10)] + ['other_ext']
                    arr = [features.get(k,0.0) for k in feat_order]
                    arr = np.array(arr).reshape(1,-1)
                    proba = model.predict_proba(arr)[0,1]
                    ml_p = float(proba)
                except Exception as e:
                    ml_p = None
            combined = heur
            if ml_p is not None:
                combined = 0.5*heur + 0.5*ml_p
            suspicious = combined >= threshold
            results.append({
                'path': fp,
                'size': features['size'],
                'entropy': features['entropy'],
                'heuristic': round(heur,3),
                'ml_prob': None if ml_p is None else round(ml_p,3),
                'combined': round(combined,3),
                'suspicious': suspicious
            })
        if not recurse:
            break
    return results

def quarantine_file(path, quarantine_dir):
    """Move file to quarantine directory. Does not execute files."""
    os.makedirs(quarantine_dir, exist_ok=True)
    base = os.path.basename(path)
    target = os.path.join(quarantine_dir, base)
    # be careful: do not overwrite existing files
    if os.path.exists(target):
        # append a number
        i=1
        while os.path.exists(f"{target}.q{i}"):
            i+=1
        target = f"{target}.q{i}"
    os.rename(path, target)
    return target

if __name__ == '__main__':
    import argparse, joblib
    p = argparse.ArgumentParser()
    p.add_argument('--path', default='test_samples', help='Directory to scan')
    p.add_argument('--model', default=None, help='Optional model.joblib path')
    p.add_argument('--threshold', type=float, default=0.6)
    p.add_argument('--quarantine', default=None, help='Move suspicious files to this dir')
    args = p.parse_args()
    model = None
    if args.model:
        try:
            model = joblib.load(args.model)
        except Exception as e:
            print('Could not load model:', e)
            model = None
    res = scan_directory(args.path, model=model, threshold=args.threshold)
    for r in res:
        print(f"{r['path']}: suspicious={r['suspicious']} combined={r['combined']} heuristic={r['heuristic']} ml_prob={r['ml_prob']}")
        if r['suspicious'] and args.quarantine:
            tgt = quarantine_file(r['path'], args.quarantine)
            print('Quarantined to', tgt)
