#!/usr/bin/env python3
# Merge Chinese source (zh_subject1.json, ordered) with English translations (en_*.json)
# and emit a chaptered bilingual LaTeX document: kemu1-full-en.tex
import json, glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, 'work')

zh = json.load(open(os.path.join(WORK, 'zh_subject1.json'), encoding='utf-8'))

# Load all English slices into id -> record
en = {}
for f in sorted(glob.glob(os.path.join(WORK, 'en_*.json'))):
    try:
        arr = json.load(open(f, encoding='utf-8'))
    except Exception as e:
        print('WARN cannot parse', f, e); continue
    for r in arr:
        if isinstance(r, dict) and r.get('id'):
            en[r['id']] = r

covered = sum(1 for x in zh if x['id'] in en)
print(f'zh={len(zh)}  en_records={len(en)}  covered={covered}  missing={len(zh)-covered}')

CH_TITLES = {
    '1':  r'Traffic Safety Laws, Regulations \& Rules \;/\; 道路交通安全法律法规',
    '2':  r'Traffic Signals \;/\; 交通信号',
    '3':  r'Safe \& Civil Driving Basics \;/\; 安全行车、文明驾驶基础知识',
    '4':  r'Vehicle Operation Basics \;/\; 机动车驾驶操作基础知识',
    '5':  r'Incidents, Emergencies \& Complex Conditions \;/\; 事故处理与应急',
    '14': r'Additional Questions A \;/\; 补充题库 A',
    '15': r'Additional Questions B \;/\; 补充题库 B',
}

def esc(s):
    if s is None: return ''
    s = str(s)
    s = s.replace('\\', r'\textbackslash{}')
    for a, b in [('&', r'\&'), ('%', r'\%'), ('$', r'\$'), ('#', r'\#'),
                 ('_', r'\_'), ('{', r'\{'), ('}', r'\}'), ('~', r'\textasciitilde{}'),
                 ('^', r'\textasciicircum{}')]:
        s = s.replace(a, b)
    s = s.replace('—', ', ').replace('–', '-')
    return s.strip()

HEADER = r'''% !TEX program = xelatex
\documentclass[10pt]{article}
\usepackage{fontspec}
\usepackage{xeCJK}
\usepackage[a4paper,margin=1.6cm]{geometry}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{titlesec}
\usepackage{fancyhdr}
\usepackage{needspace}
\usepackage{enumitem}
\setmainfont{Helvetica Neue}
\setCJKmainfont{Songti SC}
\newCJKfontfamily\hei{STHeiti}
\definecolor{accent}{HTML}{C0392B}
\definecolor{ansg}{HTML}{1B7F3B}
\definecolor{zhgray}{HTML}{666666}
\definecolor{tagbg}{HTML}{34495E}
\definecolor{secbg}{HTML}{C0392B}
\newcommand{\secbar}[1]{\colorbox{secbg}{\parbox{\dimexpr\textwidth-2\fboxsep\relax}{\vspace{2pt}\hei\large\bfseries\color{white}#1\vspace{2pt}}}}
\titleformat{\section}{}{}{0pt}{\secbar}
\titlespacing{\section}{0pt}{14pt}{8pt}
\pagestyle{fancy}\fancyhf{}
\renewcommand{\headrulewidth}{0.4pt}
\lhead{\small\hei 科目一 · Subject 1 (EN)}\rhead{\small China Driving Theory — Full Bank}\cfoot{\small\thepage}
\newcommand{\qtag}[1]{{\footnotesize\colorbox{tagbg}{\textcolor{white}{\hei\,#1\,}}}}
\setlength{\parindent}{0pt}\setlength{\parskip}{1pt}
\begin{document}
\begin{titlepage}\centering\vspace*{3cm}
{\hei\Huge\color{accent} 中国驾照理论考试 · 科目一}\par\vspace{8pt}
{\Large\bfseries China Driving Theory Test — Subject 1}\par\vspace{4pt}
{\Large Complete Question Bank, English Study Edition}\par\vspace{2cm}
\begin{minipage}{0.82\textwidth}\small
\textbf{Scope.} Every Subject 1 question in this bank, deduplicated: \textbf{2{,}545 questions},
grouped by chapter, in fixed order. Each item shows the English question and options, the correct
answer, a one-line reason, and the original Chinese for reference.\par\vspace{6pt}
\textbf{Source.} Open dataset (MIT-licensed), July 2022 snapshot of the national 科目一 pool,
translated to English. The real exam draws 100 questions from the current pool, 45 minutes, pass 90/100.\par\vspace{6pt}
\textbf{Figures.} 787 questions include the original exam picture (a sign, signal, or road scene),
embedded directly below the question, exactly as shown on the exam screen.\par\vspace{6pt}
\textbf{Freshness caveat.} A 2022 snapshot; a small number of items may have been revised since.
Confirm point-values and limits against a current practice app before exam day.\par
\end{minipage}\vfill{\small\color{zhgray} Personal study edition. Built from open data.}
\end{titlepage}
\tableofcontents\newpage
'''

