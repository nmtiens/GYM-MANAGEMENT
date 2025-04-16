<template>
  <div class="custom-container">
    <h1 class="custom-title">Quản lý Gói Tập</h1>

    <!-- Thanh tìm kiếm -->
    <div class="custom-search">
      <input v-model="searchQuery" placeholder="Tìm kiếm gói tập..." class="custom-input" />
    </div>

    <!-- Nút thêm mới -->
    <button @click="openModal(null)" class="custom-btn custom-btn-add">Thêm Gói Tập</button>

    <!-- Loading -->
    <div v-if="loading" class="loading-spinner">Đang tải dữ liệu...</div>

    <!-- Bảng dữ liệu -->
    <table v-else class="custom-table">
      <thead>
        <tr>
          <th>Mã Gói</th>
          <th>Tên Gói Tập</th>
          <th>Mô Tả</th>
          <th>
            Giá
            <select v-model="priceFilter" @change="applyPriceFilter" class="price-filter">
              <option value="">Tất cả</option>
              <option value="under500k">Dưới 500k</option>
              <option value="500k-1m">500k - 1 triệu</option>
              <option value="1m-2m">1 triệu - 2 triệu</option>
              <option value="over2m">Trên 2 triệu</option>
            </select>
          </th>
          <th>Quyền Lợi</th>
          <th>Hành Động</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="gt in paginatedGoiTaps" :key="gt._id">
          <td>{{ gt.MaGT || "N/A" }}</td>
          <td>{{ gt.TenGoiTap || "Chưa có dữ liệu" }}</td>
          <td>{{ gt.MoTa || "Không xác định" }}</td>
          <td>{{ formatCurrency(gt.Gia) }}</td>
          <td>
            <ul class="benefits-list">
              <li v-for="(quyenLoi, index) in gt.QuyenLoi" :key="index">
                {{ quyenLoi }}
              </li>
            </ul>
          </td>
          <td>
            <button @click="openModal(gt)" class="custom-btn custom-btn-edit">Sửa</button>
            <button @click="confirmDelete(gt)" class="custom-btn custom-btn-delete">Xóa</button>
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
            {{ editingGoiTap ? "Chỉnh sửa Gói Tập" : "Thêm Gói Tập" }}
          </h2>

          <form @submit.prevent="saveGoiTap" class="custom-form">
            <div class="form-group">
              <label for="TenGoiTap">Tên Gói Tập:</label>
              <input id="TenGoiTap" v-model="form.TenGoiTap" placeholder="Nhập tên gói tập" class="custom-input" required />
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
              <label for="QuyenLoi">Quyền Lợi (mỗi quyền lợi một dòng):</label>
              <textarea 
                id="QuyenLoi" 
                v-model="form.QuyenLoi" 
                placeholder="Nhập quyền lợi, mỗi quyền lợi một dòng" 
                class="custom-input"
                rows="3"
              ></textarea>
            </div>

            <div class="custom-btn-group">
              <button type="submit" class="custom-btn custom-btn-save" :disabled="loading">
                {{ loading ? "Đang lưu..." : "Lưu" }}
              </button>
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
          <p>Bạn có chắc chắn muốn xóa gói tập <strong>{{ deletingGoiTap?.TenGoiTap }}</strong> không?</p>
          <div class="custom-btn-group">
            <button @click="deleteGoiTap(deletingGoiTap._id)" class="custom-btn custom-btn-delete">Xóa</button>
            <button @click="closeDeleteModal" class="custom-btn custom-btn-cancel">Hủy</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from "axios";
import _ from "lodash";

