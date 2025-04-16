<template>
  <div class="custom-container">
    <h1 class="custom-title">Quản lý Dịch Vụ</h1>

    <!-- Thanh tìm kiếm -->
    <div class="custom-search">
      <input v-model="searchQuery" placeholder="Tìm kiếm dịch vụ..." class="custom-input" />
    </div>

    <!-- Nút thêm mới -->
    <button @click="openModal()" class="custom-btn custom-btn-add">Thêm Dịch Vụ</button>

    <!-- Loading spinner -->
    <div v-if="loading" class="loading-spinner">Đang tải dữ liệu...</div>

    <!-- Bảng dữ liệu -->
   <!-- Bảng dữ liệu -->
<table v-if="!loading" class="custom-table">
  <thead>
    <tr>
      <th>Mã DV</th>
      <th>Tên Dịch Vụ</th>
      <th>Mô Tả</th>

      <!-- Thêm dropdown lọc ngay trong cột Giá -->
      <th>
        Giá
        <select v-model="selectedPriceRange" class="table-filter">
          <option value="">Tất cả</option>
          <option value="0-500000">Dưới 500,000 VND</option>
          <option value="500000-1000000">500,000 - 1,000,000 VND</option>
          <option value="1000000-3000000">1,000,000 - 3,000,000 VND</option>
          <option value="3000000">Trên 3,000,000 VND</option>
        </select>
      </th>

      <th>Trạng Thái</th>
      <th>Hành Động</th>
    </tr>
  </thead>

  <tbody>
    <tr v-for="dv in paginatedDichVus" :key="dv._id">
      <td>{{ dv.MaDV || "N/A" }}</td>
      <td>{{ dv.TenDichVu || "Chưa có dữ liệu" }}</td>
      <td>{{ dv.MoTa || "Không xác định" }}</td>
      <td>{{ formatCurrency(dv.Gia) }}</td>
      <td>{{ dv.TrangThai || "Không xác định" }}</td>
      <td>
        <button @click="openModal(dv)" class="custom-btn custom-btn-edit">Sửa</button>
        <button @click="confirmDelete(dv)" class="custom-btn custom-btn-delete">Xóa</button>
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

    <!-- Modal thêm/sửa -->
    <transition name="fade">
      <div v-if="showModal" class="custom-modal">
        <div class="custom-modal-content">
          <h2>{{ editingDichVu ? "Chỉnh sửa Dịch Vụ" : "Thêm Dịch Vụ" }}</h2>

          <form @submit.prevent="saveDichVu" class="custom-form">
            <div class="form-group">
              <label for="TenDichVu">Tên Dịch Vụ:</label>
              <input id="TenDichVu" v-model="form.TenDichVu" placeholder="Nhập tên dịch vụ" class="custom-input" required />
            </div>

            <div class="form-group">
              <label for="MoTa">Mô Tả:</label>
              <textarea id="MoTa" v-model="form.MoTa" placeholder="Nhập mô tả" class="custom-input"></textarea>
            </div>

            <div class="form-group">
              <label for="Gia">Giá:</label>
              <input id="Gia" v-model.number="form.Gia" type="number" placeholder="Nhập giá" class="custom-input" required />
            </div>

            <div class="form-group">
              <label for="TrangThai">Trạng Thái:</label>
              <select id="TrangThai" v-model="form.TrangThai" class="custom-input">
                <option value="Hoạt động">Hoạt động</option>
                <option value="Ngừng hoạt động">Ngừng hoạt động</option>
              </select>
            </div>

            <div class="custom-btn-group">
              <button type="submit" class="custom-btn custom-btn-save">Lưu</button>
              <button type="button" @click="closeModal" class="custom-btn custom-btn-cancel">Hủy</button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- Modal xác nhận xóa -->
    <transition name="fade">
      <div v-if="showConfirmDelete" class="custom-modal">
        <div class="custom-modal-content">
          <h2>Xác nhận xóa</h2>
          <p>Bạn có chắc muốn xóa dịch vụ <strong>{{ selectedDichVu?.TenDichVu }}</strong> không?</p>
          <div class="custom-btn-group">
            <button @click="deleteDichVu" class="custom-btn custom-btn-delete">Xóa</button>
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
      selectedPriceRange: "",
      dichVus: [],
      searchQuery: "",
      showModal: false,
      showConfirmDelete: false,
      selectedDichVu: null,
      editingDichVu: null,
      loading: false,
      currentPage: 1,
      itemsPerPage: 5,
      form: {
        TenDichVu: "",
        MoTa: "",
        Gia: null,
        TrangThai: "Hoạt động",
      },
    };
  },
  
  computed: {
   filteredDichVus() {
  return this.dichVus
    .filter((dv) => dv.TenDichVu?.toLowerCase().includes(this.searchQuery.toLowerCase()))
    .filter((dv) => {
      if (!this.selectedPriceRange) return true;
      const price = dv.Gia || 0;
      const [min, max] = this.selectedPriceRange.split("-").map(Number);
      return max ? price >= min && price <= max : price >= min;
    });
},

    paginatedDichVus() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredDichVus.slice(start, start + this.itemsPerPage);
    },
    totalPages() {
      return Math.ceil(this.filteredDichVus.length / this.itemsPerPage);
    },
  },
  methods: {
    async fetchDichVus() {
  try {
    this.loading = true;
    const { data } = await axios.get("http://localhost:5000/dichvu/");
    this.dichVus = data.map((dv) => ({ ...dv, _id: String(dv._id) }));
  } catch (err) {
    alert("Không thể tải dữ liệu dịch vụ. Vui lòng thử lại!");
    console.error("Lỗi khi tải danh sách dịch vụ:", err.message);
  } finally {
    this.loading = false;
  }
},

    openModal(dv = null) {
      this.editingDichVu = dv;
      this.form = dv ? { ...dv } : { TenDichVu: "", MoTa: "", Gia: null, TrangThai: "Hoạt động" };
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.editingDichVu = null;
    },
    async saveDichVu() {
      try {
        const url = "http://localhost:5000/dichvu/";
        const payload = { ...this.form };
        delete payload._id;

        if (this.editingDichVu) {
          await axios.put(`${url}${this.editingDichVu._id}`, payload);
        } else {
          await axios.post(url, payload);
        }

        this.closeModal();
        this.fetchDichVus();
      } catch (err) {
        console.error("Lỗi khi lưu dịch vụ:", err.message);
      }
    },
    confirmDelete(dv) {
      this.selectedDichVu = dv;
      this.showConfirmDelete = true;
    },
    async deleteDichVu() {
      try {
        await axios.delete(`http://localhost:5000/dichvu/${this.selectedDichVu._id}`);
        this.showConfirmDelete = false;
        this.fetchDichVus();
      } catch (err) {
        console.error("Lỗi khi xóa dịch vụ:", err.message);
      }
    },
    formatCurrency(amount) {
      return amount ? `${amount.toLocaleString()} VND` : "Không xác định";
    },
    prevPage() {
      if (this.currentPage > 1) this.currentPage--;
    },
    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },
  },
  mounted() {
    this.fetchDichVus();
  },
};
</script>


