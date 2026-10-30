import { describe, expect, it } from 'vitest';
import { BASE_BANK as bank, SUBJECTS, createExam } from '../src/model';

// Independent of Python generation. Discrete allocation is simulated; simple
// quantities are reconstructed with inverse relations. Binary/hex inputs are
// parsed from the visible prompt, not copied from the authored expected value.
function allocationCount(amount:number,block:number) {
  let count=0,remaining=amount;
  while(remaining>0) { remaining-=block;count++; }
  return count;
}
const numeric=bank.filter(q=>q.calculation);
describe('계산 조건 변형 29유형·580조건의 별도 재계산',()=>{
  it('420개 개념·사례형 + 29유형×20조건이며 숫자 조건이 중복되지 않는다',()=>{
    expect(numeric).toHaveLength(580);
    expect(bank.filter(q=>!q.calculation)).toHaveLength(420);
    const families=new Set(numeric.map(q=>q.family));expect(families.size).toBe(29);
    for(const family of families) {
      const rows=numeric.filter(q=>q.family===family);
      expect(rows).toHaveLength(20);
      expect(new Set(rows.map(q=>JSON.stringify(q.calculation!.values))).size).toBe(20);
      expect(new Set(rows.map(q=>q.calculation!.kind)).size).toBe(1);
    }
  });
  it('현재 1000문항에서 실전 추출은 과목별 서로 다른 20그룹을 유지',()=>{
    for(let run=0;run<30;run++) {
      const exam=createExam(bank,'main');
      for(const subject of SUBJECTS) {
        const questions=exam.questions.filter(q=>q.subject===subject);
        expect(questions).toHaveLength(20);
        expect(new Set(questions.map(q=>q.family||q.id)).size).toBe(20);
      }
    }
  });
  for(const q of numeric) it(`${q.id}: 독립 재계산·단위·보기`,()=>{
    const c=q.calculation!,v=c.values,r=c.result;
    const assert=(n:number)=>expect(r,q.id).toBeCloseTo(n,8);
    switch(c.kind) {
      case 'printable-width': expect(r+v[1]+v[2]).toBe(v[0]);break;
      case 'printable-height': expect(r+v[1]+v[2]).toBe(v[0]);break;
      case 'column-width': expect(r*v[1]+(v[1]-1)*v[2]).toBe(v[0]);break;
      case 'table-cell-width': expect(r*v[1]).toBe(v[0]);break;
      case 'first-line-position': expect(r-v[0]-v[1]).toBe(v[2]);break;
      case 'text-page-count': assert(allocationCount(v[0],v[1]));break;
      case 'simplex-copies': expect(r/v[1]).toBe(v[0]);break;
      case 'duplex-copies': {
        let sheets=0;
        for(let copy=0;copy<v[1];copy++) for(let page=0;page<v[0];page+=2) sheets++;
        assert(sheets);break;
      }
      case 'font-print-scale': expect(r/v[0]*100).toBeCloseTo(v[1],8);break;
      case 'raster-print-width': expect(r*v[1]).toBeCloseTo(v[0],8);break;
      case 'files-total': expect(r/v[1]).toBe(v[0]);break;
      case 'kib-to-bytes': expect(r/2**10).toBe(v[0]);break;
      case 'cluster-count': assert(allocationCount(v[0],v[1]));break;
      case 'cluster-slack': {
        let filled=v[0]%v[1]; assert(filled===0?0:v[1]-filled);
        expect(r).toBeGreaterThanOrEqual(0);expect(r).toBeLessThan(v[1]);break;
      }
      case 'volume-free': expect(r+v[1]).toBe(v[0]);break;
      case 'full-incremental': {
        let total=v[0];for(let day=0;day<v[2];day++)total+=v[1];assert(total);break;
      }
      case 'copy-time': expect(r*v[1]).toBe(v[0]);break;
      case 'compressed-size': expect(r/v[0]*100).toBeCloseTo(v[1],8);break;
      case 'memory-pages': assert(allocationCount(v[0],v[1]));break;
      case 'scheduled-elapsed': {
        const match=q.question.match(/(\d{2}):(\d{2}).*?(\d{2}):(\d{2})/)!;
        expect(match).not.toBeNull();
        const start=Number(match[1])*60+Number(match[2]),end=Number(match[3])*60+Number(match[4]);
        expect([start,end]).toEqual(v);assert(end-start);break;
      }
      case 'binary-value': {
        const digits=q.question.match(/2진수 ([01]+)/)![1];
        const value=parseInt(digits,2);expect(value).toBe(v[0]);assert(value);break;
      }
      case 'hex-value': {
        const digits=q.question.match(/16진수 ([0-9A-F]+)/)![1];
        const value=parseInt(digits,16);expect(value).toBe(v[0]);assert(value);break;
      }
      case 'bit-patterns': {
        let count=1;for(let bit=0;bit<v[0];bit++) count+=count;assert(count);break;
      }
      case 'network-time': expect(r*v[1]/8).toBeCloseTo(v[0],6);break;
      case 'rgb-bytes': expect(r/(v[0]*v[1])).toBe(v[2]/8);break;
      case 'pcm-bytes': expect(r/(v[0]*v[1]*v[3])).toBe(v[2]/8);break;
      case 'scan-pixels': expect(r/(v[0]*v[1])).toBe(v[2]**2);break;
      case 'utf8-bytes': {
        const visible='A'.repeat(v[0])+'가'.repeat(v[1]);
        assert(new TextEncoder().encode(visible).byteLength);break;
      }
      case 'byte-not': {
        const bits=q.question.match(/8비트 값 ([01]{8})/)![1];
        expect(parseInt(bits,2)).toBe(v[0]);expect(v[1]).toBe(8);
        assert((~parseInt(bits,2))&0xff);break;
      }
      default: throw new Error(`미검증 계산 유형: ${c.kind}`);
    }
    expect(Number.isFinite(r)).toBe(true);
    const choices=q.choices.map(choice=>{
      expect(choice.endsWith(c.unit)).toBe(true);
      expect(choice).toMatch(/^\d+(?:\.\d+)? /);
      return Number.parseFloat(choice);
    });
    expect(new Set(choices).size).toBe(4);
    expect(choices[q.answer-1]).toBeCloseTo(r,8);
    expect(choices.filter(n=>Math.abs(n-r)<1e-8)).toHaveLength(1);
    expect(q.explanation).toContain(String(r));
    expect(r*10**(c.precision||0)).toBeCloseTo(Math.round(r*10**(c.precision||0)),8);
    expect(q.reviewNote).toContain('계산 조건 변형');
  });
});
