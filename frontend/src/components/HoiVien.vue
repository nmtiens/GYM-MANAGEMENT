<template>
  <div class="custom-container">
    <h1 class="custom-title">Quản lý Hội Viên</h1>

    <!-- Thanh tìm kiếm -->
    <div class="custom-search">
      <input v-model="searchQuery" placeholder="Tìm kiếm Hội Viên..." class="custom-input" />
    </div>

    <!-- Bảng dữ liệu -->
    <table class="custom-table">
      <thead>
        <tr>
          <th>Mã Hội Viên</th>
        <th @click="sortByName" style="cursor: pointer;">
  Họ Tên
  <span v-if="sortOrder === 'asc'">▲</span>
  <span v-else>▼</span>
</th>
          <th>Địa Chỉ</th>
          <th>Ngày Sinh</th>
          <th>Email</th>
          <th>Số Điện Thoại</th>
          <th>Hành Động</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="hv in paginatedHoiViens" :key="hv._id">
          <td>{{ hv.MaHoiVien || "Chưa có dữ liệu" }}</td>
          <td>{{ hv.HoTen || "Không xác định" }}</td>
          <td>{{ hv.DiaChi || "Không xác định" }}</td>
          <td>{{ formatDate(hv.NgaySinh) }}</td>
          <td>{{ hv.Email || "Không xác định" }}</td>
          <td>{{ hv.SDT || "Không xác định" }}</td>
          <td>
            <button @click="openModal(hv)" class="custom-btn custom-btn-edit">Sửa</button>
            <button @click="confirmDelete(hv)" class="custom-btn custom-btn-delete">Xóa</button>
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

    <!-- Modal Thêm/Sửa -->
    <transition name="fade">
      <div v-if="showModal" class="custom-modal">
        <div class="custom-modal-content">
          <h2 class="custom-title">
            {{ editingHoiVien ? "Chỉnh sửa Hội Viên" : "Thêm Hội Viên" }}
          </h2>

          <form @submit.prevent="saveHoiVien" class="custom-form">
            <div class="form-group">
              <label for="HoTen">Họ Tên:</label>
              <input id="HoTen" v-model="form.HoTen" placeholder="Nhập họ tên" class="custom-input" required />
            </div>

             <div class="form-group">
              <label for="DiaChi">Địa Chỉ:</label>
              <input id="DiaChi" v-model="form.DiaChi" placeholder="Nhập địa chỉ" class="custom-input" />
            </div>

            <div class="form-group">
              <label for="NgaySinh">Ngày Sinh:</label>
              <input id="NgaySinh" v-model="form.NgaySinh" type="date" class="custom-input" />
            </div>

            <div class="form-group">
              <label for="Email">Email:</label>
              <input id="Email" v-model="form.Email" type="email" placeholder="Nhập email" class="custom-input" />
            </div>

            <div class="form-group">
              <label for="SDT">Số Điện Thoại:</label>
              <input id="SDT" v-model="form.SDT" placeholder="Nhập số điện thoại" class="custom-input" required />
            </div>

            <div class="custom-btn-group">
              <button type="submit" class="custom-btn custom-btn-save">Lưu</button>
              <button type="button" @click="closeModal" class="custom-btn custom-btn-cancel">Hủy</button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- Modal Xác Nhận Xóa -->
    <transition name="fade">
      <div v-if="showDeleteModal" class="delete-modal">
        <div class="delete-modal-content">
          <h2>Xác nhận xóa</h2>
          <p>Bạn có chắc chắn muốn xóa hội viên <strong>{{ deletingHoiVien?.HoTen }}</strong> không?</p>
          <div class="custom-btn-group">
            <button @click="deleteHoiVien(deletingHoiVien._id)" class="custom-btn custom-btn-delete">Xóa</button>
            <button @click="closeDeleteModal" class="custom-btn custom-btn-cancel">Hủy</button>
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
      hoiViens: [],
      searchQuery: "",
      showModal: false,
      showDeleteModal: false,
      editingHoiVien: null,
      deletingHoiVien: null,
      currentPage: 1,
      itemsPerPage: 5,
      sortOrder: 'asc', // Mặc định sắp xếp tăng dần
      form: {
        HoTen: "",
        DiaChi: "",
        NgaySinh: "",
        SDT: "",
        Email: "",
      },
    };
  },

  computed: {
    filteredHoiViens() {
      return this.hoiViens.filter((hv) =>
        hv.HoTen?.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    paginatedHoiViens() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredHoiViens.slice(start, start + this.itemsPerPage);
    },
    totalPages() {
      return Math.ceil(this.filteredHoiViens.length / this.itemsPerPage);
    },
  },

  methods: {
    async fetchHoiViens() {
      try {
        const res = await axios.get("http://localhost:5000/");
        this.hoiViens = res.data.map((hv) => ({
          ...hv,
          _id: String(hv._id),
        }));
      } catch (error) {
        alert("Lỗi khi tải danh sách hội viên!");
      }
    },
     sortByName() {
    this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
    this.hoiViens.sort((a, b) => {
      const nameA = a.HoTen ? a.HoTen.toLowerCase() : '';
      const nameB = b.HoTen ? b.HoTen.toLowerCase() : '';
      if (this.sortOrder === 'asc') {
        return nameA.localeCompare(nameB);
      } else {
        return nameB.localeCompare(nameA);
      }
    });
  },

    openModal(hv = null) {
      this.editingHoiVien = hv;
      this.form = hv
        ? { ...hv }
        : {
            HoTen: "",
            DiaChi: "",
            NgaySinh: "",
            SDT: "",
            Email: "",
          };
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
      this.editingHoiVien = null;
    },

    confirmDelete(hv) {
      this.deletingHoiVien = hv;
      this.showDeleteModal = true;
    },

    closeDeleteModal() {
      this.showDeleteModal = false;
      this.deletingHoiVien = null;
    },

    async saveHoiVien() {
      try {
        if (this.editingHoiVien) {
          await axios.put(`http://localhost:5000/${this.editingHoiVien._id}`, this.form);
        }
        this.closeModal();
        this.fetchHoiViens();
      } catch (error) {
        alert("Lỗi khi lưu hội viên!");
      }
    },

    async deleteHoiVien(id) {
      try {
        await axios.delete(`http://localhost:5000/${id}`);
        this.fetchHoiViens();
        this.closeDeleteModal();
      } catch (error) {
        alert("Không thể xóa hội viên.");
      }
    },

    prevPage() {
      if (this.currentPage > 1) this.currentPage--;
    },

    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },

    formatDate(dateString) {
      if (!dateString) return "Không có dữ liệu";
      const date = new Date(dateString);
      return isNaN(date) ? "Sai định dạng" : date.toLocaleDateString("vi-VN");
    },
  },

  mounted() {
    this.fetchHoiViens();
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