<template>
  <div class="trainers-container">
    <div class="trainers-header">
      <h2>Danh Sách Huấn Luyện Viên</h2>
    </div>
    
    <!-- Loading and error states -->
    <div v-if="loading" class="state-message">
      <div class="spinner"></div>
      <p>Đang tải danh sách huấn luyện viên...</p>
    </div>
    
    <div v-if="error" class="state-message error">
      <p>{{ error }}</p>
      <button @click="fetchHuanLuyenVien" class="retry-button">Thử lại</button>
    </div>
    
    <!-- Search and filter options -->
    <div v-if="!loading && !error" class="search-container">
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Tìm kiếm theo tên hoặc mô tả..."
        />
        <span class="search-icon">🔍</span>
      </div>
      
      <div class="filter-options">
        <select v-model="yearFilter">
          <option value="">Tất cả năm kinh nghiệm</option>
          <option value="0-1">0-1 năm</option>
          <option value="1-3">1-3 năm</option>
          <option value="3-5">3-5 năm</option>
          <option value="5+">Trên 5 năm</option>
        </select>
      </div>
    </div>
    
    <!-- Trainer cards -->
    <div v-if="!loading && !error" class="trainers-grid">
      <div 
        v-for="hlv in filteredTrainers" 
        :key="hlv._id" 
        class="trainer-card"
        :class="{ 'selected': selectedTrainer === hlv._id }"
        @click="toggleTrainerSelection(hlv)"
      >
        <div class="trainer-image">
          <swiper
            v-if="hlv.Anh && hlv.Anh.length > 1"
            :slides-per-view="1"
            :pagination="{ clickable: true }"
            :navigation="true"
            :modules="modules"
          >
            <swiper-slide v-for="(img, index) in hlv.Anh" :key="index">
              <img :src="getImageUrl(img)" :alt="`Ảnh của ${hlv.HoTen}`" />
            </swiper-slide>
          </swiper>
          
          <div v-else class="single-image">
            <img 
              :src="getImageUrl(hlv.Anh && hlv.Anh.length ? hlv.Anh[0] : null)" 
              :alt="`Ảnh của ${hlv.HoTen}`"
            />
          </div>
          
          <div class="experience-badge" v-if="hlv.KinhNghiem">
            {{ hlv.KinhNghiem }}
          </div>
        </div>
        
        <div class="trainer-info">
          <h3>{{ hlv.HoTen || 'Chưa cập nhật' }}</h3>
          
          <div class="info-detail">
            <span class="info-icon">📱</span>
            <span>{{ formatPhone(hlv.SDT) || 'Chưa cập nhật' }}</span>
          </div>
          
          <div class="info-detail">
            <span class="info-icon">🏆</span>
            <span>{{ hlv.KinhNghiem || 'Chưa có kinh nghiệm' }}</span>
          </div>
          
          <div class="trainer-description">
            <p>{{ hlv.MoTa || 'Chưa có mô tả' }}</p>
          </div>
          
          <button class="select-button" @click.stop="selectHLV(hlv)">
            Chọn huấn luyện viên
          </button>
        </div>
      </div>
    </div>
    
    <!-- Empty state -->
    <div v-if="!loading && !error && filteredTrainers.length === 0" class="empty-state">
      <div class="empty-icon">🔎</div>
      <p>Không tìm thấy huấn luyện viên phù hợp với tiêu chí tìm kiếm.</p>
      <button @click="resetFilters" class="reset-button">Xóa bộ lọc</button>
    </div>
    
    <!-- Pagination -->
    <div v-if="!loading && !error && filteredTrainers.length > 0" class="pagination">
      <button 
        :disabled="currentPage === 1" 
        @click="currentPage--" 
        class="page-button"
      >
        &laquo; Trước
      </button>
      <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
      <button 
        :disabled="currentPage === totalPages" 
        @click="currentPage++" 
        class="page-button"
      >
        Sau &raquo;
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Swiper, SwiperSlide } from "swiper/vue";
import { Navigation, Pagination } from "swiper/modules";
import "swiper/css";
import "swiper/css/pagination";
import "swiper/css/navigation";

