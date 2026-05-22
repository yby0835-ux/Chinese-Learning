# 카카오톡 자동 중국어 학습 알림 프로젝트

## 프로젝트 목적
매일 오전 7:00 (KST) HSK 1급 기반 중국어 학습 콘텐츠를
카카오톡 '나와의 채팅'으로 자동 수신하는 시스템.

30일 커리큘럼으로 구성되며, 30일 후 처음부터 반복.

---

## 전체 동작 흐름

```
[GitHub Actions 스케줄러]
    ↓ 매일 KST 07:00 (UTC 22:00) 자동 트리거
[main.py]
    ↓ 오늘 날짜 기준으로 커리큘럼 인덱스 계산
    ↓ 단어 3개 + 예문 + 문법 포인트 포맷 생성
[kakao.py]
    ↓ refresh_token → access_token 갱신
    ↓ 새 refresh_token 수신 시 GH_PAT로 GitHub Secret 자동 업데이트
    ↓ access_token으로 '나에게 메시지 보내기' API 호출
[카카오톡 수신]
```

---

## 파일 구조

```
E:\Claude\Chinese-Learning\
├── .github/
│   └── workflows/
│       └── chinese.yml   ← 스케줄 및 실행 설정
├── curriculum.py          ← 30일치 HSK 1급 커리큘럼 데이터
├── kakao.py               ← access_token 갱신 + refresh_token 자동 갱신 + 메시지 전송
├── main.py                ← 진입점: 날짜 기반 커리큘럼 선택 → 포맷 → 전송
├── requirements.txt       ← requests, PyNaCl
├── CLAUDE.md              ← 이 파일
└── PROJECT_DOC.md         ← 전체 프로젝트 문서
```

---

## 메시지 형태

```
🇨🇳  오늘의 중국어
📅  5월 23일 (금)  · Day 1 / 30

  주제  📌 인사

📝  단어

  你好    nǐ hǎo
          안녕하세요

  谢谢    xiè xiè
          감사합니다

  再见    zài jiàn
          안녕히 가세요

💬  오늘의 표현
  你好！谢谢你。再见！
  nǐ hǎo！xiè xiè nǐ。zài jiàn！
  안녕하세요! 감사합니다. 안녕히 가세요!

📖  오늘의 문법
  你好 = 你(너) + 好(좋다) → 상대를 향한 인사

  你好，我叫小明。
  nǐ hǎo，wǒ jiào xiǎo míng。
  안녕하세요, 저는 샤오밍이에요.
```

---

## 커리큘럼 구성 (30일)

| Day | 주제 | Day | 주제 |
|---|---|---|---|
| 1 | 인사 | 16 | 집과 직장 |
| 2 | 기본 표현 | 17 | 교통 |
| 3 | 나·너·그 | 18 | 쇼핑 |
| 4 | 우리·이것·저것 | 19 | 색깔 |
| 5 | 숫자 1~5 | 20 | 크기와 양 |
| 6 | 숫자 6~10 | 21 | 있다·없다·이다 |
| 7 | 날짜 | 22 | 이동 동사 |
| 8 | 지금 몇 시? | 23 | 먹고 마시고 자다 |
| 9 | 요일 | 24 | 좋다·빠르다·느리다 |
| 10 | 가족 1 | 25 | 날씨 |
| 11 | 가족 2 | 26 | 몸과 건강 |
| 12 | 음식 | 27 | 위치와 방향 |
| 13 | 과일 | 28 | 감정 표현 |
| 14 | 음료 | 29 | 할 수 있다·원하다 |
| 15 | 장소 | 30 | 종합 복습 |

---

## 연동 방식

### 카카오톡 전송
- 방식: 카카오 OAuth 2.0 (Weather 프로젝트와 동일 계정)
- 엔드포인트: `POST https://kapi.kakao.com/v2/api/talk/memo/default/send`
- 앱: Weather2 (앱 ID: 1464201)

### refresh_token 자동 갱신
- 만료 30일 전부터 새 token → GH_PAT로 GitHub Secret 자동 업데이트
- **사람이 직접 갱신할 필요 없음**

### GitHub Actions
- 스케줄: `cron: '0 22 * * *'` (UTC) = 매일 KST 07:00
- 수동 실행: workflow_dispatch 지원

---

## GitHub Secrets

| Secret | 설명 | 갱신 |
|---|---|---|
| `KAKAO_REST_API_KEY` | 카카오 앱 REST API 키 | 영구 |
| `KAKAO_CLIENT_SECRET` | 카카오 클라이언트 시크릿 | 영구 |
| `KAKAO_REFRESH_TOKEN` | 카카오 OAuth refresh token | **자동 갱신** |
| `GH_PAT` | GitHub PAT (Secrets 쓰기 권한) | 만료일 확인 |

---

## 운영 가이드

### 발송 시각 변경
`.github/workflows/chinese.yml`의 cron 수정 (KST = UTC + 9)

| 원하는 시각 | cron 값 |
|---|---|
| 오전 7시 | `0 22 * * *` |
| 오전 8시 | `0 23 * * *` |

### 커리큘럼 추가
`curriculum.py`에 항목 추가. `len(CURRICULUM)`이 자동으로 반영됨.

### refresh_token 최초 발급
```
1. 브라우저에서 인가 코드 획득:
   https://kauth.kakao.com/oauth/authorize?client_id=d40c837591e55451fddf671490367d0d&redirect_uri=https://example.com&response_type=code&scope=talk_message

2. python E:\Claude\Weather\get_token.py 실행

3. 출력된 refresh_token → GitHub Secrets KAKAO_REFRESH_TOKEN 등록
```

### 수동 실행
```
https://github.com/yby0835-ux/Chinese-Learning/actions/workflows/chinese.yml
→ Run workflow
```
