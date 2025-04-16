<template>
  <div class="custom-container">
    <h1 class="custom-title">Danh Sách Thẻ Hội Viên</h1>

    <div class="custom-search">
      <input v-model="searchQuery" placeholder="Tìm theo tên hội viên..." class="custom-input" />
      <select v-model="filterStatus" class="custom-input">
        <option value="">Tất cả</option>
        <option value="valid">Còn hạn</option>
        <option value="expired">Hết hạn</option>
        <option value="today">Đăng ký hôm nay</option>
        <option value="login_today">Đăng nhập hôm nay</option>
      </select>
    </div>

    <p v-if="isLoading" class="loading-overlay">Đang tải dữ liệu...</p>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <table v-if="!isLoading && paginatedTheHoiVienList.length > 0" class="custom-table">
      <thead>
        <tr>
          <th>Mã Thẻ Hội Viên</th>
          <th>Hội Viên</th>
          <th>Nhân Viên Tạo</th>
          <th>Huấn Luyện Viên</th>
          <th>Gói Tập</th>
          <th>Dịch Vụ</th>
          <th>Ngày Tạo Thẻ</th>
          <th>Ngày Hết Hạn</th>
          <th>Đăng nhập gần đây</th>
          <th>Hành động</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in paginatedTheHoiVienList" :key="item._id" :class="{ 
          'expired': isExpired(item.NgayHetHan), 
          'today-created': isCreatedToday(item.NgayTao),
          'login-today': hasLoginToday(item.Login_History)
        }">
          <td>{{ item.MaTheHoiVien }}</td>
          <td>{{ item.HoiVien }}</td>
          <td>{{ item.NhanVien }}</td>
          <td>{{ item.HuanLuyenVien }}</td>
          <td>{{ item.GoiTap }}</td>
          <td>{{ formatDichVu(item.DichVu) }}</td>
          <td>{{ formatDate(item.NgayTao) }}</td>
          <td>{{ formatDate(item.NgayHetHan) }}</td>
          <td>
            {{ formatLoginHistory(item.Login_History) }}
            <button 
              v-if="item.Login_History && Array.isArray(item.Login_History) && item.Login_History.length > 0" 
              @click="showLoginHistory(item)" 
              class="custom-btn custom-btn-info btn-sm">
              Chi tiết
            </button>
          </td>
          <td>
            <button @click="editItem(item)" class="custom-btn custom-btn-edit">Sửa</button>
            <button @click="confirmDeleteItem(item)" class="custom-btn custom-btn-delete">Xóa</button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="!isLoading && theHoiVienList.length === 0">Không có dữ liệu.</p>

    <div class="pagination">
      <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">Trước</button>
      <span>Trang {{ currentPage }} / {{ totalPages }}</span>
      <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">Sau</button>
    </div>

    <transition name="fade">
      <div v-if="editingItem" class="custom-modal">
        <div class="custom-modal-content">
          <h2 class="custom-title">Chỉnh Sửa Thẻ Hội Viên</h2>
          <form @submit.prevent="updateItem" class="custom-form">
            <div class="form-group">
              <label>Hội Viên:</label>
              <input v-model="editingItem.HoiVien" class="custom-input" required />
            </div>

            <div class="form-group">
              <label>Nhân Viên Tạo:</label>
              <input v-model="editingItem.NhanVien" class="custom-input" required />
            </div>

            <div class="form-group">
              <label>Huấn Luyện Viên:</label>
              <input v-model="editingItem.HuanLuyenVien" class="custom-input"  />
            </div>

            <div class="form-group">
              <label>Gói Tập:</label>
              <input v-model="editingItem.GoiTap" class="custom-input" required />
            </div>

            <div class="form-group">
              <label>Dịch Vụ:</label>
              <input v-model="editingItem.DichVu" class="custom-input" />
            </div>

            <div class="form-group">
              <label>Ngày Hết Hạn:</label>
             <input 
              v-model="editingItem.NgayHetHan" 
              type="date" 
              :min="new Date().toISOString().split('T')[0]" 
              class="custom-input" 
              required 
            />
            </div>

            <div class="custom-btn-group">
              <button type="submit" class="custom-btn custom-btn-save">Lưu</button>
              <button type="button" @click="cancelEdit" class="custom-btn custom-btn-cancel">Hủy</button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- Thông báo Cập nhật -->
    <transition name="fade">
      <div v-if="showUpdateSuccess" class="custom-modal">
        <div class="custom-modal-content">
          <h2 class="modal-title">Thông báo</h2>
          <p>Cập nhật thẻ hội viên <strong>{{ editingItem?.HoiVien || "này" }}</strong> thành công!</p>
          <div class="custom-btn-group">
            <button @click="closeUpdateModal" class="custom-btn custom-btn-save">Đóng</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Thông báo Xóa -->
    <transition name="fade">
      <div v-if="showConfirmDelete" class="custom-modal">
        <div class="custom-modal-content">
          <h2 class="modal-title">Xác nhận xóa</h2>
          <p>Bạn có chắc muốn xóa thẻ hội viên <strong>{{ selectedTheHoiVien?.HoiVien || "này" }}</strong> không?</p>
          <div class="custom-btn-group">
            <button @click="deleteItem" class="custom-btn custom-btn-delete">Xóa</button>
            <button @click="showConfirmDelete = false" class="custom-btn custom-btn-cancel">Hủy</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Modal Lịch sử đăng nhập -->
    <transition name="fade">
      <div v-if="showLoginHistoryModal" class="custom-modal">
        <div class="custom-modal-content">
          <h2 class="modal-title">Lịch sử đăng nhập</h2>
          <p>Hội viên: <strong>{{ selectedLoginHistory?.HoiVien || "Không xác định" }}</strong></p>
          <p>Mã thẻ: <strong>{{ selectedLoginHistory?.MaTheHoiVien || "Không xác định" }}</strong></p>
          
          <div class="login-history-list">
            <div v-if="!selectedLoginHistory?.Login_History || selectedLoginHistory.Login_History.length === 0"
                class="no-history">
              Chưa có lịch sử đăng nhập
            </div>
            <ul v-else>
              <li v-for="(loginDate, index) in selectedLoginHistory.Login_History" :key="index" 
                  :class="{ 'login-today-item': isLoginToday(loginDate) }">
                {{ formatDate(loginDate) }}
                <span v-if="isLoginToday(loginDate)" class="today-badge">Hôm nay</span>
              </li>
            </ul>
            
            <!-- Thống kê cơ bản -->
            <div v-if="selectedLoginHistory?.Login_History && selectedLoginHistory.Login_History.length > 0" 
                class="login-stats">
              <p><strong>Tổng số lần đăng nhập:</strong> {{ selectedLoginHistory.Login_History.length }}</p>
              <p><strong>Lần đăng nhập đầu tiên:</strong> {{ formatDate(selectedLoginHistory.Login_History[0]) }}</p>
              <p><strong>Lần đăng nhập gần nhất:</strong> {{ formatDate(selectedLoginHistory.Login_History[selectedLoginHistory.Login_History.length - 1]) }}</p>
              <p v-if="countLoginToday(selectedLoginHistory.Login_History) > 0">
                <strong>Số lần đăng nhập hôm nay:</strong> {{ countLoginToday(selectedLoginHistory.Login_History) }}
              </p>
            </div>
          </div>
          
          <div class="custom-btn-group">
            <button @click="showLoginHistoryModal = false" class="custom-btn custom-btn-save">Đóng</button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { format, isToday, startOfDay, parseISO } from 'date-fns';
