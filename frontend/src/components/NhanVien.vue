<template>
  <div class="custom-container">
    <h1 class="custom-title">Quản lý Nhân Viên</h1>

    <!-- Thanh tìm kiếm -->
    <div class="custom-search">
      <input v-model="searchQuery" placeholder="Tìm kiếm nhân viên..." class="custom-input" />
    </div>

    <!-- Nút thêm mới -->
    <button @click="openModal(null)" class="custom-btn custom-btn-add">Thêm Nhân Viên</button>

    <!-- Bảng hiển thị dữ liệu -->
    <table class="custom-table">
      <thead>
        <tr>
          <th>Mã NV</th>
          <th>Họ Tên</th>
          <th>Ngày Sinh</th>
          <th>Giới Tính</th>
          <th>Số ĐT</th>
          <th>Địa Chỉ</th>
          <th>Chức Vụ</th>
          <th>Lương</th>
          <th>Hành Động</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="nv in filteredNhanViens" :key="nv.MaNV">
          <td>{{ nv.MaNV }}</td>
          <td>{{ nv.HoTen || 'Chưa có dữ liệu' }}</td>
          <td>{{ formatDate(nv.NgaySinh) }}</td>
          <td>{{ nv.GioiTinh || 'Không xác định' }}</td>
          <td>{{ nv.SDT || 'Không xác định' }}</td>
          <td>{{ nv.DiaChi || 'Không xác định' }}</td>
          <td>{{ nv.ChucVu || 'Không xác định' }}</td>
          <td>{{ nv.Luong || 'Không xác định' }}</td>
         <td>
  <button @click="openModal(nv)" class="custom-btn custom-btn-edit">Sửa</button>
  <button @click="openConfirmDelete(nv)" class="custom-btn custom-btn-delete">Xóa</button>
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
          <h2 class="modal-title">
            {{ editingNhanVien ? 'Chỉnh sửa Nhân Viên' : 'Thêm Nhân Viên' }}
          </h2>

          <!-- Form -->
          <form @submit.prevent="saveNhanVien" class="custom-form">
            <div class="form-group">
              <label for="HoTen">Họ Tên:</label>
              <input id="HoTen" v-model="form.HoTen" placeholder="Nhập họ tên" class="custom-input" required />
            </div>

            <div class="form-group">
              <label for="NgaySinh">Ngày Sinh:</label>
              <input id="NgaySinh" v-model="form.NgaySinh" type="date" class="custom-input" required />
            </div>

            <div class="form-group">
              <label for="GioiTinh">Giới Tính:</label>
              <select id="GioiTinh" v-model="form.GioiTinh" class="custom-input">
                <option value="Nam">Nam</option>
                <option value="Nữ">Nữ</option>
              </select>
            </div>

            <div class="form-group">
              <label for="SDT">Số Điện Thoại:</label>
              <input id="SDT" v-model="form.SDT" placeholder="Nhập số điện thoại" class="custom-input" required />
            </div>

            <div class="form-group">
              <label for="DiaChi">Địa Chỉ:</label>
              <input id="DiaChi" v-model="form.DiaChi" placeholder="Nhập địa chỉ" class="custom-input" />
            </div>

            <div class="form-group">
              <label for="Luong">Lương:</label>
              <input id="Luong" v-model="form.Luong" placeholder="Nhập lương" class="custom-input" />
            </div>

            <div class="form-group">
              <label for="ChucVu">Chức Vụ:</label>
              <input id="ChucVu" v-model="form.ChucVu" placeholder="Nhập chức vụ" class="custom-input" />
            </div>

            <!-- Nút hành động -->
            <div class="custom-btn-group">
              <button type="submit" class="custom-btn custom-btn-save">Lưu</button>
              <button type="button" @click="closeModal" class="custom-btn custom-btn-cancel">Hủy</button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- Modal xác nhận xóa Nhân Viên -->
