# Shared helpers for lub5 schedule generation.
import json, os
OUT = '/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/lub5'

def merge_rows(rows, svc_type):
    """rows: list of (item, action, note, marks). Keep rows whose marks contain svc_type.
    Rows with the same item+action are merged; their notes are joined."""
    out, idx = [], {}
    for item, action, note, marks in rows:
        if svc_type not in marks:
            continue
        key = (item, action)
        if key in idx:
            o = out[idx[key]]
            if note and note not in o.get('note', ''):
                o['note'] = (o['note'] + '; ' + note) if o.get('note') else note
        else:
            idx[key] = len(out)
            d = {'item': item, 'action': action}
            if note:
                d['note'] = note
            out.append(d)
    return out

def ab_services(interval_km, n, rows, pattern='AB'):
    """Services at interval_km*k (k=1..n). pattern gives the service type per position, cycling."""
    svcs = []
    for k in range(1, n + 1):
        t = pattern[(k - 1) % len(pattern)]
        svcs.append({'km': interval_km * k, 'items': merge_rows(rows, t)})
    return svcs

def write(d):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, d['id'] + '.json')
    with open(p, 'w', encoding='utf8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write('\n')
    return p
