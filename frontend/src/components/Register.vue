<template>
  <div class="registration-page">
    
    <div class="registration-card">
      <div class="card-header">
        <h1 class="title">Đăng Ký Hội Viên</h1>
        <p class="subtitle">Điền thông tin để đăng ký hội viên mới</p>
      </div>

      <transition name="fade">
        <div v-if="errorMessage" class="alert alert-error">
          <span class="alert-icon">⚠️</span>
          <span>{{ errorMessage }}</span>
        </div>
      </transition>

      <form @submit.prevent="registerHoiVien" class="registration-form">
        <div class="form-grid">
          <!-- Thông tin cá nhân -->
          <div class="form-section">
            <h2 class="section-title">Thông tin cá nhân</h2>
            
            <div class="form-group">
              <label for="hoTen">Họ và tên <span class="required">*</span></label>
              <input id="hoTen" type="text" v-model="form.hoTen" required placeholder="Nhập họ và tên" />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="ngaySinh">Ngày sinh</label>
                <input id="ngaySinh" type="date" v-model="form.ngaySinh" />
              </div>

              <div class="form-group">
                <label for="gioiTinh">Giới tính</label>
                <select id="gioiTinh" v-model="form.gioiTinh">
                  <option value="Nam">Nam</option>
                  <option value="Nữ">Nữ</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label for="diaChi">Địa chỉ</label>
              <input id="diaChi" type="text" v-model="form.diaChi" placeholder="Nhập địa chỉ" />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="soDienThoai">Số điện thoại <span class="required">*</span></label>
                <input id="soDienThoai" type="text" v-model="form.soDienThoai" required placeholder="Nhập số điện thoại" />
              </div>

              <div class="form-group">
                <label for="email">Email</label>
                <input id="email" type="email" v-model="form.email" placeholder="Nhập email" />
              </div>
            </div>
          </div>

          <!-- Thông tin đăng ký -->
          <div class="form-section">
            <h2 class="section-title">Thông tin đăng ký</h2>
            
            <div class="form-group">
              <label for="nhanVienTao">Nhân viên tạo</label>
              <select id="nhanVienTao" v-model="form.nhanVienTao" :disabled="!danhSachNhanVien.length">
                <option disabled value="">Chọn nhân viên</option>
                <option v-for="nv in danhSachNhanVien" :key="nv" :value="nv">{{ nv }}</option>
              </select>
            </div>

            <div class="form-group">
              <label for="huanLuyenVien">Huấn luyện viên</label>
              <div class="input-with-button">
                <input
                  id="huanLuyenVien"
                  type="text"
                  v-model="form.huanLuyenVien"
                  readonly
                  placeholder="Chọn huấn luyện viên"
                />
                <button type="button" @click="showHLVModal" class="button-select">
                  <span class="button-icon">👤</span> Chọn
                </button>
              </div>
            </div>

            <div class="form-group">
              <label for="goiTap">Gói tập <span class="required">*</span></label>
              <select id="goiTap" v-model="form.goiTap" required :disabled="!danhSachGoiTap.length">
                <option disabled value="">Chọn gói tập</option>
                <option v-for="goi in danhSachGoiTap" :key="goi" :value="goi">{{ goi }}</option>
              </select>
              <small v-if="validationErrors.goiTap" class="error-text">{{ validationErrors.goiTap }}</small>
            </div>

            <div class="form-group">
              <label>Thời gian đăng ký</label>
              <div class="time-selection">
                <div class="number-input">
                  <button type="button" @click="decrementValue">−</button>
                  <input type="number" v-model.number="form.soLuong" min="1" />
                  <button type="button" @click="incrementValue">+</button>
                </div>
                <select v-model="form.donVi" class="time-unit">
                  <option value="Ngày">Ngày</option>
                  <option value="Tháng">Tháng</option>
                  <option value="Năm">Năm</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label for="dichVu">Dịch vụ đăng ký</label>
              <div class="custom-dropdown">
                <div class="selected-option" @click="toggleDichVuDropdown">
                  <span v-if="selectedDichVus.length">{{ selectedDichVus.join(', ') }}</span>
                  <span v-else class="placeholder">Chọn dịch vụ</span>
                  <span class="dropdown-arrow">▼</span>
                </div>
                <div v-if="showDichVuDropdown" class="dropdown-options">
                  <div v-for="dichVu in danhSachDichVu" :key="dichVu.value" class="dropdown-option">
                    <label>
                      <span>{{ dichVu.label }}</span>
                      <input type="checkbox" v-model="selectedDichVuValues" :value="dichVu.value" />
                    </label>
                  </div>
                </div>
              </div>
            </div>

            <div class="form-group checkbox-group">
              <label class="checkbox-container">
                <input type="checkbox" v-model="form.luuKhuonMat" />
                <span class="checkmark"></span>
                Lưu khuôn mặt
              </label>
            </div>
          </div>
        </div>

       <div class="form-actions">
  <button type="button" @click="resetForm" class="button-secondary">Làm mới</button>
  <button type="submit" class="button-primary" :disabled="isLoading">
    <span v-if="isLoading" class="spinner"></span>
    <span>{{ isLoading ? "Đang đăng ký..." : "Đăng ký" }}</span>
  </button>
