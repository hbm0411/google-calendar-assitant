#!/bin/bash

# 스타벅스 캘린더 어시스턴트 종료 스크립트
# 사용법: stop_calendar

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🔄 스타벅스 캘린더 어시스턴트 서버를 종료합니다...${NC}"

# 서버 프로세스 찾기 및 종료
PIDS=$(pgrep -f "python run_server.py")

if [ -z "$PIDS" ]; then
    echo -e "${BLUE}ℹ️  실행 중인 서버가 없습니다.${NC}"
else
    echo -e "${YELLOW}📋 종료할 프로세스: $PIDS${NC}"
    
    # 각 프로세스 종료
    for PID in $PIDS; do
        echo -e "${YELLOW}🔄 프로세스 $PID 종료 중...${NC}"
        kill $PID 2>/dev/null || true
    done
    
    # 강제 종료 (필요시)
    sleep 2
    PIDS_REMAINING=$(pgrep -f "python run_server.py")
    if [ ! -z "$PIDS_REMAINING" ]; then
        echo -e "${RED}⚠️  강제 종료를 시도합니다...${NC}"
        for PID in $PIDS_REMAINING; do
            kill -9 $PID 2>/dev/null || true
        done
    fi
    
    echo -e "${GREEN}✅ 서버가 종료되었습니다.${NC}"
fi

# 포트 8000 사용 확인
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${YELLOW}⚠️  포트 8000이 여전히 사용 중입니다.${NC}"
else
    echo -e "${GREEN}✅ 포트 8000이 해제되었습니다.${NC}"
fi 