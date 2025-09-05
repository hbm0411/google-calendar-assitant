#!/bin/bash

# 스타벅스 캘린더 어시스턴트 시작 스크립트
# 사용법: start_calendar

# 색상 정의
RED='\033[0;31m'      # 빨간색
GREEN='\033[0;32m'    # 초록색
YELLOW='\033[1;33m'   # 노란색 (굵게)
BLUE='\033[0;34m'     # 파란색
NC='\033[0m'          # 색상 리셋 (No Color)

# 프로젝트 디렉토리 (절대 경로로 수정하세요)
PROJECT_DIR="$HOME/Projects/Test/google-calendar-assitant"

echo -e "${BLUE}🚀 스타벅스 캘린더 어시스턴트를 시작합니다...${NC}"

# 프로젝트 디렉토리로 이동
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ 프로젝트 디렉토리를 찾을 수 없습니다: $PROJECT_DIR${NC}"
    echo -e "${YELLOW}💡 PROJECT_DIR 변수를 올바른 경로로 수정해주세요.${NC}"
    exit 1
fi

cd "$PROJECT_DIR"
echo -e "${GREEN}✅ 프로젝트 디렉토리로 이동: $PROJECT_DIR${NC}"

# 기존 서버 프로세스 종료
echo -e "${YELLOW}🔄 기존 서버 프로세스를 종료합니다...${NC}"
pkill -f "python run_server.py" 2>/dev/null || true
sleep 2

# 가상환경 확인 및 생성
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 가상환경을 생성합니다...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ 가상환경 생성 완료${NC}"
else
    echo -e "${GREEN}✅ 기존 가상환경 발견${NC}"
fi

# 가상환경 활성화
echo -e "${YELLOW}🔧 가상환경을 활성화합니다...${NC}"
source venv/bin/activate

# 의존성 설치 확인 (더 정확한 방법)
echo -e "${YELLOW}🔍 의존성 상태를 확인하는 중...${NC}"

# requirements.txt의 모든 패키지가 설치되어 있는지 확인
MISSING_PACKAGES=""
while IFS= read -r package; do
    # 주석이나 빈 줄 건너뛰기
    if [[ ! "$package" =~ ^[[:space:]]*# ]] && [[ -n "$package" ]]; then
        # 패키지 이름 추출 (버전 정보 제거)
        package_name=$(echo "$package" | cut -d'=' -f1 | cut -d'[' -f1 | cut -d'<' -f1 | cut -d'>' -f1 | cut -d'!' -f1 | xargs)
        
        # 패키지가 설치되어 있는지 확인
        if ! pip show "$package_name" >/dev/null 2>&1; then
            MISSING_PACKAGES="$MISSING_PACKAGES $package_name"
        fi
    fi
done < requirements.txt

if [ -n "$MISSING_PACKAGES" ]; then
    echo -e "${YELLOW}📦 누락된 패키지를 설치합니다: $MISSING_PACKAGES${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}✅ 의존성 설치 완료${NC}"
else
    echo -e "${GREEN}✅ 모든 의존성이 이미 설치되어 있습니다${NC}"
fi

# 포트 사용 확인
PORT=8000
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${RED}❌ 포트 $PORT가 이미 사용 중입니다.${NC}"
    echo -e "${YELLOW}💡 다른 프로세스를 종료하거나 포트를 변경해주세요.${NC}"
    exit 1
fi

# 서버 시작
echo -e "${GREEN}🚀 서버를 시작합니다...${NC}"
echo -e "${BLUE}📱 웹 브라우저에서 http://localhost:8000 으로 접속하세요${NC}"
echo -e "${BLUE}🛑 서버를 종료하려면 Ctrl+C를 누르세요${NC}"
echo -e "${BLUE}"--------------------------------------------------"${NC}"

# 서버를 백그라운드에서 시작하고 PID 저장
python run_server.py &
SERVER_PID=$!

# 서버가 완전히 시작될 때까지 대기
echo -e "${YELLOW}⏳ 서버 시작을 기다리는 중...${NC}"

# 서버가 포트에서 응답할 때까지 대기 (최대 30초)
TIMEOUT=30
COUNTER=0
while [ $COUNTER -lt $TIMEOUT ]; do
    # 서버 프로세스가 살아있는지 확인
    if ! kill -0 $SERVER_PID 2>/dev/null; then
        echo -e "${RED}❌ 서버 프로세스가 종료되었습니다.${NC}"
        exit 1
    fi
    
    # 포트에서 응답 확인
    if curl -s http://localhost:8000/health/ >/dev/null 2>&1; then
        echo -e "${GREEN}✅ 서버가 성공적으로 시작되었습니다!${NC}"
        break
    fi
    
    echo -n "."
    sleep 1
    COUNTER=$((COUNTER + 1))
done

if [ $COUNTER -eq $TIMEOUT ]; then
    echo -e "${RED}❌ 서버 시작 시간 초과 (30초)${NC}"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

echo ""

# 크롬에서 자동으로 페이지 열기
echo -e "${BLUE}🌐 크롬에서 페이지를 여는 중...${NC}"

# macOS에서 크롬 실행 (여러 방법 시도)
if command -v open >/dev/null 2>&1; then
    # macOS의 경우 open 명령어 사용
    open -a "Google Chrome" http://localhost:8000 >/dev/null 2>&1 &
    BROWSER_OPENED=true
elif command -v google-chrome >/dev/null 2>&1; then
    google-chrome http://localhost:8000 >/dev/null 2>&1 &
    BROWSER_OPENED=true
elif command -v google-chrome-stable >/dev/null 2>&1; then
    google-chrome-stable http://localhost:8000 >/dev/null 2>&1 &
    BROWSER_OPENED=true
elif command -v chromium-browser >/dev/null 2>&1; then
    chromium-browser http://localhost:8000 >/dev/null 2>&1 &
    BROWSER_OPENED=true
else
    BROWSER_OPENED=false
fi

if [ "$BROWSER_OPENED" = true ]; then
    echo -e "${GREEN}🎉 브라우저가 열렸습니다!${NC}"
else
    echo -e "${YELLOW}⚠️  크롬을 찾을 수 없습니다. 수동으로 브라우저를 열어주세요.${NC}"
    echo -e "${BLUE}💡 브라우저에서 http://localhost:8000 에 접속하세요${NC}"
fi

echo -e "${BLUE}🛑 서버를 종료하려면 Ctrl+C를 누르세요${NC}"
echo -e "${BLUE}"--------------------------------------------------"${NC}"

# 서버 프로세스가 종료될 때까지 대기
wait $SERVER_PID 