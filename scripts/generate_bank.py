"""Deterministic authored concept bank. No scraped items or invented exam metadata."""
import csv, json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
subjects = ['워드프로세싱 용어 및 기능', 'PC 운영체제', 'PC 기본상식']
subject = None
bank = []
for line in (root/'scripts/concepts.tsv').read_text().splitlines():
    if not line.strip(): continue
    if line.startswith('# '):
        subject = line[2:]; assert subject in subjects; continue
    stem, correct, *rest = line.split('|')
    assert len(rest) == 4
    distractors, explanation = rest[:3], rest[3]
    n = sum(q['subject'] == subject for q in bank) + 1
    answer = (n - 1) % 4 + 1
    choices = distractors[:]; choices.insert(answer-1, correct)
    bank.append(dict(id=f'WP-{subjects.index(subject)+1}-{n:03}', subject=subject,
        topic=stem.split('의')[0][:30], question=stem, choices=choices, answer=answer,
        explanation=explanation, difficulty='하', year=None, session=None,
        type='original', sourceUrl='https://github.com/YunSangYeong/Word-Processor-CBT/blob/main/docs/QUESTION_BANK.md',
        verificationStatus='reviewed',
        reviewNote='AI의 일반 지식으로 자체 작성. 문항·정답·오답 선택지·해설을 내부 검토함. 외부 전문가 검수 및 공식 출제기준 대조 미완료. 저장소 주소는 작성 위치이며 외부 정답 증빙이 아님.',
        version='main', rights='자체 제작 · CC BY 4.0 · Word-Processor-CBT contributors'))
assert len({q['id'] for q in bank}) == len(bank)
assert len({''.join(q['question'].split()) + '|'.join(sorted(q['choices'])) for q in bank}) == len(bank)
(root/'src/data/questions.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
example={**bank[0], 'id':'LOCAL-EXAMPLE-001', 'question':'직접 작성한 문항의 문제를 입력하세요.', 'verificationStatus':'pending', 'reviewNote':'출처·권한·정답 직접 확인 후 승인 필요'}
(root/'public/templates/questions.json').write_text(json.dumps([example],ensure_ascii=False,indent=2)+'\n')
fields=[k for k in example if k != 'choices']+['choice1','choice2','choice3','choice4']
with (root/'public/templates/questions.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n"); w.writeheader()
 w.writerow({**{k:v for k,v in example.items() if k!='choices'},**{f'choice{i+1}':c for i,c in enumerate(example['choices'])}})
print(json.dumps({'registered':len(bank),'shortfall':1000-len(bank),'subjects':{s:sum(q['subject']==s for q in bank) for s in subjects}},ensure_ascii=False))
