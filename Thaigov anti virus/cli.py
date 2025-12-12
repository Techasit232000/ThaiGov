"""Simple CLI for AI Virus Defender"""
import argparse, sys
from scanner import scan_directory
def load_model(path):
    try:
        import joblib
        return joblib.load(path)
    except Exception as e:
        print('Could not load model:', e)
        return None

def cmd_scan(args):
    model = None
    if args.model:
        model = load_model(args.model)
    res = scan_directory(args.path, model=model, threshold=args.threshold)
    suspicious = [r for r in res if r['suspicious']]
    print('\nScan complete. Files scanned:', len(res))
    print('Suspicious files:', len(suspicious))
    for r in suspicious:
        print('-', r['path'], 'combined=', r['combined'])
    if args.quarantine and suspicious:
        from scanner import quarantine_file
        for r in suspicious:
            quarantine_file(r['path'], args.quarantine)
        print('Moved suspicious files to', args.quarantine)

def main():
    p = argparse.ArgumentParser(prog='ai-virus-defender')
    sub = p.add_subparsers(dest='cmd')
    sscan = sub.add_parser('scan', help='Scan directory')
    sscan.add_argument('--path', default='test_samples')
    sscan.add_argument('--model', default=None)
    sscan.add_argument('--threshold', type=float, default=0.6)
    sscan.add_argument('--quarantine', default=None)
    args = p.parse_args()
    if args.cmd == 'scan':
        cmd_scan(args)
    else:
        p.print_help()

if __name__ == '__main__':
    main()