import axios from "axios";

// Biến cho hiển thị lịch sử đăng nhập
const showLoginHistoryModal = ref(false);
const selectedLoginHistory = ref(null);
const theHoiVienList = ref([]);
const isLoading = ref(true);
const errorMessage = ref("");
const editingItem = ref(null);
const searchQuery = ref("");
const filterStatus = ref(""); // Lọc theo còn hạn hay hết hạn
const showUpdateSuccess = ref(false); // Điều khiển modal thông báo cập nhật

// Add pagination logic
const currentPage = ref(1);
const itemsPerPage = 5;

const showConfirmDelete = ref(false); // Điều khiển hiển thị modal xác nhận xóa
const selectedTheHoiVien = ref(null); // Lưu thẻ hội viên đang chọn để xóa

// Kiểm tra xem thẻ có được tạo ngày hôm nay không
const isCreatedToday = (dateString) => {
  if (!dateString) return false;
  try {
    // Sử dụng hàm isToday từ date-fns để kiểm tra
    return isToday(new Date(dateString));
  } catch (error) {
    console.error("Lỗi kiểm tra ngày tạo:", error);
    return false;
  }
};

// Kiểm tra xem có đăng nhập hôm nay không
const isLoginToday = (dateString) => {
  if (!dateString) return false;
  try {
    return isToday(new Date(dateString));
  } catch (error) {
    console.error("Lỗi kiểm tra ngày đăng nhập:", error);
    return false;
  }
};