<transition name="fade">
  <div v-if="showConfirmDelete" class="custom-modal">
    <div class="custom-modal-content">
      <h2 class="modal-title">Xác nhận xóa</h2>
      <p>Bạn có chắc muốn xóa nhân viên <strong>{{ selectedNhanVien?.HoTen }}</strong> không?</p>
      <div class="custom-btn-group">
        <button @click="deleteNhanVien" class="custom-btn custom-btn-delete">Xóa</button>
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
    nhanViens: [],
    searchQuery: "",
    showModal: false,
    editingNhanVien: null,
    form: { HoTen: "", NgaySinh: "", GioiTinh: "Nam", SDT: "", DiaChi: "", ChucVu: "", Luong: "" },
    currentPage: 1,
    pageSize: 5, // Số nhân viên hiển thị trên mỗi trang
     showConfirmDelete: false,
    selectedNhanVien: null,
  };
  },
 computed: {
  filteredNhanViens() {
    const search = this.searchQuery.toLowerCase();
    return this.nhanViens
      .filter((nv) => nv.HoTen?.toLowerCase().includes(search))
      .slice(this.startIndex, this.endIndex);
  },
  totalPages() {
    return Math.ceil(
      this.nhanViens.filter((nv) =>
        nv.HoTen?.toLowerCase().includes(this.searchQuery.toLowerCase())
      ).length / this.pageSize
    );
  },
  startIndex() {
    return (this.currentPage - 1) * this.pageSize;
  },
  endIndex() {
    return this.startIndex + this.pageSize;
  },
},

  methods: {
    async fetchNhanViens() {
      try {
        const res = await axios.get("http://localhost:5000/nhanvien");
        this.nhanViens = res.data.map((nv) => ({
          ...nv,
          _id: String(nv._id), // Chuyển ObjectId thành chuỗi
        }));
      } catch (error) {
        console.error("Lỗi khi tải danh sách nhân viên:", error);
      }
    },
    openModal(nv) {
      this.editingNhanVien = nv;
      this.form = nv
        ? { ...nv }
        : { HoTen: "", NgaySinh: "", GioiTinh: "Nam", SDT: "", DiaChi: "", ChucVu: "", Luong: "" };
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.editingNhanVien = null;
    },
    async saveNhanVien() {
      try {
        let updatedData = { ...this.form };
        delete updatedData._id; // Xóa _id để tránh lỗi MongoDB

        if (this.editingNhanVien) {
          await axios.put(
            `http://localhost:5000/nhanvien/${this.editingNhanVien._id}`,
            updatedData
          );
        } else {
          await axios.post("http://localhost:5000/nhanvien/", this.form);
        }

        this.closeModal();
        this.fetchNhanViens();
      } catch (error) {
        console.error("Lỗi khi lưu nhân viên:", error);
      }
    },
    openConfirmDelete(nv) {
    this.selectedNhanVien = nv;
    this.showConfirmDelete = true;
  },
  async deleteNhanVien() {
    if (!this.selectedNhanVien) return;

    try {
      await axios.delete(`http://localhost:5000/nhanvien/${this.selectedNhanVien._id}`);
      this.fetchNhanViens(); // Load lại danh sách sau khi xóa
      this.showConfirmDelete = false;
      this.selectedNhanVien = null;
    } catch (error) {
      console.error("Lỗi khi xóa nhân viên:", error);
    }
  },
     nextPage() {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
    }
  },
  prevPage() {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  },
  goToPage(page) {
    this.currentPage = page;
  },  

    formatDate(dateString) {
      if (!dateString) return "Không có dữ liệu";
      const date = new Date(dateString);
      return isNaN(date) ? "Sai định dạng" : date.toISOString().split("T")[0];
    },
  },

  
  mounted() {
    this.fetchNhanViens();
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


.custom-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.custom-modal-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
  text-align: center;
  animation: fadeIn 0.3s ease;
}

.modal-title {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #2c3e50;
}

.custom-btn-group {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}

.custom-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  color: white;
  font-size: 1rem;
}

.custom-btn-delete {
  background-color: #c0392b;
}

.custom-btn-cancel {
  background-color: #7f8c8d;
}

.custom-btn-delete:hover {
  background-color: #a93226;
}

.custom-btn-cancel:hover {
  background-color: #5d6d7e;
}

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

</style>