<template>
  <div>
    <!-- Chatbot Container -->
    <div :class="['chatbot', { 'open': isOpen }]">
      <div v-if="!isOpen" class="chat-bubble" @click="toggleChat">
        <span>💬</span> <!-- Biểu tượng chatbot -->
      </div>
      <div v-else class="chat-content">
        <div class="chat-header">
          <h2>Chatbot</h2>
          <button class="close-button" @click="toggleChat">X</button>
        </div>
        <div class="messages">
          <div
            v-for="(message, index) in messages"
            :key="index"
            :class="[ 'message', message.sender === 'bot' ? 'bot' : 'user' ]"
          >
            <span>{{ message.text }}</span>
          </div>
        </div>

        <div v-if="isTyping" class="message bot typing-indicator">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
        </div>
        <div class="chat-input">
          <input
            type="text"
            v-model="userInput"
            @keyup.enter="sendMessage"
            placeholder="Nhập tin nhắn..."
          />
          <button @click="sendMessage">Gửi</button>
          <button @click="toggleRecording" :class="{ 'recording': isRecording }" class="voice-button">
            <span>🎤</span>
          </button>
        </div>
        <!-- Voice transcript preview -->
        <div v-if="(transcript || voiceStatus) && showTranscript" class="transcript-preview">
          <div v-if="voiceStatus" class="voice-status">{{ voiceStatus }}</div>
          <div v-if="transcript" class="transcript-text">{{ transcript }}</div>
          <div v-if="transcript" class="transcript-actions">
            <button @click="cancelVoiceMessage" class="cancel-voice">Hủy</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      isOpen: false,
      messages: [{ sender: 'bot', text: 'Chào bạn! Tôi có thể giúp gì cho bạn?' }],
      userInput: "",
      isTyping: false, // Thêm biến này
      // Biến cho voice recognition
      recognition: null,
      isRecording: false,
      transcript: '',
      isVoiceSupported: false,
      voiceStatus: '',
      retryTimeout: null,
      recognitionActive: false,
      showTranscript: true, // Biến mới để điều khiển hiển thị transcript
      
      // Biến cho auto-send
      autoSendTimeout: null,
      lastTranscriptChange: null,
      silenceDelay: 2000 // 2 giây
    };
  },
  mounted() {
    // Kiểm tra và khởi tạo Web Speech API
    this.initSpeechRecognition();
  },
  methods: {
    toggleChat() {
      this.isOpen = !this.isOpen;
    },
    
    async sendMessage() {
  if (this.userInput.trim() === "") return;

  const userMessage = this.userInput.trim();
  this.messages.push({ text: userMessage, sender: "user" });
  
  // Xóa nội dung input ngay sau khi gửi
  this.userInput = "";
  
  // Hiển thị typing indicator
  this.isTyping = true;

  try {
    const response = await axios.post("http://localhost:5000/chat", {
      message: userMessage,
    });

    // Tạo hiệu ứng trì hoãn trước khi hiển thị phản hồi
    setTimeout(() => {
      // Ẩn typing indicator
      this.isTyping = false;
      
      // Hiển thị phản hồi từ bot
      response.data.messages.forEach((msg) => {
        this.messages.push({ text: msg, sender: "bot" });
      });
    }, Math.random() * 1000 + 500); // Trì hoãn ngẫu nhiên từ 500ms đến 1500ms

  } catch (error) {
    console.error("Lỗi gửi tin nhắn:", error);
    
    // Ẩn typing indicator sau lỗi
    setTimeout(() => {
      this.isTyping = false;
      this.messages.push({ text: "Lỗi kết nối chatbot!", sender: "bot" });
    }, 500);
  }
},
    
    initSpeechRecognition() {
      this.isVoiceSupported = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
      
      if (this.isVoiceSupported) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        this.recognition.lang = 'vi-VN';
        this.recognition.interimResults = true;
        this.recognition.continuous = true;
        this.recognition.maxAlternatives = 1;
        
        this.recognition.onstart = () => {
          console.log('Recognition started');
          this.recognitionActive = true;
          this.voiceStatus = 'Đang nghe...';
          this.showTranscript = true; // Hiển thị transcript khi bắt đầu ghi âm
        };
        
        this.recognition.onresult = (event) => {
          let interimTranscript = '';
          let finalTranscript = '';
          
          for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
              finalTranscript += transcript;
            } else {
              interimTranscript += transcript;
            }
          }
          
          // Cập nhật transcript và hiển thị trong thời gian thực
          const newTranscript = finalTranscript || interimTranscript;
          if (newTranscript !== this.transcript) {
            this.transcript = newTranscript;
            this.lastTranscriptChange = Date.now();
            
            // Xóa timeout cũ và đặt timeout mới
            clearTimeout(this.autoSendTimeout);
            this.autoSendTimeout = setTimeout(() => {
              if (this.transcript.trim() && this.isRecording) {
                this.sendVoiceMessage();
              }
            }, this.silenceDelay);
          }
          
          this.voiceStatus = '';
        };
        
        this.recognition.onerror = (event) => {
          console.error('Lỗi nhận dạng giọng nói:', event.error);
          
          switch(event.error) {
            case 'no-speech':
              this.voiceStatus = 'Không nghe thấy tiếng nói, vui lòng thử lại...';
              break;
            case 'audio-capture':
              this.voiceStatus = 'Không tìm thấy thiết bị thu âm. Vui lòng kiểm tra microphone.';
              this.stopRecording();
              break;
            case 'not-allowed':
              this.voiceStatus = 'Không có quyền truy cập microphone. Vui lòng cấp quyền và thử lại.';
              this.stopRecording();
              break;
            case 'network':
              this.voiceStatus = 'Lỗi kết nối mạng. Vui lòng kiểm tra kết nối internet.';
              this.stopRecording();
              break;
            default:
              this.voiceStatus = 'Đã xảy ra lỗi. Vui lòng thử lại.';
              this.stopRecording();
          }
        };
        
        this.recognition.onend = () => {
          console.log('Recognition ended');
          this.recognitionActive = false;
          
          // Chỉ khởi động lại recognition nếu đang ghi âm và chưa có văn bản
          if (this.isRecording && !this.transcript) {
            this.voiceStatus = 'Không nghe rõ, đang thử lại...';
            setTimeout(() => {
              this.startRecognition();
            }, 100);
          }
        };
      }
    },
    
    startRecognition() {
      if (!this.recognitionActive) {
        try {
          console.log('Attempting to start recognition');
          this.recognition.start();
        } catch (e) {
          console.error('Lỗi khi bắt đầu ghi âm:', e);
          this.voiceStatus = 'Lỗi khởi động: ' + e.message;
          this.recognitionActive = false;
        }
      } else {
        console.log('Recognition already active, not starting again');
      }
    },
    
    toggleRecording() {
      if (!this.isVoiceSupported) {
        alert('Trình duyệt của bạn không hỗ trợ nhận dạng giọng nói');
        return;
      }
      
      if (this.isRecording) {
        this.stopRecording();
      } else {
        this.startRecording();
      }
    },
    
    startRecording() {
      // Reset các biến
      this.transcript = '';
      this.voiceStatus = 'Đang khởi động microphone...';
      this.isRecording = true;
      this.lastTranscriptChange = null;
      this.showTranscript = true; // Hiển thị transcript khi bắt đầu ghi âm
      clearTimeout(this.autoSendTimeout);
      
      // Yêu cầu quyền microphone
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then(() => {
          this.startRecognition();
        })
        .catch(err => {
          console.error('Lỗi quyền microphone:', err);
          this.voiceStatus = 'Không thể truy cập microphone. Vui lòng cấp quyền và thử lại.';
          this.isRecording = false;
        });
    },
    
    stopRecording() {
      clearTimeout(this.retryTimeout);
      clearTimeout(this.autoSendTimeout);
      this.isRecording = false;
      
      if (this.recognitionActive) {
        try {
          this.recognition.stop();
        } catch (e) {
          console.error('Lỗi khi dừng ghi âm:', e);
        }
      }
      
      if (!this.transcript) {
        this.voiceStatus = '';
        this.showTranscript = false; // Ẩn transcript khi không có nội dung
      }
    },
    
    sendVoiceMessage() {
      if (this.transcript.trim()) {
        this.userInput = this.transcript.trim();
        
        // Ẩn transcript trước khi gửi tin nhắn
        this.showTranscript = false;
        
        this.sendMessage();
        this.transcript = '';
        this.voiceStatus = '';
        
        // Tắt microphone sau khi gửi tin nhắn
        this.stopRecording();
      }
    },
    
    cancelVoiceMessage() {
      this.transcript = '';
      this.voiceStatus = '';
      this.showTranscript = false; // Ẩn transcript khi hủy
      clearTimeout(this.autoSendTimeout);
      this.stopRecording();
    }
  },
  beforeDestroy() {
    // Dọn dẹp
    clearTimeout(this.retryTimeout);
    clearTimeout(this.autoSendTimeout);
    if (this.recognition && this.recognitionActive) {
      try {
        this.recognition.stop();
      } catch (e) {
        console.error('Lỗi khi hủy recognition:', e);
      }
    }
  }
};
</script>

