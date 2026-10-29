# 실제 검증 및 배포 기록

검증일: 2026-10-30 (Asia/Seoul). 작업 경로 `/workspace/Word-Processor-CBT`.

## 시작 상태와 적용

README 1개만 있는 초기 커밋 `eb0397b0da0e1a2bcf158794360ff0979c98f6de`, 브랜치 work, tracked/untracked 변경 없음, 기존 AGENTS.md 없음. README의 원래 `워드프레스` 표현을 대상 자격증 `워드프로세서`로 정정했다. 기존 사용자 작업을 덮어쓰지 않았다.

표준 저장소 최신 main을 읽기용 `/tmp/cbt-standard-latest`에 clone했다. 최신 표준 커밋 `76b990b8720adfa85c22a0a8f699b17094aa357b`, v1.4.0. SKILL.md와 references 전부를 읽었다. 지정 앱 기준 커밋 `b9a682ccff1b460334b78d5bfad9375b7ec4fbb6`의 실제 코드와 package/lockfile·설정·테스트·workflow를 재사용했다. 해당 앱 경로들은 확보한 main과 diff가 없었다. 표준 폴더 9개 파일의 경로와 바이트 일치를 검사했다. 원본 저장소에는 변경·push·배포를 하지 않았다.

## 최종 로컬 결과

| 검사 | 명령/방식 | 결과 |
| --- | --- | --- |
| 의존성 | npm ci --no-audit --no-fund | exit 0, 110 패키지 설치, lockfile 변경 없음(프로젝트 이름 변경 제외) |
| 단위 검사 | npm test (`npm run check`에서 실행) | exit 0, 142개 통과 |
| 타입/프로덕션 빌드 | npm run build | exit 0, TypeScript + Vite 성공 |
| 최종 PC/모바일 | PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e | exit 0, 빌드 성공, 28개 통과·6개 제외·실패0, 42.1초 |
| 표준 복사 | 9개 파일 전체 bytes 비교 | 동일 |
| 변경 형식 | git diff --check | exit 0 |
| 문항 수 | 생성기 및 단위 검사 | 120개, 과목별40, 부족880 |

브라우저 검사는 Chromium의 Desktop Chrome/Pixel 7 **에뮬레이션**이다. 실제 PC/휴대전화 장치, Safari/Firefox, 블로그 iframe은 미실행이다. 테스트 결과 스크린샷으로 PC 대시보드와 가로 모바일 메뉴의 배치도 육안 확인했다. 다운로드·업로드·버튼·키보드·터치 자동 입력을 사용했다.

확인 범위: 두 모드, 실제 keydown/keyup Space, 미응답·수정키·반복키·버튼/컨트롤/대화상자 보호, 마지막 문제 자동 제출 방지, 60문항 선택·정답 비공개·답안 변경·북마크·새로고침·종료 시각 보존, 제출 확인·취소, 만료 자동 제출·만료 뒤 답안 차단·중복 제출 방지, 합격 결과 및 높은 평균에서도 과락 불합격, 전체 해설과 시험 오답 복습, 랜덤 즉시 채점·중복 기록 방지·오답 해제·통계, JSON/CSV 가져오기·중복·검증 대기·근거 승인·오류 행 원자성·초기화, 저장 실패 경고 및 손상 원본 보존, 가로 넘침·학습 기준 메뉴·criteria-note 부재.

모바일 전용 6검사는 PC 프로젝트에서만 제외됐다(미실행을 통과로 집계하지 않음). 모바일에서는 **390×480, 740×360, 390×480 글자확대** 각각 실제 휠 및 CDP touchStart/move/end를 별도로 실행했다. 메뉴 아래로 이동→백업 실제 다운로드→초기화 확인창 열기/취소→위로 이동→대시보드 실제 선택을 검증했다. scrollTop 대입은 하지 않았고, 위치 읽기와 배경 스크롤 불변을 확인했다.

개발 중 처음에는 샌드박스의 Python 하위 프로세스 실행 제한으로 단위 재생성 검사가 EPERM을 냈다. 승인된 실행 컨텍스트에서 142개 모두 통과했다. TypeScript 테스트 변수의 추론 타입을 Store로 명시해 빌드 오류를 수정했다. Playwright 다운로드 브라우저가 설치되지 않아 기본 경로로 한 번 실행한 검사는 브라우저 시작 전에 실패했으며, 기존 `/usr/bin/chromium`을 명시한 최종 실행이 위 결과다. 이는 로컬 개발 검사 수정이며 배포 파이프라인 재실행이 아니다.

## 별도 미충족 조건

- 기본 은행 1,000문항: 120/1,000, 부족880. 수량 기준 미충족.
- 공식 시험 규칙·현행 과목명·지정 OS·공식 출제기준 대조: 공식 사이트 요청 프록시403으로 차단, 미완료.
- 기출 재배포 권한이 확인된 자료: 확보0. 원문 기출0·복원0·자체 제작120·숫자 조건 변형0.
- 전문가/외부 독립 내용 검수: 미완료. 내부 검토와 자동 구조 검사만으로 이를 대신하지 않는다.

## 배포 사전 확인: 첫 차단으로 중단

1. 원격 main 읽기 `git ls-remote origin refs/heads/main`: exit0, 초기 커밋과 동일.
2. 기존 주입 인증의 GH_TOKEN 존재만 확인(값 출력 없음).
3. 단 한 번의 권한 확인 명령 `gh api repos/YunSangYeong/Word-Processor-CBT --jq '{full_name,default_branch,permissions}'`: **exit1**.

실제 오류:

```text
Get "https://api.github.com/repos/YunSangYeong/Word-Processor-CBT": Forbidden
```

이 오류 이후 배포 확인을 즉시 중단했다. 다른 API 경로·추가 권한 조회·Pages 조회·main push·workflow_dispatch·workflow 재실행·대체 배포를 하지 않았다. 현재 Pages Source, CI 실행 상태, 기존 게시 여부 및 공개 화면은 **미확인**이다. 이번 작업의 배포 파이프라인은 시작하지 않았다.

기본 흐름 main push→validate→deploy 및 PR 검증만 수행하는 workflow는 구현물에 포함했다. 차단 뒤에는 자동 배포를 일으키지 않는 `codex/word-processor-cbt` 브랜치로 코드 보존만 수행한다. 이 브랜치는 main push 트리거에 해당하지 않고 PR도 자동 생성하지 않는다. 원격 보존의 실제 성공 여부와 커밋은 작업 최종 보고에서 별도로 확인한다.

예상 URL: https://YunSangYeong.github.io/Word-Processor-CBT/ . **배포 성공 주소로 확인한 것이 아니다.**

사용자가 지금 확인할 최소 단계: 환경 설정의 네트워크 허용 목록에 `api.github.com`을 추가/허용한다. 현재 정책 스냅샷에는 이 호스트가 없다. 이 조치만으로 인증·권한·Pages 최초 설정이 모두 해결된다는 뜻은 아니다. 에이전트는 이를 추정해 재시도하지 않으며 이후 배포 마무리는 사용자가 진행한다. 공식 자료 대조에는 `license.korcham.net` 접근도 별도로 필요하다.
