"""Translate the collected HTML text extracts with the Subject 4 model.

Outputs resumable bilingual chunks; these are unreviewed machine translations.
"""
import hashlib
import json
import os
import pathlib
import re
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'data/traffic-laws'
OUTPUT = SOURCE / 'translations'
MODEL = None


def chunks(text, limit=1800):
    # Preserve the entire source, including extracted site navigation.
    pieces = re.findall(r'.*?(?:\n|$)', text)
    pending = ''
    for piece in pieces:
        while piece:
            room = limit - len(pending)
            pending += piece[:room]
            piece = piece[room:]
            if len(pending) == limit:
                yield pending
                pending = ''
    if pending:
        yield pending


def main():
    global MODEL
    MODEL = os.environ.get('OPENROUTER_MODEL', '').strip()
    if not MODEL: raise SystemExit('Set OPENROUTER_MODEL to the model ID to use')
    key = (pathlib.Path.home() / 'Desktop' / 'openrouter_key.txt').read_text(encoding='utf-8-sig').strip()
    if '=' in key and not key.startswith('sk-'):
        key = key.split('=', 1)[1].strip().strip('"\'')
    OUTPUT.mkdir(exist_ok=True)
    sources = sorted(SOURCE.glob('*.txt'))
    if len(sys.argv) > 1:
        requested = set(sys.argv[1:])
        sources = [source for source in sources if source.stem in requested]
        if {source.stem for source in sources} != requested:
            raise ValueError('Unknown source name')
    for source in sources:
        raw = source.read_text(encoding='utf-8')
        parts = list(chunks(raw))
        path = OUTPUT / (source.stem + '.json')
        result = json.loads(path.read_text(encoding='utf-8')) if path.exists() else []
        for i, item in enumerate(result):
            if item['text_zh'] != parts[i]:
                raise ValueError(f'Source changed: {source.name} chunk {i+1}')
        for i in range(len(result)):
            if len(re.findall(r'[\u4e00-\u9fff]', result[i]['text_en'])) <= 100:
                continue
            repaired = []
            for start in range(0, len(parts[i]), 450):
                prompt = ('Translate faithfully to English, retaining all legal conditions and details. '
                          'Return English translation only:\n' + parts[i][start:start + 450])
                payload = json.dumps({'model': MODEL, 'messages': [
                    {'role': 'system', 'content': 'You are a professional legal translator. Translate Chinese into English.'},
                    {'role': 'user', 'content': prompt}], 'reasoning': {'enabled': False},
                    'temperature': 0.2, 'max_tokens': 3000}, ensure_ascii=False).encode()
                req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=payload,
                                             headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
                for attempt in range(4):
                    with urllib.request.urlopen(req, timeout=180) as response:
                        answer = json.load(response)['choices'][0]
                    translated = answer['message']['content'].strip()
                    if translated and answer.get('finish_reason') != 'length' and len(re.findall(r'[\u4e00-\u9fff]', translated)) <= 50:
                        break
                    if attempt == 3:
                        raise ValueError(f'Retry incomplete: {source.name} chunk {i+1}, offset {start}')
                    time.sleep(2)
                repaired.append(translated)
            result[i]['text_en'] = '\n'.join(repaired)
            result[i]['translation_note'] = 'Retried in smaller pieces after substantial Chinese remained.'
            tmp = path.with_suffix('.tmp')
            tmp.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            tmp.replace(path)
            print(f'{source.name}: repaired chunk {i+1}', flush=True)
        for i in range(len(result), len(parts)):
            prompt = ('Translate this Chinese legal source text into accurate, clear English. '
                      'Translate every part without summarizing or adding content. Preserve article '
                      'numbers, conditions, exceptions, negations, dates, amounts and references. '
                      'The text may start or end mid-sentence. Return only the translation.\n\n' + parts[i])
            payload = json.dumps({'model': MODEL, 'messages': [{'role': 'user', 'content': prompt}],
                                  'reasoning': {'enabled': False}, 'temperature': 0.2, 'max_tokens': 6000}, ensure_ascii=False).encode()
            for attempt in range(4):
                try:
                    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=payload,
                                                 headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
                    with urllib.request.urlopen(req, timeout=180) as response:
                        answer = json.load(response)['choices'][0]
                    translated = answer['message']['content'].strip()
                    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', translated))
                    if not translated or answer.get('finish_reason') == 'length' or chinese_chars > 100:
                        raise ValueError('Empty or truncated translation')
                    break
                except Exception:
                    if attempt == 3:
                        raise
                    time.sleep(5 * (attempt + 1))
            result.append({'chunk': i + 1, 'text_zh': parts[i], 'text_en': translated,
                           'translation_model': MODEL, 'translation_review_required': True,
                           'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
            tmp = path.with_suffix('.tmp')
            tmp.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            tmp.replace(path)
            print(f'{source.name}: {i+1}/{len(parts)}', flush=True)


if __name__ == '__main__':
    main()
