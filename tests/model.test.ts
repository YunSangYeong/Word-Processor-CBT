import { createHash } from 'node:crypto';
import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { BASE_BANK as bank, SUBJECTS, STORAGE_KEY, createExam, grade, emptyStore, answerExam, submitExam, remainingSeconds, restoreStore, startPractice, checkPractice, nextPractice, importQuestions, validateQuestion, fingerprint, parseCsv } from '../src/model';
import type { Store } from '../src/model';
import { PROFILE } from '../src/qualification';
describe('워드프로세서 문제은행과 출처', () => {
  it('기존 120개 전체 필드와 ID를 그대로 보존',()=>{
    expect(createHash('sha256').update(JSON.stringify(bank.slice(0,120))).digest('hex')).toBe('838c33fe75352198c1f3f5d654d8166be70f1f089ebf86e215fbe4e3997bfd31');
  });
  it('1000개 내부 검토 문항·과목별 분포·부족0을 정확히 집계한다', () => {
    expect(bank).toHaveLength(1000);
    expect(new Set(bank.map(q=>q.id)).size).toBe(1000);
    expect(new Set(bank.map(fingerprint)).size).toBe(1000);
    SUBJECTS.forEach((s,i)=>expect(bank.filter(q=>q.subject===s)).toHaveLength([340,340,320][i]));
    expect(PROFILE.targetReviewedCount-bank.length).toBe(0);
    expect(STORAGE_KEY).toBe('word-processor-cbt:v1');
  });
  for (const q of bank) it(`${q.id}: 단일 정답·출처·확인 한계·연도 미부여`, () => {
    expect(()=>validateQuestion(q)).not.toThrow();
    expect(q.type).toBe('original'); expect(q.year).toBeNull(); expect(q.session).toBeNull();
    expect(q.verificationStatus).toBe('reviewed');
    expect(q.reviewNote).toContain('AI의 일반 지식');
    expect(q.reviewNote).toContain('외부 전문가');
    expect(q.explanation.length).toBeGreaterThan(40);
    if (q.calculation) expect(q.family).toBeTruthy();
    else expect(q.family).toBeUndefined();
    expect(q.rights).toContain('CC BY 4.0');
  });
  it('원고에서 재생성해도 동일한 JSON',()=>{
    const before=readFileSync('src/data/questions.json','utf8');
    execFileSync('python3',['scripts/generate_bank.py']);
    expect(readFileSync('src/data/questions.json','utf8')).toBe(before);
  });
});
function withCounts(counts: number[]) {
  const e=createExam(bank,'main',1000); e.answers={};
  SUBJECTS.forEach((s,i)=>e.questions.filter(q=>q.subject===s).slice(0,counts[i]).forEach(q=>e.answers[q.id]=q.answer));
  return e;
}
describe('시간·과목별 과락·합격 경계',()=>{
  it('과목별20·고유60·60분·검증 대기 제외',()=>{
    const e=createExam([...bank,{...bank[0],id:'pending',verificationStatus:'pending'}],'main',1000);
    expect(e.questions).toHaveLength(PROFILE.questionCount);
    expect(new Set(e.questions.map(q=>q.id)).size).toBe(60);
    SUBJECTS.forEach(s=>expect(e.questions.filter(q=>q.subject===s)).toHaveLength(20));
    expect(e.deadline-e.startedAt).toBe(3600000);
    expect(e.questions.every(q=>q.verificationStatus==='reviewed')).toBe(true);
  });
  it('과목 부족 시 시험을 만들지 않음',()=>expect(()=>createExam(bank.filter(q=>q.subject!==SUBJECTS[0]),'main')).toThrow());
  it.each([
    [[12,12,12],60,true], [[11,12,12],58.3,false],
    [[7,20,20],78.3,false], [[8,8,20],60,true],
    [[8,8,19],58.3,false], [[0,20,20],66.7,false],
    [[20,20,20],100,true], [[0,0,0],0,false],
  ])('정답 분포 %j → 점수 %s·합격 %s',(counts,score,passed)=>{
    const g=grade(withCounts(counts as number[])); expect(g.score).toBe(score);expect(g.passed).toBe(passed);
  });
  it('미응답은 오답이며 결과에 별도로 집계',()=>{ const g=grade(withCounts([8,8,20]));expect(g.unanswered).toBe(24);expect(g.wrong).toBe(24); });
  it('만료 직전 답안 변경 가능, 만료 경계 답안 거부 및 단 한번 제출',()=>{
    const e=withCounts([0,0,0]);let s: Store={...emptyStore(),exam:e};
    s=answerExam(s,e.questions[0].id,1,e.deadline-1);
    expect(s.exam?.answers[e.questions[0].id]).toBe(1);
    const expired=answerExam(s,e.questions[1].id,2,e.deadline);
    expect(expired.exam).toBeNull();expect(expired.results[0].reason).toBe('timeout');
    expect(expired.results[0].answers[e.questions[1].id]).toBeUndefined();
    expect(submitExam(expired)).toBe(expired);
  });
  it('남은 초 올림과 만료시 0',()=>{expect(remainingSeconds(1001,1000)).toBe(1);expect(remainingSeconds(1000,1001)).toBe(0);});
  it('재접속시 절대시각 보존·손상 데이터 거부',()=>{
    const s={...emptyStore(),exam:createExam(bank,'main',1000)};
    expect(restoreStore(JSON.stringify(s))).toEqual(s);
    expect(()=>restoreStore('{broken')).toThrow();
    expect(()=>restoreStore(JSON.stringify({...s,exam:{...s.exam,deadline:1234}}))).toThrow();
  });
});
describe('학습·복습·가져오기',()=>{
  it('순회 내 중복 없음·과목 필터·채점 한번·정답 재학습으로 오답 해제',()=>{
    let s: Store={...emptyStore(),practice:startPractice(bank,'main',SUBJECTS[0])};
    const seen=new Set<string>();
    for(let i=0;i<bank.filter(q=>q.subject===SUBJECTS[0]).length;i++) {
      const p=s.practice!;const q=bank.find(q=>q.id===p.currentId)!;
      expect(q.subject).toBe(SUBJECTS[0]);expect(seen.has(q.id)).toBe(false);seen.add(q.id);
      s={...s,practice:{...p,selected:q.answer}};
      s=checkPractice(s,bank);expect(checkPractice(s,bank)).toBe(s);
      s={...s,practice:nextPractice(s.practice!,bank)};
    }
    expect(s.attempts).toHaveLength(340);
    const q=bank[0];let wrong={...emptyStore(),wrongIds:[q.id],practice:{...startPractice(bank,'main','전체',[q.id]),selected:q.answer}};
    expect(checkPractice(wrong,bank).wrongIds).toEqual([]);
  });
  it('보기 순서가 달라도 중복 제외·가져온 검수 완료도 강제로 검증 대기',()=>{
    const same={...bank[0],id:'DUP',choices:[...bank[0].choices].reverse()};
    const custom={...bank[0],id:'LOCAL',question:'직접 검토할 새 문항'};
    const r=importQuestions([same,custom],bank);expect(r.duplicates).toBe(1);expect(r.added[0].verificationStatus).toBe('pending');
  });
  it('오류 행이 섞이면 원자적으로 등록 거부',()=>expect(()=>importQuestions([{...bank[0],id:'LOCAL',question:'새 문항'},{}],bank)).toThrow('2번 문항'));
  it('자체 제작에 연도·회차를 부여하지 못함',()=>expect(()=>validateQuestion({...bank[0],year:2025,session:'1'})).toThrow());
  it('CSV 양식은 실제로 파싱·검증 가능',()=>{const rows=parseCsv(readFileSync('public/templates/questions.csv','utf8'));expect(()=>validateQuestion(rows[0])).not.toThrow();});
  it('고유 계열을 우선 추출하고 부족분만 다른 변형으로 보충',()=>{
    const familyBank=bank.map((q,i)=>({...q,family:`${q.subject}-${i%22}`}));
    const e=createExam(familyBank,'main');
    SUBJECTS.forEach(s=>expect(new Set(e.questions.filter(q=>q.subject===s).map(q=>q.family)).size).toBe(20));
  });
});

describe('감사 기록',()=>{
  it('현재 기본 JSON 해시·수량·과목별 합계가 감사 파일과 일치',()=>{
    const raw=readFileSync('src/data/questions.json');
    const audit=JSON.parse(readFileSync('docs/BANK_AUDIT.json','utf8'));
    expect(audit.bankSha256).toBe(createHash('sha256').update(raw).digest('hex'));
    expect(audit.counts).toMatchObject({total:1000,reviewed:1000,pending:0,conceptAndScenario:420,numericVariants:580,numericFamilies:29,shortfall:0});
    expect(audit.subjects.map((s:{total:number})=>s.total)).toEqual([340,340,320]);
    expect(audit.families.every((f:{count:number;distinctConditions:number})=>f.count===20&&f.distinctConditions===20)).toBe(true);
    expect(audit.normalizedDuplicateContent).toBe(0);
  });
});