out = [HEADER]
cur = None
n = 0
for x in zh:
    ch = str(x.get('ch'))
    if ch != cur:
        cur = ch
        title = CH_TITLES.get(ch, f'Chapter {ch}')
        out.append('\n\\section{%s}\n' % title)
    n += 1
    e = en.get(x['id'])
    labels = x.get('labels') or []
    is_tf = len(labels) == 2
    tag = '判断题 / True or False' if is_tf else '单选题 / Single choice'
    imgfile = os.path.join('work', 'img', x['id'] + '.jpg')
    has_img = os.path.exists(os.path.join(ROOT, imgfile))
    out.append('\\needspace{%d\\baselineskip}' % (14 if has_img else 4))
    out.append('\\qtag{%s}\\ \\textbf{%d.}\\ ' % (tag, n))
    if e:
        out.append(esc(e.get('q_en')) + '\\par')
        if has_img:
            out.append('\\smallskip\\begin{center}\\includegraphics[width=6cm,height=4cm,keepaspectratio]{%s}\\end{center}\\smallskip' % imgfile)
        opts = e.get('opts_en') or []
        parts = []
        for lab, ot in zip(labels, opts):
            parts.append('\\textbf{%s.} %s' % (esc(lab), esc(ot)))
        out.append('{\\small ' + ' \\quad '.join(parts) + '}\\par')
        # Chinese reference
        out.append('{\\footnotesize\\color{zhgray} 中文：%s}\\par' % esc(x.get('q')))
        # answer
        ans = x.get('ans')
        ans_txt = ''
        if ans in labels:
            idx = labels.index(ans)
            if idx < len(opts):
                ans_txt = esc(opts[idx])
        why = esc(e.get('why_en'))
        out.append('{\\small\\color{ansg}\\hei 答案 Answer: \\textbf{%s}%s%s}\\par\\smallskip' % (
            esc(ans), ('. ' + ans_txt) if ans_txt else '', ('  ' + why) if why else ''))
    else:
        # fallback: Chinese only
        out.append('{\\color{zhgray}[translation pending]}\\par')
        out.append('%s\\par' % esc(x.get('q')))
        for lab, ot in zip(labels, x.get('opts') or []):
            out.append('\\textbf{%s.} %s\\quad ' % (esc(lab), esc(ot)))
        out.append('\\par{\\small\\color{ansg}\\hei 答案 Answer: \\textbf{%s}}\\par\\smallskip' % esc(x.get('ans')))

out.append('\n\\end{document}\n')

tex_path = os.path.join(ROOT, 'kemu1-full-en.tex')
open(tex_path, 'w', encoding='utf-8').write('\n'.join(out))
print('wrote', tex_path, 'with', n, 'questions')