</div>

<!-- Add this new login line -->
<div class="login-line">
  Đã có tài khoản? <a href="/" class="login-text">Đăng nhập</a>
</div>
      </form>
    </div>

    <!-- Modal HLV -->
    <transition name="modal-fade">
      <div v-if="showInfoHLV" class="modal-overlay" @click.self="closeModal">
        <div class="modal-container">
          <div class="modal-header">
            <h2>Chọn Huấn Luyện Viên</h2>
            <button @click="closeModal" class="close-button">&times;</button>
          </div>
          <InfoHLV
            :danhSachHuanLuyenVien="danhSachHuanLuyenVien"
            @select="selectHLV"
            @close="closeModal"
          />
        </div>
      </div>
    </transition>

    <!-- Thông báo thành công -->
    <transition name="modal-fade">
      <div v-if="showSuccessModal" class="modal-overlay">
        <div class="modal-container success-modal">
          <div class="modal-icon">✅</div>
          <h2>Đăng Ký Thành Công!</h2>
          <p>{{ message }}</p>
          <div class="modal-actions">
            <button @click="showSuccessModal = false" class="button-primary">Đóng</button>
            <button @click="navigateToLogin" class="button-secondary">Quay về đăng nhập</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Thông báo lỗi -->
    <transition name="modal-fade">
      <div v-if="showErrorModal" class="modal-overlay">
        <div class="modal-container error-modal">
          <div class="modal-icon">❌</div>
          <h2>Đăng Ký Thất Bại</h2>
          <p>{{ errorMessage }}</p>
          <button @click="showErrorModal = false" class="button-primary">Đóng</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from "axios";
import InfoHLV from "./InfoHLV.vue";