// Kiểm tra xem thẻ có đăng nhập hôm nay không
const hasLoginToday = (loginHistory) => {
  if (!loginHistory || !Array.isArray(loginHistory) || loginHistory.length === 0) return false;
  return loginHistory.some(date => isLoginToday(date));
};

// Đếm số lần đăng nhập hôm nay
const countLoginToday = (loginHistory) => {
  if (!loginHistory || !Array.isArray(loginHistory) || loginHistory.length === 0) return 0;
  return loginHistory.filter(date => isLoginToday(date)).length;
};

const paginatedTheHoiVienList = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredTheHoiVienList.value.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(filteredTheHoiVienList.value.length / itemsPerPage);
});

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

// Định dạng ngày
const formatDate = (dateString) => {
  if (!dateString) return "Chưa cập nhật";
  try {
    return format(new Date(dateString), "dd/MM/yyyy HH:mm:ss"); // Ngày/Tháng/Năm Giờ:Phút:Giây
  } catch (error) {
    console.error("Lỗi định dạng ngày:", error);
    return "Không hợp lệ";
  }
};

// Định dạng lịch sử đăng nhập
const formatLoginHistory = (loginHistory) => {
  if (!loginHistory || loginHistory.length === 0) return "Chưa có đăng nhập";
  
  // Lấy 3 lần đăng nhập gần nhất
  const recentLogins = Array.isArray(loginHistory) 
    ? loginHistory.slice(-3) 
    : [loginHistory];
  
  return recentLogins.map(date => formatDate(date)).join(", ");
};

// Hiển thị modal lịch sử đăng nhập
const showLoginHistory = (item) => {
  selectedLoginHistory.value = item;
  showLoginHistoryModal.value = true;
};

// Định dạng dịch vụ
const formatDichVu = (DichVu) => {
  if (!DichVu) return "Không có dịch vụ"; 
  if (typeof DichVu === "string") return DichVu; 
  if (Array.isArray(DichVu)) return DichVu.join(", ");
  return "Không có dịch vụ"; 
};

// Lấy danh sách thẻ hội viên
const fetchTheHoiVien = async () => {
  try {
    isLoading.value = true;
    errorMessage.value = "";
    const response = await axios.get("http://localhost:5000/thehoivien/");
    
    // Đảm bảo `dichVu` luôn là mảng
    theHoiVienList.value = response.data.map(item => ({
      ...item,
      DichVu: Array.isArray(item.DichVu) ? item.DichVu : (item.DichVu ? [item.DichVu] : []),
      Login_History: Array.isArray(item.Login_History) ? item.Login_History : 
                (item.Login_History ? [item.Login_History] : 
                (item.Last_Login_Date ? [item.Last_Login_Date] : []))
    }));
  } catch (error) {
    console.error("Lỗi khi lấy dữ liệu:", error);
    errorMessage.value = "Không thể tải dữ liệu!";
    theHoiVienList.value = [];
  } finally {
    isLoading.value = false;
  }
};

const filteredTheHoiVienList = computed(() => {
  const today = new Date();

  return theHoiVienList.value.filter((item) => {
    // Search check - make sure HoiVien exists before trying to search
    let matchesSearch = true;
    if (searchQuery.value.trim() !== "") {
      // Only apply search filter if there's actually a search query
      matchesSearch = item.HoiVien && 
                      item.HoiVien.toLowerCase().includes(searchQuery.value.toLowerCase());
    }

    // Status check (expired/valid/today)
    let isExpired = false;
    if (item.NgayHetHan) {
      const expirationDate = new Date(item.NgayHetHan);
      isExpired = expirationDate < today;
    }

    // Kiểm tra xem thẻ có được tạo hôm nay không
    const createdToday = isCreatedToday(item.NgayTao);
    
    // Kiểm tra xem có đăng nhập hôm nay không
    const loginToday = hasLoginToday(item.Login_History);

    const matchesStatus =
      filterStatus.value === "valid" ? !isExpired : 
      filterStatus.value === "expired" ? isExpired : 
      filterStatus.value === "today" ? createdToday :
      filterStatus.value === "login_today" ? loginToday :
      true; // If nothing is selected, show all

    // Item must match both search and status filters
    return matchesSearch && matchesStatus;
  });
});

