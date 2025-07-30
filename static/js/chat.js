// DOM 요소들
const chatMessages = document.getElementById('chatMessages');
const messageForm = document.getElementById('messageForm');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const loadingIndicator = document.getElementById('loadingIndicator');
const imageButton = document.getElementById('imageButton');
const imageInput = document.getElementById('imageInput');
const imagePreview = document.getElementById('imagePreview');
const previewImage = document.getElementById('previewImage');
const removeImage = document.getElementById('removeImage');

// 전역 변수로 선택된 이미지 파일 추적
let selectedImageFile = null;

// 현재 시간을 포맷팅하는 함수
function formatTime() {
    const now = new Date();
    return now.toLocaleTimeString('ko-KR', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

// Markdown을 HTML로 변환하는 함수
function parseMarkdown(text) {
    if (!text) return '';
    
    // marked 옵션 설정
    marked.setOptions({
        breaks: true,
        gfm: true,
        sanitize: false
    });
    
    try {
        return marked.parse(text);
    } catch (error) {
        console.error('Markdown 파싱 오류:', error);
        return text; // 파싱 실패시 원본 텍스트 반환
    }
}

// 메시지를 채팅창에 추가하는 함수
function addMessage(content, isUser = false, isError = false, toolInfo = null, responseId = null, previousResponseId = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
    if (isError) messageDiv.classList.add('error');
    
    const avatarIcon = isUser ? 'fas fa-user' : 'fas fa-robot';
    
    // ID 정보 표시
    let previousIdInfo = '';
    let currentIdInfo = '';
    
    let toolSection = '';
    if (toolInfo) {
        if (previousResponseId) {
            previousIdInfo += `<div class="id-info previous-id">이전 ID: ${previousResponseId}</div>`;
        }
        if (responseId) {
            currentIdInfo += `<div class="id-info current-id">현재 ID: ${responseId}</div>`;
        }
        toolSection = `
            <div class="tool-info">
                <div class="tool-header" onclick="toggleToolInfo(this)">
                    <i class="fas fa-chevron-right"></i>
                    <span class="tool-name">${toolInfo.name}</span>
                    <span class="tool-toggle">클릭하여 상세보기</span>
                </div>
                <div class="tool-content">
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
            </div>
        `;
    }
    
    // Assistant 메시지인 경우 Markdown 파싱
    const processedContent = isUser ? content : parseMarkdown(content);
    const messageTextClass = isUser ? 'message-text' : 'message-text markdown-content';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            ${isUser ? 
                '<i class="fas fa-user"></i>' : 
                '<img src="/static/images/logo.png" alt="AI 비서" onerror="this.style.display=\'none\'; this.nextElementSibling.style.display=\'block\';">' +
                '<i class="fas fa-robot" style="display: none;"></i>'
            }
        </div>
        <div class="message-content">
            ${previousIdInfo}
            <div class="${messageTextClass}">${processedContent}</div>
            ${toolSection}
            ${currentIdInfo}
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

// Tool 정보 토글 함수
function toggleToolInfo(headerElement) {
    const toolInfo = headerElement.parentElement;
    const toolContent = toolInfo.querySelector('.tool-content');
    const toggleText = headerElement.querySelector('.tool-toggle');
    
    if (toolContent.classList.contains('expanded')) {
        // 접기
        toolContent.classList.remove('expanded');
        headerElement.classList.remove('expanded');
        toggleText.textContent = '클릭하여 상세보기';
    } else {
        // 펼치기
        toolContent.classList.add('expanded');
        headerElement.classList.add('expanded');
        toggleText.textContent = '클릭하여 접기';
    }
}

// 로딩 상태를 토글하는 함수
function toggleLoading(show) {
    loadingIndicator.style.display = show ? 'block' : 'none';
    sendButton.disabled = show;
    messageInput.disabled = show;
}

// 전역 변수로 response_id 추적
let currentResponseId = null;

// 이미지 선택 이벤트 핸들러
imageButton.addEventListener('click', () => {
    imageInput.click();
});

// 이미지 파일 선택 시 처리
imageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    console.log('이미지 파일 선택:', file);
    if (file) {
        if (file.type.startsWith('image/')) {
            selectedImageFile = file;
            console.log('이미지 파일 설정됨:', file.name, file.type, file.size);
            showImagePreview(file);
        } else {
            alert('이미지 파일만 선택할 수 있습니다.');
        }
    }
});

// 이미지 미리보기 표시
function showImagePreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        imagePreview.style.display = 'flex';
    };
    reader.readAsDataURL(file);
}

