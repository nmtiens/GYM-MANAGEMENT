<template>
  <div class="custom-container">
    <h1 class="custom-title">Quản lý Huấn Luyện Viên</h1>

    <!-- Thanh tìm kiếm -->
    <div class="custom-search">
      <input v-model="searchQuery" placeholder="Tìm kiếm huấn luyện viên..." class="custom-input" />
    </div>

    <!-- Thêm mới -->
    <button @click="openModal(null)" class="custom-btn custom-btn-add">Thêm Huấn Luyện Viên</button>

    <!-- Loading & Thông báo lỗi -->
    <p v-if="isLoading" class="loading">Đang tải dữ liệu...</p>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <!-- Bảng dữ liệu -->
    <table v-if="!isLoading" class="custom-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Ảnh</th>
          <th>Họ Tên</th>
          <th>Ngày Sinh</th>
          <th>Giới Tính</th>
          <th>SDT</th>
          <th>Địa Chỉ</th>
          <th>Kinh Nghiệm</th>
          <th>Mô Tả</th>
          <th>Hành Động</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="hlv in paginatedHuanLuyenViens" :key="hlv._id">
          <td>{{ hlv.MaHLV }}</td>
          <td>
            <img :src="getImageUrl(hlv.Anh)" alt="Ảnh HLV" class="custom-avatar" />
          </td>
          <td>{{ hlv.HoTen || 'Chưa có dữ liệu' }}</td>
          <td>{{ formatDate(hlv.NgaySinh) }}</td>
          <td>{{ hlv.GioiTinh || 'Không xác định' }}</td>
          <td>{{ hlv.SDT || 'Không xác định' }}</td>
          <td>{{ hlv.DiaChi || 'Không xác định' }}</td>
          <td>{{ hlv.KinhNghiem || 'Không xác định' }}</td>
          <td>{{ hlv.MoTa || 'Không xác định' }}</td>
          <td>
            <button @click="openModal(hlv)" class="custom-btn custom-btn-edit">Sửa</button>
            <button @click="confirmDelete(hlv)" class="custom-btn custom-btn-delete">Xóa</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Phân trang -->
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">Trước</button>
      <span>Trang {{ currentPage }} / {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Sau</button>
    </div>

    <!-- Modal thêm/sửa huấn luyện viên -->
<transition name="fade">
  <div v-if="showModal" class="custom-modal">
    <div class="custom-modal-content">
      <h2>{{ editingHuanLuyenVien ? "Chỉnh sửa Huấn Luyện Viên" : "Thêm Huấn Luyện Viên" }}</h2>

      <form @submit.prevent="saveHuanLuyenVien" class="custom-form">
        <div class="form-group">
          <label for="HoTen">Họ Tên:</label>
          <input v-model="form.HoTen" id="HoTen" class="custom-input" required />
        </div>

        <div class="form-group">
          <label for="NgaySinh">Ngày Sinh:</label>
          <input type="date" v-model="form.NgaySinh" id="NgaySinh" class="custom-input" required />
        </div>

        <div class="form-group">
          <label for="GioiTinh">Giới Tính:</label>
          <select v-model="form.GioiTinh" id="GioiTinh" class="custom-input">
            <option value="Nam">Nam</option>
            <option value="Nữ">Nữ</option>
          </select>
        </div>

        <div class="form-group">
          <label for="SDT">Số Điện Thoại:</label>
          <input v-model="form.SDT" id="SDT" class="custom-input" />
        </div>

        <div class="form-group">
          <label for="DiaChi">Địa Chỉ:</label>
          <input v-model="form.DiaChi" id="DiaChi" class="custom-input" />
        </div>

        <div class="form-group">
          <label for="KinhNghiem">Kinh Nghiệm:</label>
          <input v-model="form.KinhNghiem" id="KinhNghiem" class="custom-input" />
        </div>

        <div class="form-group">
          <label for="MoTa">Mô Tả:</label>
          <textarea v-model="form.MoTa" id="MoTa" class="custom-input"></textarea>
        </div>

        <div class="form-group">
          <label for="Anh">Ảnh:</label>
          <input type="file" @change="handleFileUpload" multiple class="custom-input" />
        </div>

        <div class="custom-btn-group">
          <button type="submit" class="custom-btn custom-btn-save">Lưu</button>
          <button type="button" @click="closeModal" class="custom-btn custom-btn-cancel">Hủy</button>
        </div>
      </form>
    </div>
  </div>
</transition>

    <!-- Thông báo Xóa -->
    <transition name="fade">
      <div v-if="showConfirmDelete" class="custom-modal">
        <div class="custom-modal-content">
          <h2 class="modal-title">Xác nhận xóa</h2>
          <p>Bạn có chắc muốn xóa huấn luyện viên <strong>{{ selectedHuanLuyenVien?.HoTen }}</strong> không?</p>
          <div class="custom-btn-group">
            <button @click="deleteHuanLuyenVien" class="custom-btn custom-btn-delete">Xóa</button>
            <button @click="showConfirmDelete = false" class="custom-btn custom-btn-cancel">Hủy</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      huanLuyenViens: [],
      searchQuery: "",
      showModal: false,
      showConfirmDelete: false,
      isLoading: false,
      errorMessage: "",
      editingHuanLuyenVien: null,
      selectedHuanLuyenVien: null,
      currentPage: 1,
      pageSize: 5,
      form: {
        HoTen: "",
        NgaySinh: "",
        GioiTinh: "Nam",
        SDT: "",
        DiaChi: "",
        KinhNghiem: "",
        MoTa: "",
        Anh: [],
      },
    };
  },

  computed: {
    filteredHuanLuyenViens() {
      return this.huanLuyenViens.filter((hlv) =>
        hlv.HoTen?.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    totalPages() {
      return Math.ceil(this.filteredHuanLuyenViens.length / this.pageSize);
    },
    paginatedHuanLuyenViens() {
      const start = (this.currentPage - 1) * this.pageSize;
      return this.filteredHuanLuyenViens.slice(start, start + this.pageSize);
    },
  },

  methods: {
    // Fetch danh sách HLV
  async fetchHuanLuyenViens() {
  this.loading = true;
  this.error = null;
  try {
    const response = await axios.get('http://localhost:5000/huanluyenvien/');
    this.huanLuyenViens = response.data;
  } catch (error) {
    console.error('Lỗi chi tiết:', error);
    if (error.response) {
      // Lỗi từ server với status code
      this.error = `Lỗi server: ${error.response.status} - ${error.response.data}`;
    } else if (error.request) {
      // Lỗi không nhận được response
      this.error = 'Không thể kết nối đến server API. Vui lòng kiểm tra server có đang chạy không.';
    } else {
      // Lỗi khi thiết lập request
      this.error = `Lỗi: ${error.message}`;
    }
  } finally {
    this.loading = false;
  }
},

    // Mở modal (chỉnh sửa hoặc thêm mới)
    openModal(hlv = null) {
      this.editingHuanLuyenVien = hlv;
      this.form = hlv
        ? { ...hlv, Anh: [] }
        : {
            HoTen: "",
            NgaySinh: "",
            GioiTinh: "Nam",
            SDT: "",
            DiaChi: "",
            KinhNghiem: "",
            MoTa: "",
            Anh: [],
          };
      this.showModal = true;
    },

    // Đóng modal
    closeModal() {
      this.showModal = false;
      this.editingHuanLuyenVien = null;
    },

    // Xử lý upload file
    handleFileUpload(event) {
      this.form.Anh = Array.from(event.target.files);
    },

    // Lưu HLV (thêm hoặc cập nhật)
    async saveHuanLuyenVien() {
      try {
        const formData = new FormData();
        for (const key in this.form) {
          if (key === "Anh") {
            this.form.Anh.forEach((file) => formData.append("Anh", file));
          } else {
            formData.append(key, this.form[key]);
          }
        }

        // Gửi ảnh cũ (nếu có) khi chỉnh sửa
        if (this.editingHuanLuyenVien && this.editingHuanLuyenVien.Anh) {
          formData.append("OldAnh", JSON.stringify(this.editingHuanLuyenVien.Anh));
        }

        if (this.editingHuanLuyenVien) {
          await axios.put(
            `http://localhost:5000/huanluyenvien/${this.editingHuanLuyenVien._id}`,
            formData
          );
        } else {
          await axios.post("http://localhost:5000/huanluyenvien", formData);
        }

        this.closeModal();
        this.fetchHuanLuyenViens();
      } catch (error) {
        console.error("Lỗi khi lưu HLV:", error);
      }
    },

    // Mở modal xác nhận xóa
    confirmDelete(hlv) {
      this.selectedHuanLuyenVien = hlv;
      this.showConfirmDelete = true;
    },

    // Xóa HLV
    async deleteHuanLuyenVien() {
      try {
        if (!this.selectedHuanLuyenVien) return;

        await axios.delete(
          `http://localhost:5000/huanluyenvien/${this.selectedHuanLuyenVien._id}`
        );

        this.fetchHuanLuyenViens();
        this.showConfirmDelete = false;
        this.selectedHuanLuyenVien = null;
      } catch (error) {
        console.error("Lỗi khi xóa HLV:", error);
        this.errorMessage = "Không thể xóa huấn luyện viên. Vui lòng thử lại!";
      }
    },

    // Phân trang
    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },
    prevPage() {
      if (this.currentPage > 1) this.currentPage--;
    },

    // Định dạng ngày
    formatDate(dateString) {
      if (!dateString) return "Không có dữ liệu";
      const date = new Date(dateString);
      return !isNaN(date) ? date.toLocaleDateString("vi-VN") : "Sai định dạng";
    },

    // Hiển thị ảnh
    getImageUrl(Anh) {
      if (Array.isArray(Anh) && Anh.length > 0) return `http://localhost:5000${Anh[0]}`;
      if (typeof Anh === "string" && Anh) return `http://localhost:5000${Anh}`;
      return "path/to/default-avatar.png";
    },
  },

  mounted() {
    this.fetchHuanLuyenViens();
  },
};
</script>

<style>
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

</style>