// Chỉnh sửa thẻ hội viên
const editItem = (item) => {
  editingItem.value = { 
    ...item,
    DichVu: Array.isArray(item.DichVu) ? item.DichVu.join(", ") : item.DichVu
  };
};

// Hủy chỉnh sửa
const cancelEdit = () => {
  editingItem.value = null;
};

const isExpired = (NgayHetHan) => {
  if (!NgayHetHan) return false;
  const expirationDate = new Date(NgayHetHan);
  const today = new Date();
  return expirationDate < today;
};

// Cập nhật thẻ hội viên
const updateItem = async () => {
  if (!editingItem.value) return;

  try {
    // Chuyển dịch vụ thành mảng
    editingItem.value.DichVu = typeof editingItem.value.DichVu === "string"
      ? editingItem.value.DichVu.split(",").map(item => item.trim())
      : editingItem.value.DichVu;

    // Định dạng ngày hết hạn
    const expirationDate = new Date(editingItem.value.NgayHetHan);
    editingItem.value.NgayHetHan = expirationDate.toISOString().split("T")[0];

    // Cập nhật số ngày còn lại
    const timeDiff = expirationDate.getTime() - new Date().getTime();
    editingItem.value.SoNgayConLai = Math.max(Math.ceil(timeDiff / (1000 * 60 * 60 * 24)), 0);

    // Gửi yêu cầu cập nhật
    await axios.put(`http://localhost:5000/thehoivien/${editingItem.value._id}`, editingItem.value);
    
    // Hiển thị modal thông báo
    showUpdateSuccess.value = true;
    fetchTheHoiVien();
    editingItem.value = null;
  } catch (error) {
    console.error("Lỗi khi cập nhật:", error);
    alert("Cập nhật thất bại!");
  }
};

const closeUpdateModal = () => {
  showUpdateSuccess.value = false;
};

// Xóa thẻ hội viên
const confirmDeleteItem = (item) => {
  selectedTheHoiVien.value = item; // Gán thẻ hội viên được chọn
  showConfirmDelete.value = true;   // Hiện modal xác nhận xóa
};

const deleteItem = async () => {
  if (!selectedTheHoiVien.value) return;

  try {
    await axios.delete(`http://localhost:5000/thehoivien/${selectedTheHoiVien.value._id}`);
    fetchTheHoiVien(); // Cập nhật lại danh sách sau khi xóa
    showConfirmDelete.value = false;
    selectedTheHoiVien.value = null;
  } catch (error) {
    console.error("Lỗi khi xóa:", error);
    alert("Xóa thất bại!");
  }
};

onMounted(fetchTheHoiVien);
</script>

<style>
/* CSS cho nút xem chi tiết */
.custom-btn-info {
  background-color: #3498db;
  color: white;
  padding: 2px 8px;
  font-size: 0.8rem;
  margin-left: 5px;
}

.custom-btn-info:hover {
  background-color: #2980b9;
}

.btn-sm {
  padding: 3px 8px;
  font-size: 0.75rem;
}

/* CSS cho danh sách lịch sử đăng nhập */
.login-history-list {
  max-height: 300px;
  overflow-y: auto;
  margin: 15px 0;
  border: 1px solid #eee;
  border-radius: 5px;
  padding: 10px;
}

.login-history-list ul {
  list-style-type: none;
  padding: 0;
  margin-bottom: 15px;
}

.login-history-list li {
  padding: 8px;
  border-bottom: 1px solid #eee;
  font-size: 0.95rem;
}

.login-history-list li:last-child {
  border-bottom: none;
}

.no-history {
  text-align: center;
  color: #7f8c8d;
  padding: 20px;
}

/* CSS cho phần thống kê */
.login-stats {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px dashed #ccc;
}

.login-stats p {
  margin: 5px 0;
  font-size: 0.95rem;
}
/* ======= Tổng quát ======= */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Arial', sans-serif;
  background-color: #f4f4f4;
  color: #333;
  line-height: 1.6;
}

/* ======= Container chính ======= */
.custom-container {
  max-width: 1200px;
  margin: auto;
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  margin-top: 60px;
}

/* ======= Tiêu đề ======= */
.custom-title {
  font-size: 1.8rem;
  text-align: center;
  margin-bottom: 20px;
  color: #2c3e50;
}