<style scoped>

/* Typing indicator */
.typing-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  width: auto;
  min-width: 60px;
  padding: 10px 15px;
}

.typing-indicator .dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: white;
  margin: 0 3px;
  animation: bounce 1.5s infinite ease-in-out;
}

.typing-indicator .dot:nth-child(1) {
  animation-delay: 0s;
}

.typing-indicator .dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator .dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-5px);
  }
}
/* Chatbot container */
.chatbot {
  position: fixed;
  bottom: 20px;
  right: 20px;
  cursor: pointer;
  z-index: 1000;
  transition: all 0.3s ease-in-out;
  border-radius: 50%;
  background-color: #0078d4;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 15px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
}

/* Chat bubble (icon only) */
.chat-bubble {
  font-size: 24px;
}

/* When chatbot is open */
.chatbot.open {
  width: 350px;
  height: 500px;
  border-radius: 10px;
  padding: 0;
}

/* Chat content */
.chat-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #fff;
  border-radius: 10px;
  overflow: hidden;
  position: relative;
}

/* Header of the chat */
.chat-header {
  background-color: #0078d4;
  color: white;
  padding: 10px;
  text-align: center;
  font-size: 18px;
  position: relative;
}

/* Close button (X) */
.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
}

.close-button:hover {
  color: #ff5555;
}