export default {
  data() {
    return {
      priceFilter: "",
      goiTaps: [],
      searchQuery: "",
      showModal: false,
      showDeleteModal: false,
      loading: false,
      editingGoiTap: null,
      deletingGoiTap: null,
      currentPage: 1,
      itemsPerPage: 5,
      form: { 
        TenGoiTap: "", 
        MoTa: "", 
        Gia: null, 
        QuyenLoi: "" 
      },
    };
  },

  computed: {
    filteredGoiTaps() {
      return this.goiTaps.filter((gt) => {
        const matchesSearch = gt.TenGoiTap?.toLowerCase().includes(this.searchQuery.toLowerCase());

        let matchesPrice = true;
        if (this.priceFilter === "under500k") {
          matchesPrice = gt.Gia < 500000;
        } else if (this.priceFilter === "500k-1m") {
          matchesPrice = gt.Gia >= 500000 && gt.Gia <= 1000000;
        } else if (this.priceFilter === "1m-2m") {
          matchesPrice = gt.Gia > 1000000 && gt.Gia <= 2000000;
        } else if (this.priceFilter === "over2m") {
          matchesPrice = gt.Gia > 2000000;
        }

        return matchesSearch && matchesPrice;
      });
    },
    paginatedGoiTaps() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredGoiTaps.slice(start, start + this.itemsPerPage);
    },
    totalPages() {
      return Math.ceil(this.filteredGoiTaps.length / this.itemsPerPage);
    },
  },

  watch: {
    searchQuery: _.debounce(function () {
      this.currentPage = 1;
    }, 300),
  },

  methods: {
    applyPriceFilter() {
      this.currentPage = 1;
    },

    async fetchGoiTaps() {
      try {
        this.loading = true;
        const { data } = await axios.get("http://localhost:5000/goitap/");
        this.goiTaps = data.map((gt) => ({ 
          ...gt, 
          _id: String(gt._id),
          QuyenLoi: Array.isArray(gt.QuyenLoi) ? gt.QuyenLoi : (gt.QuyenLoi ? gt.QuyenLoi.split('\n') : [])
        }));
      } catch (err) {
        alert("Lỗi khi tải danh sách gói tập!");
      } finally {
        this.loading = false;
      }
    },

    openModal(gt = null) {
      this.editingGoiTap = gt;
      this.form = gt 
        ? { 
            ...gt, 
            QuyenLoi: Array.isArray(gt.QuyenLoi) ? gt.QuyenLoi.join('\n') : gt.QuyenLoi 
          } 
        : { TenGoiTap: "", MoTa: "", Gia: null, QuyenLoi: "" };
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
      this.editingGoiTap = null;
    },

    confirmDelete(gt) {
      this.deletingGoiTap = gt;
      this.showDeleteModal = true;
    },

    closeDeleteModal() {
      this.showDeleteModal = false;
      this.deletingGoiTap = null;
    },

    async saveGoiTap() {
      try {
        this.loading = true;
        const url = "http://localhost:5000/goitap/";
        const payload = { 
          ...this.form, 
          QuyenLoi: this.form.QuyenLoi.split('\n').filter(benefit => benefit.trim() !== '')
        };

        if (this.editingGoiTap) {
          await axios.put(`${url}${this.editingGoiTap._id}`, payload);
        } else {
          const { data } = await axios.post(url, payload);
          this.goiTaps.push(data);
        }

        this.closeModal();
        this.fetchGoiTaps();
      } catch (err) {
        alert("Có lỗi khi lưu gói tập!");
      } finally {
        this.loading = false;
      }
    },

    async deleteGoiTap(id) {
      try {
        await axios.delete(`http://localhost:5000/goitap/${id}`);
        this.goiTaps = this.goiTaps.filter((gt) => gt._id !== id);
        this.closeDeleteModal();
      } catch (err) {
        alert("Không thể xóa gói tập.");
      }
    },

    prevPage() {
      if (this.currentPage > 1) this.currentPage--;
    },

    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },

    formatCurrency(amount) {
      return amount ? `${amount.toLocaleString()} VND` : "Không xác định";
    },
  },

  mounted() {
    this.fetchGoiTaps();
  },
};
</script>



<style>

.benefits-list {
  list-style-type: disc;
  padding-left: 20px;
  font-size: 0.9rem;
}

.benefits-list li {
  margin-bottom: 5px;
}

.price-filter {
  padding: 5px;
  font-size: 0.9rem;
  margin-left: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
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
}

.custom-container {
  max-width: 1100px;
  margin: 50px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* ======= Tiêu đề ======= */
.custom-title {
  text-align: center;
  font-size: 1.8rem;
  margin-bottom: 20px;
}

/* ======= Thanh tìm kiếm & Nút ======= */
.custom-btn-group {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-bottom: 20px;
}

/* ======= Thanh tìm kiếm ======= */
.custom-search {
  display: flex;
  justify-content: center; /* Canh giữa theo chiều ngang */
  align-items: center;      /* Canh giữa theo chiều dọc nếu cần */
  margin-bottom: 20px;
  width: 100%;
}

.custom-input {
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
  max-width: 600px; /* Giới hạn độ rộng của ô tìm kiếm */
}


.custom-btn {
  padding: 10px 20px;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  color: white;
  cursor: pointer;
  transition: 0.3s;
}

.custom-btn-add { background-color: #27ae60; }
.custom-btn-edit { background-color: #f39c12; }
.custom-btn-delete { background-color: #c0392b; }
.custom-btn-save { background-color: #2980b9; }
.custom-btn-cancel { background-color: #7f8c8d; }

.custom-btn:hover {
  filter: brightness(1.1);
}

/* ======= Bảng ======= */
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
  background-color: #f9f9f9;
}

/* ======= Phân trang ======= */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.pagination button {
  padding: 8px 16px;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #3498db;
  color: white;
}

.pagination button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

/* ======= Modal ======= */
.custom-modal, .delete-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.custom-modal-content, .delete-modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
}

.custom-modal-content h2, .delete-modal-content h2 {
  font-size: 1.5rem;
  margin-bottom: 20px;
}

/* ======= Form ======= */
.custom-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 5px;
}

.custom-input, textarea {
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* ======= Responsive ======= */
@media (max-width: 768px) {
  .custom-container {
    padding: 15px;
  }

  .custom-btn-group {
    flex-direction: column;
  }

  .custom-btn {
    width: 100%;
    text-align: center;
  }
}


</style>