"""train_model.py
Train a simple RandomForest classifier on synthetic data for demonstration.

This script generates synthetic 'benign' and 'synthetic-malicious' samples using heuristics
and trains a model to separate them. **No real malware is used.**
"""
import os
import argparse
import random
import numpy as np

def generate_sample_features(n=1000, label='benign', rng_seed=None):
    random.seed(rng_seed)
    X = []
    y = []
    for _ in range(n):
        if label=='benign':
            size = int(abs(random.gauss(15000, 30000)))  # many small and medium files
            entropy = max(0.0, min(8.0, random.gauss(4.5, 1.0)))
            other_ext = 0 if random.random() < 0.9 else 1
        else:
            # synthetic "malicious" style: high entropy, small/packed
            size = int(abs(random.gauss(4000, 8000)))
            entropy = max(0.0, min(8.0, random.gauss(7.0, 0.8)))
            other_ext = 1 if random.random() < 0.7 else 0
        # histogram features: random vector that sums to 1
        hist = np.random.dirichlet([1]*16).tolist()
        extflags = [0]*10
        # random choose some ext flags rarely
        if random.random() < 0.15:
            extflags[random.randint(0,9)] = 1
        feat = [size, entropy] + hist + extflags + [other_ext]
        X.append(feat)
        y.append(1 if label!='benign' else 0)
    return X, y

def build_dataset(n_per_class=500, seed=42):
    Xb, yb = generate_sample_features(n_per_class, 'benign', rng_seed=seed)
    Xm, ym = generate_sample_features(n_per_class, 'malicious', rng_seed=seed+1)
    X = Xb + Xm
    y = yb + ym
    import numpy as np
    X = np.array(X)
    y = np.array(y)
    # shuffle
    idx = np.arange(len(y))
    np.random.seed(seed)
    np.random.shuffle(idx)
    return X[idx], y[idx]

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', default='model.joblib')
    p.add_argument('--n', type=int, default=800)
    args = p.parse_args()
    X,y = build_dataset(n_per_class=args.n//2, seed=123)
    try:
        from sklearn.ensemble import RandomForestClassifier
        from joblib import dump
        clf = RandomForestClassifier(n_estimators=100, random_state=0)
        clf.fit(X,y)
        dump(clf, args.output)
        print('Model saved to', args.output)
    except Exception as e:
        print('Training requires scikit-learn and joblib. Error:', e)
        print('You can still use heuristic scanner without a model.')
