"""Reproducible structural audit. Similarity candidates are not a proof of semantics."""
import difflib
import hashlib
import json
import re
import unicodedata
from pathlib import Path

root = Path(__file__).resolve().parents[1]
raw = (root/'src/data/questions.json').read_bytes()
bank = json.loads(raw)

def normalize(value):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', value)).lower()

def fingerprint(q):
    return normalize('|'.join([q['question'], *sorted(q['choices'])]))

concepts = [q for q in bank if not q.get('calculation')]
variants = [q for q in bank if q.get('calculation')]
families = sorted({q['family'] for q in variants})
assert len(bank) == len({q['id'] for q in bank}) == len({fingerprint(q) for q in bank}) == 1000
assert len({normalize(q['question']) for q in bank}) == 1000
assert all(q['type']=='original' and q['year'] is None and q['session'] is None for q in bank)
pairs = []
for i,a in enumerate(concepts):
    for b in concepts[i+1:]:
        if a['subject'] != b['subject']:
            continue
        clean = lambda s: re.sub(r'\W','',s)
        score = difflib.SequenceMatcher(None, clean(a['question']), clean(b['question'])).ratio()
        if score >= .58:
            pairs.append(dict(ids=[a['id'],b['id']], similarity=round(score,4)))
pairs.sort(key=lambda row: (-row['similarity'], row['ids']))
report = dict(
    schema=1,
    bankSha256=hashlib.sha256(raw).hexdigest(),
    reviewedMeaning='작성자의 내부 검토; 외부 전문가 검수/공식 기준 대조 아님',
    counts=dict(total=len(bank), reviewed=sum(q['verificationStatus']=='reviewed' for q in bank),
                pending=sum(q['verificationStatus']=='pending' for q in bank),
                original=1000,past=0,reconstructed=0,conceptAndScenario=len(concepts),
                numericVariants=len(variants),numericFamilies=len(families),shortfall=0),
    subjects=[dict(subject=s,total=sum(q['subject']==s for q in bank),
                   conceptAndScenario=sum(q['subject']==s for q in concepts),
                   numericVariants=sum(q['subject']==s for q in variants))
              for s in dict.fromkeys(q['subject'] for q in bank)],
    families=[dict(family=f,kind=next(q['calculation']['kind'] for q in variants if q['family']==f),
                   count=sum(q['family']==f for q in variants),
                   distinctConditions=len({tuple(q['calculation']['values']) for q in variants if q['family']==f}))
              for f in families],
    exactDuplicateIds=0, normalizedDuplicateContent=0, normalizedDuplicateStems=0,
    conceptSimilarityScreen=dict(threshold=.58,candidateCount=len(pairs),candidates=pairs,
        note='문자열 유사도 후보 추출이며 의미 중복 여부를 자동 판정한 것이 아님.'),
    numericVerification='tests/numeric-bank.test.ts: Python 생성 경로와 별개인 재계산·역산·블록 할당 시뮬레이션·TextEncoder·진수 파싱',
)
(root/'docs/BANK_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report['counts'],ensure_ascii=False))
print('Same-subject concept similarity candidates:',len(pairs))