export default {
  components: { InfoHLV },
  data() {
    return {
      showSuccessModal: false,
      showErrorModal: false,
      showDichVuDropdown: false,
      selectedDichVuValues: [],
      showInfoHLV: false,
      danhSachNhanVien: [],
      danhSachHuanLuyenVien: [],
      danhSachGoiTap: [],
      danhSachDichVu: [],
      form: {
        hoTen: "",
        ngaySinh: "",
        gioiTinh: "Nam",
        diaChi: "",
        soDienThoai: "",
        email: "",
        nhanVienTao: "",
        huanLuyenVien: "",
        goiTap: "",
        dichVu: [],
        soLuong: 1,
        donVi: "Tháng",
        luuKhuonMat: false,
      },
      validationErrors: {
        goiTap: ""
      },
      errorMessage: "",
      message: "",
      isLoading: false,
    };
  },
  computed: {
    selectedDichVus() {
      return this.selectedDichVuValues.map(value => {
        const dichVu = this.danhSachDichVu.find(dv => dv.value === value);
        return dichVu ? dichVu.label : value;
      });
    }
  },
  watch: {
    selectedDichVuValues(newValues) {
      this.form.dichVu = newValues;
    },
    'form.goiTap'(newValue) {
      if (newValue) {
        this.validationErrors.goiTap = "";
      }
    }
  },
  async mounted() {
  try {
    await this.loadInitialData();

    // Lấy tên gói tập từ query parameter
    const packageName = this.$route.query.packageName;
    
    // Kiểm tra nếu có tên gói tập
    if (packageName) {
      // Đợi một chút để danh sách gói tập được load
      this.$nextTick(() => {
        // Kiểm tra xem gói tập có trong danh sách không
        if (this.danhSachGoiTap.includes(packageName)) {
          this.form.goiTap = packageName;
        } else {
          console.warn(`Gói tập "${packageName}" không tồn tại trong danh sách`);
        }
      });
    }

     const selectedTrainer = this.$route.query.huanluyenvien;
    if (selectedTrainer) {
      this.form.huanLuyenVien = selectedTrainer;
    }
  } catch (error) {
    console.error("Lỗi khi tải dữ liệu:", error);
    this.errorMessage = "Không thể tải danh sách từ server.";
  }
},
  methods: {
    async loadInitialData() {
      try {
        const [nvRes, hlvRes, goiRes, dvRes] = await Promise.all([
          axios.get("http://127.0.0.1:5000/nhanvien/"),
          axios.get("http://127.0.0.1:5000/huanluyenvien/"),
          axios.get("http://127.0.0.1:5000/goitap/"),
          axios.get("http://127.0.0.1:5000/dichvu/"),
        ]);

        this.danhSachNhanVien = nvRes.data.map(nv => nv.HoTen);
        this.danhSachHuanLuyenVien = hlvRes.data.map(hlv => hlv.HoTen);
        this.danhSachGoiTap = goiRes.data.map(goi => goi.TenGoiTap);
        this.danhSachDichVu = dvRes.data.map(dv => ({ value: dv.TenDichVu, label: dv.TenDichVu }));
        
        console.log("Danh sách gói tập đã tải:", this.danhSachGoiTap);
      } catch (error) {
        throw error;
      }
    },
    navigateToLogin() {
      window.location.href = '/';
    },
    incrementValue() {
      this.form.soLuong++;
    },
    decrementValue() {
      if (this.form.soLuong > 1) {
        this.form.soLuong--;
      }
    },
    toggleDichVuDropdown() {
      this.showDichVuDropdown = !this.showDichVuDropdown;
      // Close dropdown when clicking outside
      if (this.showDichVuDropdown) {
        setTimeout(() => {
          document.addEventListener('click', this.closeDichVuDropdown);
        }, 0);
      }
    },
    closeDichVuDropdown(event) {
      const dropdown = document.querySelector('.custom-dropdown');
      if (dropdown && !dropdown.contains(event.target)) {
        this.showDichVuDropdown = false;
        document.removeEventListener('click', this.closeDichVuDropdown);
      }
    },
    showHLVModal() {
      this.showInfoHLV = true;
    },
    closeModal() {
      this.showInfoHLV = false;
    },
    selectHLV(hlvName) {
      this.form.huanLuyenVien = hlvName;
      this.closeModal();
    },
    validateForm() {
      let isValid = true;
      
      // Kiểm tra gói tập
      if (!this.form.goiTap) {
        this.validationErrors.goiTap = "Vui lòng chọn gói tập";
        isValid = false;
      }
      
      return isValid;
    },
    async registerHoiVien() {
      if (!this.validateForm()) {
        this.errorMessage = "Vui lòng điền đầy đủ thông tin bắt buộc";
        return;
      }
      
      this.isLoading = true;
      try {
        // Tạo dữ liệu gửi đi
        const formData = {
          ...this.form,
          dichVu: this.form.dichVu.join(", ")
        };
        
        console.log("Dữ liệu gửi đi:", formData);
        
        const response = await axios.post("http://127.0.0.1:5000/register", formData);
        console.log("Phản hồi từ server:", response.data);

        this.message = response.data.message;
        this.showSuccessModal = true;

        // Đặt lại form sau khi thành công
        this.resetForm();
      } catch (error) {
        console.error("Lỗi khi đăng ký:", error.response || error);
        this.errorMessage = error.response?.data?.detail || "Có lỗi xảy ra khi đăng ký!";
        this.showErrorModal = true;
      } finally {
        this.isLoading = false;
      }
    },
    resetForm() {
      // Tạo object mới để reset form
      this.form = {
        hoTen: "",
        ngaySinh: "",
        gioiTinh: "Nam",
        diaChi: "",
        soDienThoai: "",
        email: "",
        nhanVienTao: "",
        huanLuyenVien: "",
        goiTap: "",
        dichVu: [],
        soLuong: 1,
        donVi: "Tháng",
        luuKhuonMat: false,
      };
      
      // Reset các giá trị liên quan
      this.selectedDichVuValues = [];
      this.validationErrors = { goiTap: "" };
    }
  },
  beforeDestroy() {
    document.removeEventListener('click', this.closeDichVuDropdown);
  }
};
</script>

<style scoped>
.registration-page {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
background: linear-gradient(135deg, rgba(13, 22, 35, 0.6), rgba(8, 15, 26, 0.65)),
            url('/images/gym-background.jpg');
  padding: 20px;
  position: relative;
}



.registration-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 1000px;
  overflow: hidden;
  margin-top: 40px;
}

.card-header {
  background: #0a4d68;
  padding: 24px 32px;
  color: white;
  text-align: center;
}

.title {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
}

.subtitle {
  color: #fff;
  margin: 8px 0 0;
  font-size: 16px;
  opacity: 0.9;
}

.registration-form {
  padding: 32px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .back-to-login {
    position: relative;
    top: 0;
    left: 0;
    margin-bottom: 20px;
    align-self: flex-start;
  }
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 20px 0;
  padding-bottom: 12px;
  border-bottom: 2px solid #f0f2f5;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #4a5568;
}

.required {
  color: #e53e3e;
}

