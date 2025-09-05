# 🚀 배포 가이드

이 프로젝트를 무료로 서버에 배포하는 방법을 안내합니다.

## 📋 배포 전 준비사항

1. **OpenAI API 키 준비**
   - [OpenAI API](https://platform.openai.com/api-keys)에서 API 키 발급
   - 충분한 크레딧이 있는지 확인

2. **GitHub 계정**
   - 코드를 GitHub에 업로드

## 🎯 추천 배포 방법: Railway

### 1단계: Railway 계정 생성
1. [Railway](https://railway.app/) 접속
2. GitHub로 로그인

### 2단계: 프로젝트 배포
1. "New Project" 클릭
2. "Deploy from GitHub repo" 선택
3. GitHub 저장소 선택
4. "Deploy Now" 클릭

### 3단계: 환경 변수 설정
Railway 대시보드에서 다음 환경 변수 설정:

```
RESPONSES_API_KEY=your-actual-openai-api-key
RESPONSES_API_URL=https://api.openai.com/v1/responses
```

### 4단계: 도메인 확인
- Railway에서 제공하는 도메인 확인 (예: `https://your-app.railway.app`)
- 자동으로 HTTPS 적용됨

## 🔄 대안 배포 방법들

### Render
1. [Render](https://render.com/) 접속
2. "New Web Service" 선택
3. GitHub 저장소 연결
4. 환경 변수 설정
5. 배포

### Vercel
1. [Vercel](https://vercel.com/) 접속
2. "New Project" 선택
3. GitHub 저장소 연결
4. 환경 변수 설정
5. 배포

## ⚠️ 주의사항

1. **API 키 보안**
   - 절대 코드에 API 키를 하드코딩하지 마세요
   - 환경 변수로 관리하세요

2. **무료 티어 제한**
   - Railway: 월 $5 크레딧
   - Render: 월 750시간
   - Vercel: 월 100GB 대역폭

3. **성능 최적화**
   - 로그 파일은 로컬에만 저장
   - 정적 파일은 CDN 사용 고려

## 🛠️ 문제 해결

### 배포 실패 시
1. 로그 확인
2. 환경 변수 설정 확인
3. requirements.txt 버전 호환성 확인

### API 오류 시
1. OpenAI API 키 유효성 확인
2. 크레딧 잔액 확인
3. API 사용량 제한 확인

## 📞 지원

문제가 발생하면 GitHub Issues에 문의해주세요! 