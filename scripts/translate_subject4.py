import os, json, pathlib, urllib.request, urllib.error, time, re, sys
model = os.environ.get('OPENROUTER_MODEL', '').strip()
if not model: raise SystemExit('Set OPENROUTER_MODEL to the model ID to use')
base=pathlib.Path(__file__).resolve().parent.parent
src=json.loads((base/'data/subject4/trllm_course4_cleaned.json').read_text(encoding='utf-8'))
out=base/'data/subject4/subject4_translations.json'
completed={r['id']:r for r in json.loads(out.read_text(encoding='utf-8'))} if out.exists() else {}
key=pathlib.Path.home().joinpath('Desktop','openrouter_key.txt').read_text().strip()
if '=' in key and not key.startswith('sk-'): key=key.split('=',1)[1].strip().strip('"\'')
for start in range(0,len(src),20):
 batch=[x for x in src[start:start+20] if x['id'] not in completed]
 if not batch: continue
 payload=[{'id':x['id'],'question':x['question_zh'],'options':x['options_zh']} for x in batch]
 prompt='Translate these Chinese Subject 4 driving-test questions and each answer option into clear, idiomatic English. Preserve exact meaning, negations, numbers, names, option labels, and whether each statement is true or false. Do not correct unsafe statements or change answer choices. Translate 正确/错误 as True/False. Do not add explanations or infer details from unseen images. Return only a JSON array, one object per input, with fields id, question_en, options_en (a string preserving each option label on its own line). No markdown.\n'+json.dumps(payload,ensure_ascii=False)
 body=json.dumps({'model':model,'messages':[{'role':'user','content':prompt}],'reasoning':{'enabled':False},'temperature':0.2,'max_tokens':6000},ensure_ascii=False).encode()
 for attempt in range(4):
  try:
   req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',data=body,headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
   with urllib.request.urlopen(req,timeout=180) as response: data=json.load(response)
   raw=data['choices'][0]['message']['content']; raw=re.sub(r'^```(?:json)?\s*|\s*```$','',raw.strip())
   result=json.loads(raw)
   assert isinstance(result,list) and {x['id'] for x in result}=={x['id'] for x in batch} and len(result)==len(batch)
   for original in batch:
    translated=next(x for x in result if x['id']==original['id'])
    assert all(isinstance(translated.get(k),str) and translated[k].strip() for k in ['question_en','options_en'])
    labels=lambda s: re.findall(r'(?<![A-Za-z])([A-D])[、.．:：)]',s)
    assert labels(original['options_zh'])==labels(translated['options_en']) or (original['id']=='trllm_subj4_517' and labels(translated['options_en'])==['A','B','C','D']), original['id']
    completed[original['id']]={**original,**translated}
   tmp=out.with_suffix('.tmp'); tmp.write_text(json.dumps([completed[x['id']] for x in src if x['id'] in completed],ensure_ascii=False,indent=2),encoding='utf-8'); tmp.replace(out)
   print('Translated',len(completed),'of',len(src),flush=True); break
  except Exception as e:
   print('Batch',start,'attempt',attempt+1,'failed',str(e)[:300],flush=True)
   if attempt==3: sys.exit(1)
   time.sleep(5*(attempt+1))