/* Messages section */
.messages {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
  background-color: #f9f9f9;
  display: flex;
  flex-direction: column;
}

/* Individual messages */
.message {
  padding: 10px;
  margin: 10px 0;
  border-radius: 20px;
  max-width: 80%;
  word-wrap: break-word;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
  position: relative;
}

.message.bot {
  background-color: #799efc;
  align-self: flex-start;
  text-align: left;
}

.message.user {
  background-color: #0078d4;
  color: white;
  align-self: flex-end;
  text-align: right;
}

/* Input section */
.chat-input {
  display: flex;
  padding: 10px;
  background-color: #f1f1f1;
}

.chat-input input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.chat-input button {
  padding: 8px 12px;
  margin-left: 10px;
  background-color: #0078d4;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.chat-input button:hover {
  background-color: #005bb5;
}

/* Voice button styles */
.voice-button {
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0;
}

.voice-button.recording {
  background-color: #ff4a4a;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(255, 74, 74, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(255, 74, 74, 0); }
  100% { box-shadow: 0 0 0 0 rgba(255, 74, 74, 0); }
}

/* Transcript preview */
.transcript-preview {
  position: absolute;
  bottom: 60px;
  left: 0;
  right: 0;
  background-color: white;
  border-top: 1px solid #ddd;
  padding: 10px;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
}

.transcript-text {
  background-color: #e9f0f8;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
  max-height: 100px;
  overflow-y: auto;
  color: #333;
  font-weight: normal;
  border: 1px solid #d0e0f0;
}

.voice-status {
  color: #666;
  font-style: italic;
  margin-bottom: 8px;
}

.transcript-actions {
  display: flex;
  justify-content: flex-end;
}

.cancel-voice {
  padding: 5px 10px;
  margin-left: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #f1f1f1;
  color: #333;
}
</style>