export default {
  components: { Swiper, SwiperSlide },
  emits: ["select"],
  data() {
    return {
      huanluyenvien: [],
      loading: false,
      error: null,
      searchQuery: "",
      yearFilter: "",
      selectedTrainer: null,
      defaultImage: "/images/default-trainer.png",
      currentPage: 1,
      itemsPerPage: 6
    };
  },
  computed: {
    filteredTrainers() {
      let filtered = [...this.huanluyenvien];
      
      // Filter by search query
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(hlv => 
          (hlv.HoTen && hlv.HoTen.toLowerCase().includes(query)) ||
          (hlv.MoTa && hlv.MoTa.toLowerCase().includes(query))
        );
      }
      
      // Filter by years of experience
      if (this.yearFilter) {
        filtered = filtered.filter(hlv => {
          // Extract years from experience text using regex
          const yearsMatch = hlv.KinhNghiem && hlv.KinhNghiem.match(/(\d+)(?:\s*-\s*(\d+))?\s*năm/i);
          
          if (!yearsMatch) return false;
          
          let years = parseInt(yearsMatch[1], 10);
          
          // Handle range based filtering
          switch(this.yearFilter) {
            case "0-1":
              return years >= 0 && years <= 1;
            case "1-3":
              return years > 1 && years <= 3;
            case "3-5":
              return years > 3 && years <= 5;
            case "5+":
              return years > 5;
            default:
              return true;
          }
        });
      }
      
      // Apply pagination
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return filtered.slice(start, end);
    },
    totalPages() {
      const filteredLength = this.huanluyenvien.filter(hlv => {
        // Apply search filter
        if (this.searchQuery) {
          const query = this.searchQuery.toLowerCase();
          if (!((hlv.HoTen && hlv.HoTen.toLowerCase().includes(query)) ||
                (hlv.MoTa && hlv.MoTa.toLowerCase().includes(query)))) {
            return false;
          }
        }
        
        // Apply experience filter
        if (this.yearFilter) {
          const yearsMatch = hlv.KinhNghiem && hlv.KinhNghiem.match(/(\d+)(?:\s*-\s*(\d+))?\s*năm/i);
          if (!yearsMatch) return false;
          
          let years = parseInt(yearsMatch[1], 10);
          
          switch(this.yearFilter) {
            case "0-1":
              return years >= 0 && years <= 1;
            case "1-3":
              return years > 1 && years <= 3;
            case "3-5":
              return years > 3 && years <= 5;
            case "5+":
              return years > 5;
            default:
              return true;
          }
        }
        
        return true;
      }).length;
      
      return Math.ceil(filteredLength / this.itemsPerPage);
    }
  },
  watch: {
    searchQuery() {
      this.currentPage = 1;
    },
    yearFilter() {
      this.currentPage = 1;
    }
  },
  mounted() {
    this.fetchHuanLuyenVien();
  },
  methods: {
    async fetchHuanLuyenVien() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.get("http://localhost:5000/huanluyenvien");
        this.huanluyenvien = response.data.map((hlv) => ({
          ...hlv,
          Anh: typeof hlv.Anh === "string" ? [hlv.Anh] : hlv.Anh || [],
        }));
      } catch (err) {
        this.error = "Không thể tải dữ liệu Huấn Luyện Viên. Vui lòng thử lại sau.";
        console.error("Error fetching trainers:", err);
      } finally {
        this.loading = false;
      }
    },
    getImageUrl(img) {
      if (!img) return this.defaultImage;
      
      // Handle different image path formats
      if (typeof img === 'string') {
        if (img.startsWith('/uploads')) {
          return `http://localhost:5000${img}`;
        } else if (img.startsWith('http')) {
          return img;
        } else {
          return `http://localhost:5000/uploads/${img}`;
        }
      }
      
      return this.defaultImage;
    },
    toggleTrainerSelection(hlv) {
      this.selectedTrainer = this.selectedTrainer === hlv._id ? null : hlv._id;
    },
   selectHLV(hlv) {
  try {
    // Check if Vue Router is available
    if (this.$router) {
      this.$router.push({
        path: '/register',
        query: { 
          huanluyenvien: hlv.HoTen
        }
      });
      
      // Also emit the event for backward compatibility
      this.$emit("select", hlv.HoTen);
    } 
    // Fallback redirect if router is not available
    else if (window.location) {
      window.location.href = `/register?huanluyenvien=${encodeURIComponent(hlv.HoTen)}`;
    }
    // Last resort error handling
    else {
      alert('Không thể chuyển trang. Vui lòng liên hệ hỗ trợ.');
    }
  } catch (error) {
    console.error('Lỗi khi chuyển trang đăng ký:', error);
    alert('Đã xảy ra lỗi. Vui lòng thử lại.');
  }
},
    resetFilters() {
      this.searchQuery = "";
      this.yearFilter = "";
    },
   
    formatPhone(phone) {
      if (!phone) return "";
      
      // Format phone number as XXX-XXX-XXXX or keep original if not valid
      const cleaned = ('' + phone).replace(/\D/g, '');
      if (cleaned.length === 10) {
        return cleaned.replace(/(\d{3})(\d{3})(\d{4})/, '$1-$2-$3');
      }
      return phone;
    }
  },
  setup() {
    return {
      modules: [Navigation, Pagination],
    };
  },
};
</script>