<style>

.table-filter {
  padding: 5px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* === Animation === */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter, 
.fade-leave-to {
  opacity: 0;
}

/* === Container === */
.custom-container {
  max-width: 1200px;
  margin: 50px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

/* === Buttons === */
.custom-btn {
  padding: 10px 20px;
  margin: 5px;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.custom-btn-add { background: #27ae60; }
.custom-btn-edit { background: #f39c12; }
.custom-btn-delete { background: #c0392b; }
.custom-btn-save { background: #2980b9; }
.custom-btn-cancel { background: #7f8c8d; }

/* === Table === */
.custom-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}
.custom-table th, .custom-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}
.custom-table th {
  background-color: #34495e;
  color: white;
}
.custom-table tr:hover {
  background-color: #f5f5f5;
}

/* ======= Phân trang ======= */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
}

.pagination button {
  padding: 8px 15px;
  font-size: 1rem;
  border: 1px solid #3498db;
  border-radius: 5px;
  background-color: white;
  color: #3498db;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pagination button:disabled {
  border-color: #bdc3c7;
  color: #bdc3c7;
  cursor: not-allowed;
  background-color: #ecf0f1;
}

.pagination button:hover:not(:disabled) {
  background-color: #3498db;
  color: white;
}

.pagination span {
  font-size: 1rem;
  font-weight: bold;
  color: #2c3e50;
}

</style>
