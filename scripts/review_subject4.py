import argparse, datetime, hashlib, json, os, pathlib, re, sys, time, urllib.request, urllib.error

BASE = pathlib.Path(__file__).resolve().parent.parent
MODEL = None
DATA = BASE / 'data/subject4/subject4_translations.json'
RESULTS = BASE / 'reports/subject4/subject4_review_results.json'
REPORT = BASE / 'reports/subject4/SUBJECT4_MODEL_FINDINGS.md'
KEY = pathlib.Path.home() / 'Desktop' / 'openrouter_key.txt'

def digest(record):
    return hashlib.sha256(json.dumps({k:record.get(k) for k in ('id','question_zh','options_zh','question_en','options_en','answer')},ensure_ascii=False,sort_keys=True).encode()).hexdigest()

def save_json(path, value):
    tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    tmp.replace(path)

def report(records, reviews, errors):
    lines=['# Subject 4 machine translation review', '', f'Updated: {datetime.datetime.now().astimezone().isoformat(timespec="seconds")}', f'Model: `{MODEL}`', f'Completed: {len(reviews)} / {len(records)}', '', 'This is a machine-generated review, not human verification. Findings may contain false positives, minor stylistic suggestions (including option punctuation), or miss errors. Review flags in the dataset have not been cleared. Source and legal accuracy were not verified.', '']
    for x in records:
        r=reviews.get(x['id'])
        if not r: continue
        findings=r['findings']
        if findings:
            lines += [f'## {x["id"]}', '']
            for f in findings:
                lines.append(f'- **{f["field"]}**: {f["issue"]} Suggested wording: {f["suggestion"]}')
            lines.append('')
    lines += ['## Coverage', '', f'- Reviewed with findings: {sum(bool(x["findings"]) for x in reviews.values())}', f'- Reviewed without findings: {sum(not x["findings"] for x in reviews.values())}', f'- Not yet reviewed: {len(records)-len(reviews)}']
    if errors: lines += ['', '## Last error', '', errors[-1]]
    tmp=REPORT.with_suffix('.tmp'); tmp.write_text('\n'.join(lines)+'\n',encoding='utf-8'); tmp.replace(REPORT)

def main():
    global MODEL
    p=argparse.ArgumentParser(); p.add_argument('--batch-size',type=int,default=5); p.add_argument('--max-batches',type=int,default=0); p.add_argument('--delay',type=float,default=2); p.add_argument('--model', default=os.environ.get('OPENROUTER_MODEL')); args=p.parse_args()
    MODEL = (args.model or '').strip()
    if not MODEL: p.error('Specify --model or set OPENROUTER_MODEL')
    if not 1 <= args.batch_size <= 20: p.error('batch size must be between 1 and 20')
    key=os.environ.get('OPENROUTER_API_KEY','').strip() or KEY.read_text(encoding='utf-8-sig').strip()
    if '=' in key and not key.startswith('sk-'): key=key.split('=',1)[1].strip().strip('"\'')
    if not key: raise SystemExit('OpenRouter API key is empty.')
    records=json.loads(DATA.read_text(encoding='utf-8-sig')); old=json.loads(RESULTS.read_text(encoding='utf-8')) if RESULTS.exists() else {}
    reviews={x['id']:old[x['id']] for x in records if x['id'] in old and old[x['id']].get('input_sha256')==digest(x)}
    todo=[x for x in records if x['id'] not in reviews]; errors=[]; report(records,reviews,errors)
    instruction=('Review each Chinese driving-test question and option against its English translation, line by line. Check omissions, additions, negation, quantities, option labels and meaning. Unsafe or false statements must remain faithfully translated. Do not correct legal facts or answers. Do not infer missing images or source text. Return only a JSON array, exactly one object per input, in the same order: {"id":"...","findings":[{"field":"question_en or option label","issue":"specific discrepancy","suggestion":"corrected English"}]}. Use an empty findings array when no material translation issue is found. Include all issues, including untranslated Chinese.')
    for start in range(0,len(todo),args.batch_size):
        if args.max_batches and start//args.batch_size>=args.max_batches: break
        batch=todo[start:start+args.batch_size]; payload=[{k:x[k] for k in ('id','question_zh','options_zh','question_en','options_en','answer')} for x in batch]
        body=json.dumps({'model':MODEL,'messages':[{'role':'system','content':instruction},{'role':'user','content':json.dumps(payload,ensure_ascii=False)}],'reasoning':{'enabled':False},'temperature':0,'max_tokens':5000},ensure_ascii=False).encode('utf-8')
        success=False
        for attempt in range(4):
            try:
                req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',data=body,headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','X-Title':'Subject 4 Translation Review'})
                with urllib.request.urlopen(req,timeout=180) as response: result=json.load(response)
                choice=result['choices'][0]
                if choice.get('finish_reason')=='length': raise ValueError('Model response was truncated')
                raw=choice['message']['content'].strip(); raw=re.sub(r'^```(?:json)?\s*|\s*```$','',raw)
                parsed=json.loads(raw)
                if not isinstance(parsed,list) or len(parsed)!=len(batch) or {r.get('id') for r in parsed}!={r['id'] for r in batch}: raise ValueError('Missing, duplicate, or unexpected record IDs')
                for r in parsed:
                    if not isinstance(r.get('findings'),list): raise ValueError('Invalid findings')
                    for f in r['findings']:
                        if not isinstance(f,dict) or any(not isinstance(f.get(k),str) for k in ('field','issue','suggestion')): raise ValueError('Invalid finding')
                for r in parsed:
                    original=next(x for x in batch if x['id']==r['id']); reviews[r['id']]={**r,'input_sha256':digest(original),'model':MODEL}
                save_json(RESULTS,reviews); report(records,reviews,errors)
                print(f'Reviewed {len(reviews)}/{len(records)}',flush=True); success=True; break
            except urllib.error.HTTPError as e:
                msg=f'HTTP {e.code}'; retry=e.code in (408,429,500,502,503,504)
                if e.code==429: msg+=' (rate or quota limit)'
                print(f'Batch {start}: {msg}',flush=True)
                if not retry or e.code==429: errors.append(msg); break
            except (ValueError,KeyError,TypeError,urllib.error.URLError,TimeoutError) as e:
                msg=f'{type(e).__name__}: {str(e)[:180]}'; print(f'Batch {start}: {msg}',flush=True)
            if attempt<3: time.sleep(3*(attempt+1))
        if not success:
            if not errors: errors.append(msg)
            report(records,reviews,errors); print('Stopped; rerun to resume.',flush=True); return 1
        time.sleep(args.delay)
    report(records,reviews,errors); return 0
if __name__=='__main__': sys.exit(main())
