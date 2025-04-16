<template>
  <Chatbot />
  <div class="login-page">
    <div class="login-content">
      <div class="logo-section">
        <h1 class="app-title">FITNESS CLUB</h1>
        <p class="app-tagline">Hệ thống quản lý phòng tập chuyên nghiệp</p>
      </div>
      
      <div class="login-form-container">
        <h2 class="welcome-text">Chào mừng trở lại</h2>
        
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="input-group">
            <label for="username">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
              Tên đăng nhập
            </label>
            <input 
              type="text" 
              id="username" 
              v-model="username" 
              placeholder="Nhập tên đăng nhập"
              required 
            />
          </div>
          
          <div class="input-group">
            <label for="password">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
              Mật khẩu
            </label>
            <div class="password-input">
              <input 
                :type="showPassword ? 'text' : 'password'" 
                id="password" 
                v-model="password" 
                placeholder="Nhập mật khẩu"
                required 
              />
              <button type="button" class="toggle-password" @click="showPassword = !showPassword">
                <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>
              </button>
            </div>
          </div>
          
         
          
          <div class="error-message" v-if="errorMessage">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
            {{ errorMessage }}
          </div>
          
          <div class="buttons-container">
            <button type="submit" class="login-button primary-button">
              <span>Đăng nhập</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
            </button>
            
         <button 
  type="button" 
  @click="navigateToFaceLogin" 
  class="face-login-button"
  :disabled="isLoading"
>
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="9" cy="9" r="1"></circle><circle cx="15" cy="9" r="1"></circle><path d="M8 14s1.5 2 4 2 4-2 4-2"></path></svg>
         <span>{{ isLoading ? 'Đang nhận diện...' : 'Đăng nhập bằng khuôn mặt' }}</span>
            </button>
          </div>
        </form>
        
        <div class="register-prompt">
          <p>Chưa có tài khoản? <router-link to="/register" class="register-link">Đăng ký ngay</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios"; // Thêm import axios
import Chatbot from "./Chatbot.vue";

export default {
  name: "Login",
  setup() {
    const router = useRouter();
    const username = ref("");
    const password = ref("");
    const errorMessage = ref("");
    const rememberMe = ref(false);
    const showPassword = ref(false);
    const isLoading = ref(false); // Thêm biến quản lý trạng thái loading

    // Trong file Login.vue, cập nhật hàm handleLogin:

const handleLogin = () => {
  if (username.value === "admin" && password.value === "1234") {
    // Lưu thông tin đăng nhập
    const loginData = {
      username: username.value,
      role: "admin",
      loginTime: new Date().toISOString(),
      // Có thể thêm thông tin khác nếu cần
    };
    
    // Lưu vào localStorage
    localStorage.setItem("token", "admin-token"); // Token đăng nhập
    localStorage.setItem("currentUser", JSON.stringify(loginData)); // Thông tin chi tiết
    
    errorMessage.value = "";
    router.push("/admin");
  } else if (username.value === "nhanvien" && password.value === "5678") {
    // Lưu thông tin đăng nhập
    const loginData = {
      username: username.value,
      role: "staff",
      loginTime: new Date().toISOString(),
      // Có thể thêm thông tin khác nếu cần
    };
    
    // Lưu vào localStorage
    localStorage.setItem("token", "staff-token"); // Token đăng nhập
    localStorage.setItem("currentUser", JSON.stringify(loginData)); // Thông tin chi tiết
    
    errorMessage.value = "";
    router.push("/staff");
  } else {
    errorMessage.value = "Tên đăng nhập hoặc mật khẩu không chính xác!";
  }
};

// Tương tự, cập nhật hàm navigateToFaceLogin:

// Trong file Login.vue, cập nhật hàm navigateToFaceLogin:

const navigateToFaceLogin = async () => {
  isLoading.value = true;

  try {
    // Giả lập API hoặc thực hiện gọi API thực tế
    const response = await axios.post("http://localhost:5000/login", {
      // Thông tin nhận diện khuôn mặt nếu cần
    });

    if (response.data && response.data.MaHoiVien) {
      // Lưu thông tin đăng nhập
      const loginData = {
        id: response.data.MaHoiVien,
        originalExpirationDate: response.data.Original_Expiration_Date || null,
        username: response.data.username || "Face Login User",
        role: "user",
        loginTime: new Date().toISOString(),
        loginMethod: "face",
        // Có thể thêm thông tin khác từ response
      };
      
      // Lưu vào localStorage
      localStorage.setItem("token", response.data.token || "user-token"); 
      localStorage.setItem("currentUser", JSON.stringify(loginData));
      
      errorMessage.value = "";
      router.push("/users");
    } else {
      errorMessage.value = "Nhận diện khuôn mặt không thành công!";
    }
  } catch (error) {
    errorMessage.value = "Đăng nhập bằng khuôn mặt không thành công. Vui lòng thử lại.";
    console.error("Face Login Error:", error);
  } finally {
    isLoading.value = false;
  }
};
    return {
      username,
      password,
      errorMessage,
      rememberMe,
      showPassword,
      isLoading, // Thêm vào để sử dụng trong template
      handleLogin,
      navigateToFaceLogin,
    };
  },
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
background: linear-gradient(135deg, rgba(13, 22, 35, 0.6), rgba(8, 15, 26, 0.65)),
            url('/images/gym-background.jpg');

  background-size: cover;
  background-position: center;
  padding: 20px;
}

