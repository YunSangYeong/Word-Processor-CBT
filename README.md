# 워드프로세서 필기 CBT

React + TypeScript + Vite 기반 비공식 학습 앱. 전기기능사 표준 앱을 실제로 재사용하되 대상 데이터와 저장 공간을 분리했다. 로그인·서버·유료 API는 없다.

## 기능

실전 모의시험, 랜덤 문제풀이, 오답노트, 북마크, 학습 통계, JSON/CSV 문제은행 가져오기·중복 검사·로컬 검수·내보내기. 실전은 답안 변경, 번호 이동, 절대 종료 시각과 자동 제출, 새로고침 복원, 제출 후 전체 해설 및 오답 복습을 지원한다. 두 모드에서 답안 선택/채점 뒤 Space로 다음 문제, 마지막 실전 문제에서는 자동 제출하지 않는다. 학습 기준/연도 선택 메뉴는 없다.

모바일 메뉴는 독립 세로 스크롤과 100dvh/100vh fallback을 사용한다. 작은 세로·가로 화면·글자 확대를 실제 휠/터치 입력으로 검사한다.

## 실행

Node 24.19.0 (`.node-version`, engines >=22.12.0), npm과 Python 3(문항 재생성 검사).

```sh
cd /workspace/Word-Processor-CBT
npm ci
npm run dev
npm test
npm run build
npx playwright install --with-deps chromium
npm run test:e2e
```

이미 설치된 Chromium을 쓸 때는 `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e`. Pages 경로는 `/Word-Processor-CBT/`. 테스트는 배포한 화면이 아니라 로컬 production preview를 검증한다.

## 문항과 시험 규칙의 한계

현재 내부 검토 기본 문항 **1,000개**, 부족 **0개**. 기존120개를 보존하고 880개를 추가했다. 과목별340·340·320개. 원문 기출0·복원0·자체 제작1,000개이며, 개념·사례형420개와 계산 조건 변형580개(29유형×20조건)로 구분한다. 1,000개 독립 개념이나 기출이라는 뜻은 아니다. 검증 대기·개인 로컬 등록분은 제외한다.

AI 일반 지식 기반 자체 작성 및 내부 내용 검토, 구조·중복·재생성 자동 검사. 외부 전문가 검수와 공식 출제기준 대조는 미완료다. 연도·회차는 모두 null. 출처 링크는 작성 위치이며 외부 정답 증빙이 아니다. [문항 출처·권리·검수](docs/QUESTION_BANK.md).

공식 안내 접근은 프록시 403으로 차단됐다. 현재 과목별 20문항·총60문항·60분·평균60점 및 과목별40점은 학습용 가정으로 설정하며 공식 검증 완료로 표시하지 않는다. 현행 과목명·지정 OS·규칙 확인은 남아 있다. [시험 규칙 확인 상태](docs/EXAM_RULES.md).

## 저장

`word-processor-cbt:v1` namespace로 같은 origin의 다른 CBT와 분리한다. 응답 최근5,000개·시험 최근30회, 통계는 보존된 기록 기준. 시험·연습·북마크·오답·로컬 문항은 이 브라우저 localStorage에 저장한다. 손상 원본은 자동 덮어쓰지 않으며 저장 실패는 경고한다. JSON 백업 내보내기는 지원하고 백업 복원 UI는 제공하지 않는다. 초기화는 확인 뒤 사용자 데이터만 삭제한다. 다른 브라우저/origin/시크릿 모드/iframe 저장 제한에 따라 기록이 분리되거나 저장 불가할 수 있다. 기기 시계를 조작하는 환경의 엄격한 시험 감독은 지원하지 않는다.

## 표준과 라이선스

최신 표준 v1.4.0은 원본 main `76b990b8720adfa85c22a0a8f699b17094aa357b`에서 폴더 전체를 복사했다. 앱 코드 출발점은 스킬에 지정된 `b9a682ccff1b460334b78d5bfad9375b7ec4fbb6`; 해당 커밋과 확보한 main 간 앱·설정·테스트 diff가 없음을 확인했다. AGENTS.md가 없어서 표준 연결 문서를 새로 추가했다. 원본 프로젝트를 수정하거나 재배포하지 않았다. 원본 코드 MIT 고지 보존, 새 문항 CC BY 4.0. 원고와 생성 자료 모두 동일 조건을 적용한다.

## GitHub Pages

사용자가 자동 배포까지 요청했다. `.github/workflows/pages.yml`은 main push → 단위검사·빌드·PC/모바일 검증 → Pages 배포, PR은 검증만 수행한다. deploy는 validate 성공 후 main에서만 실행하며 pages/id-token 쓰기 권한은 deploy job에 한정한다.

배포 전 필수 권한·인증·네트워크 확인부터 최초 실패나 관리자 설정·승인 필요 시 중단한다. 자동 재시도, workflow 재실행, 다른 배포 경로, 추가 배포 유발 푸시는 하지 않는다. [실제 검증·반영·배포 기록](docs/VERIFICATION.md).

예상 기본 주소: https://YunSangYeong.github.io/Word-Processor-CBT/ (현재 게시 성공을 뜻하지 않음).
