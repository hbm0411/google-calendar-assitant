// DOM 요소들
const chatMessages = document.getElementById('chatMessages');
const messageForm = document.getElementById('messageForm');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const loadingIndicator = document.getElementById('loadingIndicator');

// 현재 시간을 포맷팅하는 함수
function formatTime() {
    const now = new Date();
    return now.toLocaleTimeString('ko-KR', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

// 메시지를 채팅창에 추가하는 함수
function addMessage(content, isUser = false, isError = false, toolInfo = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
    if (isError) messageDiv.classList.add('error');
    
    const avatarIcon = isUser ? 'fas fa-user' : 'fas fa-robot';
    
    let toolSection = '';
    if (toolInfo) {
        toolSection = `
            <div class="tool-info">
                <div class="tool-header">
                    <i class="fas fa-tools"></i>
                    <span class="tool-name">${toolInfo.name}</span>
                </div>
                <div class="tool-details">
                    <div class="tool-arguments">
                        <strong>Arguments:</strong>
                        <pre>${JSON.stringify(JSON.parse(toolInfo.arguments), null, 2)}</pre>
                    </div>
                    <div class="tool-output">
                        <strong>Output:</strong>
                        <pre>${JSON.stringify(JSON.parse(toolInfo.output), null, 2)}</pre>
                    </div>
                </div>
            </div>
        `;
    }
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            ${isUser ? 
                '<i class="fas fa-user"></i>' : 
                '<img src="/static/images/logo.png" alt="AI 비서" onerror="this.style.display=\'none\'; this.nextElementSibling.style.display=\'block\';">' +
                '<i class="fas fa-robot" style="display: none;"></i>'
            }
        </div>
        <div class="message-content">
            <div class="message-text">${content}</div>
            ${toolSection}
            <div class="message-time">${formatTime()}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// 채팅창을 맨 아래로 스크롤하는 함수
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 로딩 상태를 토글하는 함수
function toggleLoading(show) {
    loadingIndicator.style.display = show ? 'block' : 'none';
    sendButton.disabled = show;
    messageInput.disabled = show;
}

// API 요청을 보내는 함수
async function sendMessage(message) {
    try {
        const formData = new FormData();
        formData.append('message', message);
        formData.append('user_id', 'test_user');
        
        const response = await fetch('/send_message', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            // AI 응답 처리
            let responseText = '응답을 받았습니다.';
            let toolInfo = null;
            
            if (data.response && data.response.output) {
                const outputs = data.response.output;
                
                // Tool 호출 정보 찾기
                const toolCall = outputs.find(output => output.type === 'mcp_call');
                if (toolCall) {
                    toolInfo = {
                        name: toolCall.name,
                        arguments: toolCall.arguments,
                        output: toolCall.output
                    };
                }
                
                // LLM 응답 텍스트 찾기
                const messageOutput = outputs.find(output => output.type === 'message');
                if (messageOutput && messageOutput.content) {
                    const textContent = messageOutput.content.find(content => content.type === 'output_text');
                    if (textContent && textContent.text) {
                        responseText = textContent.text;
                    }
                }
            } else if (data.response && data.response.choices && data.response.choices.length > 0) {
                const choice = data.response.choices[0];
                if (choice.message && choice.message.content) {
                    responseText = choice.message.content;
                } else if (choice.text) {
                    responseText = choice.text;
                }
            } else if (data.response && data.response.content) {
                responseText = data.response.content;
            } else if (typeof data.response === 'string') {
                responseText = data.response;
            }
            
            addMessage(responseText, false, false, toolInfo);
        } else {
            addMessage(`오류가 발생했습니다: ${data.error}`, false, true);
        }
    } catch (error) {
        console.error('Error:', error);
        addMessage(`서버 오류가 발생했습니다: ${error.message}`, false, true);
    }
}

// 폼 제출 이벤트 처리
messageForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message) return;
    
    // 사용자 메시지 추가
    addMessage(message, true);
    
    // 입력창 초기화
    messageInput.value = '';
    
    // 로딩 상태 시작
    toggleLoading(true);
    
    try {
        await sendMessage(message);
    } finally {
        // 로딩 상태 종료
        toggleLoading(false);
        messageInput.focus();
    }
});

// Enter 키 이벤트 처리 (Shift+Enter로 줄바꿈)
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        messageForm.dispatchEvent(new Event('submit'));
    }
});

// 입력창 자동 크기 조절
messageInput.addEventListener('input', () => {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
});

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', () => {
    // 환영 메시지 시간 설정
    const welcomeTime = document.getElementById('welcomeTime');
    if (welcomeTime) {
        welcomeTime.textContent = formatTime();
    }
    
    // 입력창에 포커스
    messageInput.focus();
    
    // 스크롤을 맨 아래로
    scrollToBottom();
});

// 네트워크 상태 모니터링
window.addEventListener('online', () => {
    addMessage('네트워크 연결이 복구되었습니다.', false);
});

window.addEventListener('offline', () => {
    addMessage('네트워크 연결이 끊어졌습니다. 연결을 확인해주세요.', false, true);
});

// 에러 처리
window.addEventListener('error', (e) => {
    console.error('Global error:', e.error);
});

// Promise rejection 처리
window.addEventListener('unhandledrejection', (e) => {
    console.error('Unhandled promise rejection:', e.reason);
    addMessage('예상치 못한 오류가 발생했습니다.', false, true);
}); 