// 이미지 제거
removeImage.addEventListener('click', () => {
    selectedImageFile = null;
    imagePreview.style.display = 'none';
    imageInput.value = '';
    previewImage.src = '';
});

// 이미지 붙여넣기 이벤트 핸들러
document.addEventListener('paste', (e) => {
    const items = e.clipboardData.items;
    
    for (let item of items) {
        if (item.type.startsWith('image/')) {
            e.preventDefault();
            const file = item.getAsFile();
            if (file) {
                selectedImageFile = file;
                showImagePreview(file);
            }
            break;
        }
    }
});

// 입력창에서 이미지 붙여넣기 처리
messageInput.addEventListener('paste', (e) => {
    console.log('붙여넣기 이벤트 발생');
    const items = e.clipboardData.items;
    console.log('클립보드 아이템들:', items);
    
    for (let item of items) {
        console.log('클립보드 아이템:', item.type);
        if (item.type.startsWith('image/')) {
            e.preventDefault();
            const file = item.getAsFile();
            console.log('이미지 파일 추출:', file);
            if (file) {
                selectedImageFile = file;
                console.log('이미지 파일 설정됨 (붙여넣기):', file.name, file.type, file.size);
                showImagePreview(file);
                // 이미지가 붙여넣어졌음을 사용자에게 알림
                addMessage('✅ 이미지가 붙여넣어졌습니다! 이제 메시지를 입력하고 전송하세요.', false);
            }
            break;
        }
    }
});

// 드래그 앤 드롭 이벤트 핸들러
messageInput.addEventListener('dragover', (e) => {
    e.preventDefault();
    messageInput.classList.add('dragover');
});

messageInput.addEventListener('dragleave', (e) => {
    e.preventDefault();
    messageInput.classList.remove('dragover');
});

messageInput.addEventListener('drop', (e) => {
    e.preventDefault();
    messageInput.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    console.log('드롭된 파일들:', files);
    if (files.length > 0) {
        const file = files[0];
        console.log('드롭된 파일:', file.name, file.type, file.size);
        if (file.type.startsWith('image/')) {
            selectedImageFile = file;
            console.log('이미지 파일 설정됨 (드롭):', file.name, file.type, file.size);
            showImagePreview(file);
            addMessage('✅ 이미지가 드롭되었습니다! 이제 메시지를 입력하고 전송하세요.', false);
        } else {
            addMessage('❌ 이미지 파일만 업로드할 수 있습니다.', false, true);
        }
    }
});

// API 요청을 보내는 함수
async function sendMessage(message) {
    try {
        console.log('=== sendMessage 시작 ===');
        console.log('메시지:', message);
        console.log('selectedImageFile:', selectedImageFile);
        
        const formData = new FormData();
        formData.append('message', message);
        formData.append('user_id', 'test_user');
        
        // 이미지가 있으면 추가
        if (selectedImageFile) {
            console.log('이미지 파일 추가:', selectedImageFile.name, selectedImageFile.type, selectedImageFile.size);
            formData.append('image', selectedImageFile);
        } else {
            console.log('이미지 파일이 없습니다.');
        }
        
        // 이전 response_id가 있으면 추가
        if (currentResponseId) {
            formData.append('previous_response_id', currentResponseId);
        }
        
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
            let newResponseId = null;
            
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
                
                // response_id 찾기
                if (data.response.id) {
                    newResponseId = data.response.id;
                    currentResponseId = newResponseId;
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
            
            // Tool 정보가 있으면 별도 메시지로 표시
            if (toolInfo) {
                addMessage(`Tool 실행: ${toolInfo.name}`, false, false, toolInfo, newResponseId, currentResponseId);
            }
            
            // LLM 응답을 별도 메시지로 표시
            addMessage(responseText, false, false, null, newResponseId, currentResponseId);
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
        
        // 메시지 전송 후 이미지 초기화
        if (selectedImageFile) {
            selectedImageFile = null;
            imagePreview.style.display = 'none';
            imageInput.value = '';
            previewImage.src = '';
        }
        
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