import json,pathlib,re,time,urllib.request,urllib.error,sys
p=pathlib.Path(__file__).resolve().parent; data=json.loads((p/'subject4_translations.json').read_text(encoding='utf-8')); reviews=json.loads((p/'subject4_review_results.json').read_text(encoding='utf-8')); key=(pathlib.Path.home()/'Desktop/openrouter_key.txt').read_text(encoding='utf-8-sig').strip()
if '=' in key and not key.startswith('sk-'): key=key.split('=',1)[1].strip().strip('"\'')
output=p/'subject4_adjudication.json'; done=json.loads(output.read_text(encoding='utf-8')) if output.exists() else {}
items=[]
for x in data:
 f=reviews[x['id']]['findings']
 if f and x['id'] not in done: items.append({'id':x['id'],'question_zh':x['question_zh'],'options_zh':x['options_zh'],'question_en':x['question_en'],'options_en':x['options_en'],'answer':x['answer'],'findings':[{'index':i,**v} for i,v in enumerate(f)]})
prompt='You are auditing suggestions from an unreliable model. For EACH finding, compare the suggestion to the supplied ORIGINAL CHINESE and CURRENT English. Do not rely on the finding claim: many are false, reverse meaning, propose legal corrections, reveal answers, or ask for trivial punctuation. Faithfully preserve unsafe or false statements and do not alter answers. The original image may be unavailable. Return JSON array one per input {"id":...,"decisions":[{"index":0,"decision":"apply" or "already_present" or "reject" or "uncertain", "reason":"short source-based reason", "replacement":"exact complete replacement for the specific English question or option only if decision is apply; otherwise empty"}]}. Include exactly one decision for every input finding index. Choose uncertain when unsure. No prose or markdown.'
for start in range(0,len(items),3):
 batch=items[start:start+3]; payload={'model':'xingchen-agi/xing4.0-29b-a4b:free','messages':[{'role':'system','content':prompt},{'role':'user','content':json.dumps(batch,ensure_ascii=False)}],'reasoning':{'enabled':False},'temperature':0,'max_tokens':6000}
 for attempt in range(4):
  try:
   req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',data=json.dumps(payload,ensure_ascii=False).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
   with urllib.request.urlopen(req,timeout=180) as resp: res=json.load(resp)
   c=res['choices'][0]; raw=re.sub(r'^```(?:json)?\s*|\s*```$','',c['message']['content'].strip()); result=json.loads(raw)
   if c.get('finish_reason')=='length' or not isinstance(result,list) or len(result)!=len(batch) or {v['id'] for v in result}!={v['id'] for v in batch}: raise ValueError('invalid IDs or truncated')
   for v in result:
    x=next(z for z in batch if z['id']==v['id']); ds=v['decisions']
    if len(ds)!=len(x['findings']) or {z['index'] for z in ds}!=set(range(len(x['findings']))): raise ValueError('missing decisions')
    if any(z.get('decision') not in ('apply','reject','uncertain','already_present') or not isinstance(z.get('reason'),str) or not isinstance(z.get('replacement'),str) for z in ds): raise ValueError('invalid decision')
   for v in result: done[v['id']]={**v, 'review_model': 'xingchen-agi/xing4.0-29b-a4b:free'}
   tmp=output.with_suffix('.tmp'); tmp.write_text(json.dumps(done,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); tmp.replace(output)
   print(f'Adjudicated {len(done)} / 261 records',flush=True); break
  except (urllib.error.URLError,ValueError,KeyError,TypeError,TimeoutError) as e:
   print('Batch error',type(e).__name__,str(e)[:120],flush=True)
   if attempt==3: sys.exit(1)
   time.sleep(4*(attempt+1))
 time.sleep(1)