<style scoped>
/* CSS remains unchanged */
.trainers-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.trainers-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #eaeaea;
  background-color: #ffffff;
  border-radius: 16px 16px 0 0;
}

.trainers-header h2 {
  font-size: 1.6rem;
  font-weight: 600;
  color: #222;
  margin: 0;
}

.state-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  text-align: center;
  color: #666;
}

.state-message.error {
  color: #e53935;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(33, 150, 243, 0.1);
  border-radius: 50%;
  border-left-color: #2196f3;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.retry-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.retry-button:hover {
  background-color: #d32f2f;
  transform: translateY(-2px);
}

.search-container {
  padding: 20px 24px;
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  border-bottom: 1px solid #eaeaea;
  background-color: #f9f9f9;
}

.search-box {
  flex: 1;
  position: relative;
  min-width: 250px;
}

.search-box input {
  width: 100%;
  padding: 12px 16px 12px 44px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.2s;
  background-color: white;
}

.search-box input:focus {
  outline: none;
  border-color: #2196f3;
  box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.15);
}

.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  font-size: 18px;
}

.filter-options select {
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: white;
  font-size: 15px;
  min-width: 200px;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-options select:focus {
  outline: none;
  border-color: #2196f3;
  box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.15);
}

.trainers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
  padding: 30px;
}

.trainer-card {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s;
  cursor: pointer;
  border: 2px solid transparent;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.trainer-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.trainer-card.selected {
  border-color: #2196f3;
  box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.2);
}

.trainer-image {
  height: 220px;
  overflow: hidden;
  background-color: #f5f5f5;
  position: relative;
}

.trainer-image img, .single-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s;
}

.trainer-card:hover .trainer-image img {
  transform: scale(1.08);
}

.single-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
}



.trainer-info {
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.trainer-info h3 {
  margin: 0 0 16px 0;
  font-size: 20px;
  color: #333;
  font-weight: 600;
}

.info-detail {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  color: #555;
}

.info-icon {
  font-size: 18px;
  width: 24px;
  text-align: center;
}

.trainer-description {
  margin: 16px 0;
  font-size: 15px;
  color: #666;
  line-height: 1.6;
  flex-grow: 1;
}

.select-button {
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 20px;
  font-size: 15px;
  width: 100%;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 16px;
  font-weight: 500;
}

.select-button:hover {
  background-color: #1976d2;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.select-button:active {
  transform: translateY(0);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 30px;
  text-align: center;
  color: #666;
}

.empty-icon {
  font-size: 40px;
  margin-bottom: 16px;
  opacity: 0.7;
}

.reset-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #f0f0f0;
  color: #444;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.reset-button:hover {
  background-color: #e0e0e0;
  transform: translateY(-2px);
}

/* Pagination styles */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 16px 0 24px;
  gap: 12px;
  border-top: 1px solid #eaeaea;
}

.page-button {
  padding: 8px 16px;
  background-color: #f0f0f0;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  color: #444;
  font-weight: 500;
}

.page-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-button:not(:disabled):hover {
  background-color: #2196f3;
  color: white;
}

.page-info {
  font-size: 15px;
  color: #666;
  font-weight: 500;
}

/* Swiper customization */
:deep(.swiper) {
  width: 100%;
  height: 100%;
}

:deep(.swiper-slide) {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
}

:deep(.swiper-pagination-bullet-active) {
  background-color: #2196f3;
}

:deep(.swiper-button-next),
:deep(.swiper-button-prev) {
  color: white;
  background-color: rgba(0, 0, 0, 0.4);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.swiper-button-next:after),
:deep(.swiper-button-prev:after) {
  font-size: 18px;
  font-weight: bold;
}

/* Responsive adjustments */
@media (max-width: 900px) {
  .trainers-grid {
    grid-template-columns: repeat(2, 1fr);
    padding: 20px;
  }
}

@media (max-width: 600px) {
  .trainers-grid {
    grid-template-columns: 1fr;
  }
  
  .search-container {
    flex-direction: column;
  }
  
  .filter-options select {
    width: 100%;
  }
}
</style>