.login-content {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 480px;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

.logo-section {
  padding: 40px 30px;
  text-align: center;
  background: linear-gradient(135deg, #0a4d68, #088395);
  color: white;
}

.app-title {
  font-size: 3rem;
  font-weight: 800;
  margin: 0;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.app-tagline {
  margin-top: 10px;
  font-size: 1rem;
  opacity: 0.9;
}

.login-form-container {
  padding: 40px;
  background-color: #f9f9f9;
}

.welcome-text {
  font-size: 1.8rem;
  font-weight: 700;
  color: #0a4d68;
  margin-top: 0;
  margin-bottom: 30px;
  text-align: center;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #1a5f7a;
  font-size: 1rem;
}

.icon {
  width: 18px;
  height: 18px;
}

input[type="text"],
input[type="password"] {
  padding: 14px 16px;
  border: 2px solid #e1e1e1;
  border-radius: 12px;
  font-size: 1rem;
  width: 100%;
  transition: all 0.3s;
}

input[type="text"]:focus,
input[type="password"]:focus {
  border-color: #0a4d68;
  outline: none;
  box-shadow: 0 0 0 3px rgba(10, 77, 104, 0.2);
}

.password-input {
  position: relative;
  display: flex;
  align-items: center;
}

.toggle-password {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  color: #777;
  padding: 0;
  display: flex;
  align-items: center;
}

.toggle-password:hover {
  color: #555;
}

.options-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 5px 0;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: normal;
  font-size: 0.9rem;
}

.forgot-password {
  color: #0a4d68;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.2s;
}

.forgot-password:hover {
  text-decoration: underline;
}

.error-message {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background-color: #fdeaeb;
  border-radius: 8px;
  color: #e53935;
  font-size: 0.9rem;
  gap: 8px;
}

.buttons-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 10px;
}

button {
  padding: 14px 24px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  border: none;
}

.primary-button {
  background: linear-gradient(135deg, #0a4d68, #088395);
  color: white;
}

.primary-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(10, 77, 104, 0.3);
}

.face-login-button {
  background-color: white;
  color: #1a5f7a;
  border: 2px solid #e1e1e1;
}

.face-login-button:hover {
  background-color: #f5f5f5;
  border-color: #0a4d68;
}

.register-prompt {
  text-align: center;
  margin-top: 30px;
  font-size: 0.95rem;
  color: #666;
}

.register-link {
  color: #0a4d68;
  font-weight: 600;
  text-decoration: none;
}

.register-link:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .login-content {
    border-radius: 16px;
  }
  
  .app-title {
    font-size: 2.5rem;
  }
  
  .login-form-container {
    padding: 30px 20px;
  }
  
  .welcome-text {
    font-size: 1.5rem;
    margin-bottom: 20px;
  }
  
  button {
    padding: 12px 20px;
  }
}
</style>