input[type="text"],
input[type="email"],
input[type="date"],
input[type="number"],
select,
.selected-option {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  font-size: 15px;
  transition: all 0.3s;
}

input:focus,
select:focus {
  outline: none;
  border-color: #3a7bd5;
  box-shadow: 0 0 0 3px rgba(58, 123, 213, 0.1);
}

/* Time selection */
.time-selection {
  display: flex;
  align-items: center;
  gap: 10px;
}

.number-input {
  display: flex;
  align-items: center;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  overflow: hidden;
}

.number-input button {
  background: #f5f7fa;
  border: none;
  color: #606266;
  font-size: 18px;
  width: 36px;
  height: 36px;
  cursor: pointer;
}

.number-input button:hover {
  background: #e9ecef;
}

.number-input input {
  width: 60px;
  text-align: center;
  border: none;
  padding: 8px;
appearance: none;
-webkit-appearance: none; /* Cho trình duyệt Webkit (Chrome, Safari) */
-moz-appearance: none;    /* Cho Firefox */

}

.number-input input::-webkit-outer-spin-button,
.number-input input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.time-unit {
  flex: 1;
}

/* Custom dropdown */
.custom-dropdown {
  position: relative;
}

.selected-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  background: white;
}

.placeholder {
  color: #a0aec0;
}

.dropdown-arrow {
  font-size: 12px;
  color: #718096;
}

.dropdown-options {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
  background: white;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 10;
  margin-top: 4px;
}

.dropdown-option {
  padding: 10px 16px;
  cursor: pointer;
}

.dropdown-option:hover {
  background: #f7fafc;
}

.dropdown-option {
  padding: 10px 16px;
  cursor: pointer;
}

.dropdown-option label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 0;
  width: 100%;
  cursor: pointer;
  white-space: nowrap;
}

.dropdown-option label span {
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
  text-align: left;
}

.dropdown-option input[type="checkbox"] {
  margin-left: 10px;
  flex-shrink: 0;
  width: 16px;
  height: 16px;
}

/* Input with button */
.input-with-button {
  display: flex;
  gap: 8px;
}

.input-with-button input {
  flex: 1;
}

.button-select {
  padding: 0 16px;
  background: #0a4d68;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
}

.button-icon {
  font-size: 14px;
  background-color: #fff;
}

/* Checkbox */
.checkbox-container {
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
  cursor: pointer;
  user-select: none;
  padding: 8px 0;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  height: 18px;
  width: 18px;
  background-color: #ffffff;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  position: relative;
}

.checkbox-container input:checked ~ .checkmark {
  background-color: #0a4d68;
  border-color: #0a4d68;
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

.checkbox-container input:checked ~ .checkmark:after {
  display: block;
  left: 6px;
  top: 2px;
  width: 4px;
  height: 9px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

/* Form actions */
.form-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 32px;
}

.button-primary,
.button-secondary {
  min-width: 120px;
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
}

.button-primary {
  background: #0a4d68;
  color: white;
  border: none;
}

.button-primary:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.button-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.button-secondary {
  background: white;
  color: #4a5568;
  border: 1px solid #dcdfe6;
}

.button-secondary:hover {
  background: #f8f9fa;
}

/* Spinner */
.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Alerts */
.alert {
  padding: 12px 16px;
  border-radius: 6px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.alert-error {
  background-color: #fff5f5;
  color: #c53030;
  border-left: 4px solid #fc8181;
}

.alert-icon {
  font-size: 18px;
}

/* Modals */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal-container {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #f0f2f5;
}

.modal-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  color: #a0aec0;
  cursor: pointer;
}

.success-modal,
.error-modal {
  text-align: center;
  padding: 32px;
  width: 90%;
  max-width: 400px;
}

.modal-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.success-modal h2,
.error-modal h2 {
  margin: 0 0 12px;
  font-size: 20px;
  font-weight: 600;
}

.success-modal p,
.error-modal p {
  margin: 0 0 24px;
  color: #4a5568;
}

/* Modal actions */
.modal-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
}

/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s;
}
.modal-fade-enter, .modal-fade-leave-to {
  opacity: 0;
}
.modal-fade-enter .modal-container,
.modal-fade-enter .success-modal,
.modal-fade-enter .error-modal {
  transform: scale(0.9);
  transition: transform 0.3s;
}
.modal-fade-enter-to .modal-container,
.modal-fade-enter-to .success-modal,
.modal-fade-enter-to .error-modal {
  transform: scale(1);
}


/* Login line at end of form */
.login-line {
  text-align: center;
  margin-top: 20px;
  color: #4a5568;
  font-size: 15px;
}

.login-text {
  color: #0a4d68;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.login-text:hover {
  text-decoration: underline;
}
</style>