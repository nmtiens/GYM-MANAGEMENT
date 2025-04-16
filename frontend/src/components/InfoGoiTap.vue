<template>
  <div class="membership-container">
    <h1 class="page-title">Các Gói Tập Gym</h1>
    
    <div class="loading-wrapper" v-if="loading">
      <div class="loader"></div>
    </div>

    <transition-group 
      name="package-list" 
      tag="div" 
      class="membership-grid"
      v-else
    >
      <div 
        v-for="goi in sortedGoiTaps" 
        :key="goi._id" 
        class="membership-card"
        :class="getCardClass(goi.Gia)"
      >
        <div class="card-badge">
          {{ getPackageBadge(goi.Gia) }}
        </div>
        
        <div class="card-content">
          <h2 class="card-title">{{ goi.TenGoi }}</h2>
          
          <p class="card-description">{{ goi.MoTa }}</p>
          
          <div class="card-price">
            {{ formatCurrency(goi.Gia) }}
          </div>
          
          <ul class="card-benefits">
            <li 
              v-for="(quyenLoi, idx) in goi.QuyenLoi" 
              :key="idx"
            >
              <svg 
                class="benefit-icon" 
                fill="currentColor" 
                viewBox="0 0 20 20"
              >
                <path 
                  fill-rule="evenodd" 
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" 
                  clip-rule="evenodd"
                />
              </svg>
              {{ quyenLoi }}
            </li>
          </ul>
          
          <button 
          class="register-button"
          @click="registerPackage(goi)"
        >
          Đăng Ký Ngay
        </button>
        </div>
      </div>
    </transition-group>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      goiTaps: [],
      loading: true
    }
  },
  computed: {
    sortedGoiTaps() {
      // Sắp xếp các gói theo giá tiền tăng dần
      return [...this.goiTaps].sort((a, b) => a.Gia - b.Gia);
    }
  },
  methods: {
    async fetchGoiTaps() {
      try {
        this.loading = true;
        const { data } = await axios.get("http://localhost:5000/goitap/");
        this.goiTaps = data.map((gt) => ({ 
          ...gt, 
          _id: String(gt._id),
          QuyenLoi: Array.isArray(gt.QuyenLoi) 
            ? gt.QuyenLoi 
            : (gt.QuyenLoi 
              ? gt.QuyenLoi.split('\n')
                .map(item => item.trim())
                .filter(item => item !== '')
              : [])
        }));
      } catch (err) {
        console.error("Lỗi khi tải danh sách gói tập:", err);
        alert("Không thể tải danh sách gói tập. Vui lòng thử lại sau.");
      } finally {
        this.loading = false;
      }
    },

 registerPackage(goi) {
  try {
    // Check if Vue Router is available
    if (this.$router) {
      this.$router.push({
        path: '/register',
        query: { 
          packageId: goi._id, 
          packageName: goi.TenGoiTap  // Truyền tên gói tập
        }
      });
    } 
    // Fallback redirect if router is not available
    else if (window.location) {
      window.location.href = `/register?packageId=${goi._id}&packageName=${encodeURIComponent(goi.TenGoiTap)}`;
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

    
    formatCurrency(value) {
      return new Intl.NumberFormat('vi-VN', { 
        style: 'currency', 
        currency: 'VND' 
      }).format(value);
    },
    getCardClass(price) {
      if (price < 700000) return 'basic-package';
      if (price < 1200000) return 'standard-package';
      return 'premium-package';
    },
    getPackageBadge(price) {
      if (price < 700000) return 'Cơ Bản';
      if (price < 1200000) return 'Nâng Cao';
      return 'VIP';
    }
  },
  created() {
    this.fetchGoiTaps();
  }
}
</script>

<style>
:root {
  --color-background: #f4f7f6;
  --color-text-dark: #2c3e50;
  --color-text-light: #ffffff;
  --color-basic: #3498db;
  --color-standard: #2ecc71;
  --color-premium: #9b59b6;
}
</style>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.membership-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  background-color: var(--color-background);
}

.page-title {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 2.5rem;
  color: var(--color-text-dark);
  position: relative;
}

.page-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 4px;
  background-color: var(--color-basic);
}

.loading-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50vh;
}

.loader {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top: 4px solid var(--color-basic);
  border-radius: 50%;
  width: 60px;
  height: 60px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.membership-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.membership-card {
  background-color: white;
  border-radius: 15px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
}

.membership-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.card-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
}

.basic-package .card-badge {
  background-color: var(--color-basic);
  color: var(--color-text-light);
}

.standard-package .card-badge {
  background-color: var(--color-standard);
  color: var(--color-text-light);
}

.premium-package .card-badge {
  background-color: var(--color-premium);
  color: var(--color-text-light);
}

.card-content {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.card-title {
  text-align: center;
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: var(--color-text-dark);
}

.card-description {
  text-align: center;
  color: #6c757d;
  margin-bottom: 1.5rem;
  min-height: 3rem;
}

.card-price {
  text-align: center;
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
}

.basic-package .card-price { color: var(--color-basic); }
.standard-package .card-price { color: var(--color-standard); }
.premium-package .card-price { color: var(--color-premium); }

.card-benefits {
  list-style: none;
  margin-bottom: 1.5rem;
  flex-grow: 1;
}

.card-benefits li {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}

.benefit-icon {
  width: 20px;
  height: 20px;
  margin-right: 10px;
}

.basic-package .benefit-icon { color: var(--color-basic); }
.standard-package .benefit-icon { color: var(--color-standard); }
.premium-package .benefit-icon { color: var(--color-premium); }

.register-button {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.basic-package .register-button {
  background-color: var(--color-basic);
  color: var(--color-text-light);
}

.standard-package .register-button {
  background-color: var(--color-standard);
  color: var(--color-text-light);
}

.premium-package .register-button {
  background-color: var(--color-premium);
  color: var(--color-text-light);
}

.register-button:hover {
  opacity: 0.9;
  transform: scale(1.02);
}

.package-list-enter-active, 
.package-list-leave-active {
  transition: all 0.5s ease;
}

.package-list-enter, 
.package-list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
</style>