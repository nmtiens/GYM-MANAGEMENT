<template>
  <div class="login-container">

    <div class="notification-container">
      <div
        class="notification-box"
        ref="notificationBox"
        @mousedown="makeBoxDraggable"
      >
        <h2>Chào mừng quý khách !!!</h2>
        <button @click="handleLogin" :disabled="isLoading">
          {{ isLoading ? 'Đang kiểm tra...' : 'Kiểm tra thông tin thẻ hội viên' }}
        </button>
        <p v-if="message">{{ message }}</p>
        <p v-if="expirationMessage">{{ expirationMessage }}</p>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </div>
      <Chatbot />
      <MemberInfo v-if="MaHoiVien && MaHoiVien !== ''" :MaHoiVien="MaHoiVien" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import MemberInfo from "@/components/MemberInfo.vue";

export default {
  components: { MemberInfo },
  data() {
    return {
      isLoading: false,
      message: "",
      expirationMessage: "",
      errorMessage: "",
      MaHoiVien: null,
      loginTime: null,
    };
  },
  methods: {
    goBack() {
      this.$router.push('/');
    },
    async handleLogin() {
      this.isLoading = true;
      this.errorMessage = "";
      this.MaHoiVien = null;

      try {
        const response = await axios.post("http://localhost:5000/login");
        console.log("Login API Response:", response.data);

        if (response.data && response.data.MaHoiVien) {
          this.message = response.data.message;
          this.expirationMessage = response.data.expiration_message;
          this.MaHoiVien = response.data.MaHoiVien;
          console.log("Mã hội viên nhận được:", this.MaHoiVien);
        } else {
          this.errorMessage = "Không tìm thấy mã hội viên.";
        }
      } catch (error) {
        console.error("API Error:", error);
        this.errorMessage = "Đăng nhập thất bại. Vui lòng thử lại.";
      } finally {
        this.isLoading = false;
      }
    },
    makeBoxDraggable(event) {
      const box = this.$refs.notificationBox;
      let offsetX = event.clientX - box.getBoundingClientRect().left;
      let offsetY = event.clientY - box.getBoundingClientRect().top;

      const mouseMoveHandler = (moveEvent) => {
        box.style.position = "absolute";
        box.style.left = `${moveEvent.clientX - offsetX}px`;
        box.style.top = `${moveEvent.clientY - offsetY}px`;
      };

      const mouseUpHandler = () => {
        document.removeEventListener("mousemove", mouseMoveHandler);
        document.removeEventListener("mouseup", mouseUpHandler);
      };

      document.addEventListener("mousemove", mouseMoveHandler);
      document.addEventListener("mouseup", mouseUpHandler);
    }
  }
};
</script>

<style scoped>
.login-container {
  width: 100%;
  min-height: 100vh;
}

.back-btn {
  position: absolute;
  top: 20px;
  left: 20px;
  font-size: 18px;
  font-weight: bold;
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.back-btn:hover {
  background-color: #0056b3;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.back-btn:active {
  transform: translateY(1px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
}

.notification-container {
  height: 80vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: url("https://cdn.unityfitness.vn/2024/08/trai-nghiem-phong-gym.jpg") no-repeat center center fixed;
  background-size: cover;
  margin: 0;
  position: relative;
}

/* Thêm thuộc tính position relative để hỗ trợ di chuyển */
.notification-box {
  width: 500px;
  padding: 40px;
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
  text-align: center;
  cursor: grab;
  position: absolute;
}

/* Khi đang kéo */
.notification-box:active {
  cursor: grabbing;
}

/* Các styles khác giữ nguyên */
h2 {
  margin-bottom: 30px;
  font-size: 32px;
  font-weight: bold;
  color: #333;
}

p {
  margin-top: 20px;
  font-size: 18px;
  color: #444;
  line-height: 1.8;
}

button {
  padding: 14px 28px;
  font-size: 18px;
  font-weight: normal;
  cursor: pointer;
  transition: background-color 0.2s ease, box-shadow 0.3s ease;
  border-radius: 8px;
  border: 2px solid transparent;
  background-color: #007bff;
  color: white;
}

button:hover {
  background-color: #0056b3;
}

button:active {
  background-color: #004085;
}

button:disabled {
  background-color: #c0c0c0;
  cursor: not-allowed;
}

.error-message {
  margin-top: 20px;
  color: red;
  font-weight: bold;
}

@media (max-width: 768px) {
  .notification-box {
    width: 90%;
    padding: 30px;
  }

  h2 {
    font-size: 28px;
  }

  p {
    font-size: 16px;
  }

  button {
    font-size: 18px;
  }
}
</style>