/* ======= Thanh tìm kiếm ======= */
.custom-search {
  display: flex;
  justify-content: flex-start; /* Canh các mục về bên trái */
  align-items: center;
  gap: 10px; /* Khoảng cách giữa các mục */
  max-width: 600px; /* Giới hạn chiều ngang tối đa */
  margin-bottom: 20px;
  margin-left: auto;
  margin-right: auto; /* Căn giữa thanh tìm kiếm */
}

/* Ô input tìm kiếm */
.custom-input {
  flex: 1; /* Tự điều chỉnh kích thước nhưng không vượt quá max-width */
  min-width: 200px;
  padding: 8px;
  font-size: 0.9rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.custom-input:focus {
  border-color: #3498db;
  outline: none;
}

/* ======= Nút ======= */
.custom-btn {
  padding: 10px 20px;
  margin: 5px;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
  color: white;
}

.custom-btn-add {
  background-color: #27ae60;
  margin-bottom: 20px;
}

.custom-btn-add:hover {
  background-color: #219150;
}

.custom-btn-edit {
  background-color: #f39c12;
}

.custom-btn-edit:hover {
  background-color: #e08e0b;
}

.custom-btn-delete {
  background-color: #c0392b;
}

.custom-btn-delete:hover {
  background-color: #a93226;
}

.custom-btn-save {
  background-color: #2980b9;
}

.custom-btn-save:hover {
  background-color: #2471a3;
}

.custom-btn-cancel {
  background-color: #7f8c8d;
}

.custom-btn-cancel:hover {
  background-color: #707b7c;
}

/* ======= Bảng ======= */
.custom-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.custom-table th,
.custom-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
  font-size: 1rem;
}

.custom-table th {
  background-color: #34495e;
  color: white;
}

.custom-table tr:hover {
  background-color: #f5f5f5;
}

.custom-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

/* ======= Modal ======= */
.custom-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  z-index: 1000;
}

/* Giới hạn chiều cao form */
.custom-modal-content {
  background: white;
  padding: 25px;
  border-radius: 8px;
  width: 100%;
  max-width: 400px; /* Chiều ngang form */
  max-height: 80vh; /* Giới hạn chiều cao */
  overflow-y: auto; /* Cuộn nếu nội dung quá dài */
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  animation: fadeIn 0.3s ease;
}

/* Tiêu đề */
.custom-modal-content h2 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  text-align: center;
  color: #2c3e50;
}

/* ======= Form ======= */
.custom-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-group label {
  font-weight: bold;
  font-size: 0.9rem;
  color: #34495e;
  text-align: left;
}

.custom-input {
  padding: 8px;
  font-size: 0.9rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Nút */
.custom-btn-group {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 15px;
}

.custom-btn {
  padding: 8px 15px;
  font-size: 0.9rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  color: white;
}

.custom-btn-save {
  background-color: #2980b9;
}

.custom-btn-cancel {
  background-color: #7f8c8d;
}

.custom-btn:hover {
  opacity: 0.9;
}

/* ======= Animation ======= */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ======= Responsive ======= */
@media (max-width: 768px) {
  .custom-modal-content {
    max-width: 90%;
    max-height: 85vh;
  }

  .custom-btn-group {
    flex-direction: column;
    gap: 10px;
  }

  .custom-btn {
    width: 100%;
    text-align: center;
  }
}

.expired {
  background-color: #ffcccc !important; /* Màu đỏ nhạt */
  color: red;
  font-weight: bold;
}

/* CSS cho thẻ được tạo hôm nay */
.today-created {
  background-color: #e8f7ff !important; /* Màu xanh nhạt */
  font-weight: bold;
}


/* CSS cho trạng thái đăng nhập hôm nay */
.login-today {
  background-color: #e0ffea !important; /* Màu xanh lá nhạt */
  font-weight: bold;
}

/* CSS cho item đăng nhập hôm nay trong danh sách */
.login-today-item {
  background-color: #e0ffea;
  font-weight: bold;
}

/* CSS cho badge "Hôm nay" */
.today-badge {
  background-color: #28a745;
  color: white;
  font-size: 0.75rem;
  padding: 2px 6px;
  border-radius: 10px;
  margin-left: 5px;
}

/* Cải thiện responsive cho bảng */
@media (max-width: 768px) {
  .custom-table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
  }
  
  .custom-table th, 
  .custom-table td {
    padding: 8px;
    font-size: 0.9rem;
  }
}
</style>