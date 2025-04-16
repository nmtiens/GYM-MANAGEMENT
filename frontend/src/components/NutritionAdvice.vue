<template>
  <div class="nutrition-app">
    <div class="container">
      <!-- Header -->
      <header class="header">
        <h1 class="title">Tư Vấn Dinh Dưỡng</h1>
        <p class="subtitle">Khám phá giá trị dinh dưỡng trong thực phẩm hàng ngày</p>
      </header>
      
      <!-- Search box -->
      <div class="search-container">
        <div class="search-wrapper">
          <div class="input-wrapper">
            <span class="search-icon">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </span>
            <input 
              v-model="foodQuery" 
              type="text" 
              placeholder="Nhập tên thực phẩm (ví dụ: apple, rice, chicken)" 
              class="search-input"
              @keyup.enter="fetchNutrition"
            />
          </div>
          <button 
            @click="fetchNutrition" 
            class="search-button"
          >
            <span>Tra cứu</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="button-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Loading state -->
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p class="loading-text">Đang tìm kiếm thông tin dinh dưỡng...</p>
      </div>
      
      <!-- Error message -->
      <div v-if="error" class="error-container">
        <div class="error-content">
          <div class="error-icon-wrapper">
            <svg class="error-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="error-message">
            <p>{{ error }}</p>
          </div>
        </div>
      </div>
      
      <!-- Results -->
      <div v-if="nutritionData.length && !loading" class="results-container">
        <div class="results-card">
          <div class="results-header">
            <h2 class="results-title">Kết quả dinh dưỡng</h2>
          </div>
          
          <div class="table-container">
            <table class="results-table">
              <thead>
                <tr class="table-header-row">
                  <th class="table-header-cell-left">Thực phẩm</th>
                  <th class="table-header-cell">Calo</th>
                  <th class="table-header-cell">Chất béo (g)</th>
                  <th class="table-header-cell">Protein (g)</th>
                  <th class="table-header-cell">Carbs (g)</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="(item, index) in nutritionData" 
                  :key="index"
                  class="table-row"
                >
                  <td class="table-cell-name">{{ item.name }}</td>
                  <td class="table-cell">
                    <div class="nutrition-value-container">
                      <span class="calories-value">{{ item.calories }}</span>
                      <span class="unit-text">kcal</span>
                    </div>
                  </td>
                  <td class="table-cell">
                    <div class="nutrition-value-container">
                      <span class="fat-value">{{ item.fat_total_g }}</span>
                      <span class="unit-text">g</span>
                    </div>
                  </td>
                  <td class="table-cell">
                    <div class="nutrition-value-container">
                      <span class="protein-value">{{ item.protein_g }}</span>
                      <span class="unit-text">g</span>
                    </div>
                  </td>
                  <td class="table-cell">
                    <div class="nutrition-value-container">
                      <span class="carbs-value">{{ item.carbohydrates_total_g }}</span>
                      <span class="unit-text">g</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <!-- Hiển thị biểu đồ đơn giản -->
          <div v-if="nutritionData.length" class="chart-container">
            <h3 class="chart-title">Phân bố dinh dưỡng</h3>
            <div class="nutrition-chart">
              <div 
                class="fat-bar" 
                :style="{width: getPercentage('fat') + '%'}" 
                :title="`Chất béo: ${getPercentage('fat')}%`"
              ></div>
              <div 
                class="protein-bar" 
                :style="{width: getPercentage('protein') + '%'}" 
                :title="`Protein: ${getPercentage('protein')}%`"
              ></div>
              <div 
                class="carbs-bar" 
                :style="{width: getPercentage('carbs') + '%'}" 
                :title="`Carbs: ${getPercentage('carbs')}%`"
              ></div>
            </div>
            <div class="chart-legend">
              <div class="legend-item">
                <div class="legend-color-fat"></div>
                <span class="legend-text">Chất béo</span>
              </div>
              <div class="legend-item">
                <div class="legend-color-protein"></div>
                <span class="legend-text">Protein</span>
              </div>
              <div class="legend-item">
                <div class="legend-color-carbs"></div>
                <span class="legend-text">Carbs</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Lời khuyên dinh dưỡng -->
        <div class="advice-container">
          <h3 class="advice-title">Lời khuyên dinh dưỡng</h3>
          <p class="advice-text">
            Dựa trên kết quả tra cứu, bạn có thể kết hợp thực phẩm này với các loại rau xanh và 
            trái cây để có một chế độ ăn cân bằng. Luôn đảm bảo đủ nước và đa dạng nguồn dinh dưỡng!
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      foodQuery: '',
      nutritionData: [],
      loading: false,
      error: null,
    };
  },
  methods: {
    async fetchNutrition() {
      if (!this.foodQuery.trim()) {
        this.error = "Vui lòng nhập tên thực phẩm để tra cứu";
        return;
      }
      
      this.loading = true;
      this.error = null;
      
      try {
        const apiKey = 'un4VkTKQp0nSSXOncheLKg==O6960EivFOspRIZd';
        const response = await axios.get('https://api.api-ninjas.com/v1/nutrition', {
          headers: { 'X-Api-Key': apiKey },
          params: { query: this.foodQuery },
        });

        this.nutritionData = response.data;
        
        if (this.nutritionData.length === 0) {
          this.error = "Không tìm thấy thông tin dinh dưỡng cho thực phẩm này. Vui lòng thử lại với thực phẩm khác.";
        }
      } catch (error) {
        console.error('Error:', error.response ? error.response.data : error.message);
        this.error = 'Đã xảy ra lỗi khi truy xuất dữ liệu. Vui lòng thử lại sau.';
      } finally {
        this.loading = false;
      }
    },
    getPercentage(nutrientType) {
      if (!this.nutritionData.length) return 0;
      
      const item = this.nutritionData[0];
      const total = item.fat_total_g + item.protein_g + item.carbohydrates_total_g;
      
      if (total === 0) return 0;
      
      switch(nutrientType) {
        case 'fat':
          return Math.round((item.fat_total_g / total) * 100);
        case 'protein':
          return Math.round((item.protein_g / total) * 100);
        case 'carbs':
          return Math.round((item.carbohydrates_total_g / total) * 100);
        default:
          return 0;
      }
    }
  }
};
</script>

<style scoped>
/* Base styles */
.nutrition-app {
  background: linear-gradient(to bottom right, #f0f9ff, #e6fffa);
  min-height: 100vh;
  padding: 2rem;
}

.container {
  max-width: 1024px;
  margin: 0 auto;
}

/* Header styles */
.header {
  text-align: center;

  animation: fadeIn 0.5s ease-in-out;
}

.title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #047857;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #4b5563;
  font-size: 1rem;
}

/* Search box styles */
.search-container {
  background-color: white;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  margin-bottom: 2rem;
  transition: transform 0.3s ease;
}

.search-container:hover {
  transform: scale(1.02);
}

.search-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input-wrapper {
  position: relative;
  flex-grow: 1;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 0.75rem;
  color: #9ca3af;
}

.icon {
  height: 1.5rem;
  width: 1.5rem;
}

.search-input {
  padding: 0.75rem 1rem 0.75rem 3rem;
  border-radius: 0.5rem;
  border: 2px solid #d1fae5;
  font-size: 1rem;
  width: 100%;
  transition: all 0.3s;
  outline: none;
}

.search-input:focus {
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
}

.search-button {
  background-color: #059669;
  color: white;
  font-weight: 500;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.search-button:hover {
  background-color: #047857;
  transform: translateY(-1px);
}

.button-icon {
  height: 1.25rem;
  width: 1.25rem;
  margin-left: 0.5rem;
}

/* Loading styles */
.loading-container {
  text-align: center;
  padding: 3rem 0;
}

.spinner {
  display: inline-block;
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  border: 0.25rem solid rgba(4, 120, 87, 0.1);
  border-top-color: #047857;
  animation: spin 1s linear infinite;
}

.loading-text {
  margin-top: 1rem;
  color: #047857;
  font-weight: 500;
}

/* Error styles */
.error-container {
  background-color: #fee2e2;
  border-left: 4px solid #ef4444;
  padding: 1rem;
  border-radius: 0.375rem;
  animation: pulse 2s infinite;
}

.error-content {
  display: flex;
}

.error-icon-wrapper {
  flex-shrink: 0;
}

.error-icon {
  height: 1.25rem;
  width: 1.25rem;
  color: #ef4444;
}

.error-message {
  margin-left: 0.75rem;
}

.error-message p {
  font-size: 0.875rem;
  color: #b91c1c;
}

/* Results styles */
.results-container {
  animation: fadeIn 0.5s ease-in-out;
}

.results-card {
  background-color: white;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.results-header {
  background-color: #059669;
  padding: 1rem;
}

.results-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
}

.table-container {
  overflow-x: auto;
}

.results-table {
  width: 100%;
}

.table-header-row {
  background-color: #ecfdf5;
  color: #065f46;
}

.table-header-cell {
  padding: 1rem 1.5rem;
  text-align: center;
}

.table-header-cell-left {
  padding: 1rem 1.5rem;
  text-align: left;
}

.table-row {
  border-top: 1px solid #e5e7eb;
  transition: background-color 0.3s;
}

.table-row:hover {
  background-color: #ecfdf5;
}

.table-cell {
  padding: 1rem 1.5rem;
  text-align: center;
}

.table-cell-name {
  padding: 1rem 1.5rem;
  font-weight: 500;
}

.nutrition-value-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.calories-value {
  font-weight: 700;
  color: #f59e0b;
}

.fat-value {
  font-weight: 700;
  color: #f59e0b;
}

.protein-value {
  font-weight: 700;
  color: #3b82f6;
}

.carbs-value {
  font-weight: 700;
  color: #10b981;
}

.unit-text {
  font-size: 0.75rem;
  color: #6b7280;
}

/* Chart styles */
.chart-container {
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.chart-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1rem;
}

.nutrition-chart {
  display: flex;
  height: 2rem;
  border-radius: 9999px;
  overflow: hidden;
  position: relative;
  transition: all 0.5s ease;
}

.fat-bar {
  background-color: #f59e0b;
  transition: width 1s ease-in-out;
}

.protein-bar {
  background-color: #3b82f6;
  transition: width 1s ease-in-out;
}

.carbs-bar {
  background-color: #10b981;
  transition: width 1s ease-in-out;
}

.chart-legend {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: #4b5563;
}

.legend-item {
  display: flex;
  align-items: center;
}

.legend-color-fat {
  width: 0.75rem;
  height: 0.75rem;
  background-color: #f59e0b;
  border-radius: 9999px;
  margin-right: 0.25rem;
}

.legend-color-protein {
  width: 0.75rem;
  height: 0.75rem;
  background-color: #3b82f6;
  border-radius: 9999px;
  margin-right: 0.25rem;
}

.legend-color-carbs {
  width: 0.75rem;
  height: 0.75rem;
  background-color: #10b981;
  border-radius: 9999px;
  margin-right: 0.25rem;
}

/* Advice styles */
.advice-container {
  margin-top: 1.5rem;
  background-color: white;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  border-left: 4px solid #059669;
}

.advice-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #059669;
  margin-bottom: 0.5rem;
}

.advice-text {
  color: #4b5563;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.8; }
  100% { opacity: 1; }
}

/* Responsive adjustments */
@media (min-width: 768px) {
  .search-wrapper {
    flex-direction: row;
  }
  
  .search-button {
    padding: 0 1.5rem;
  }
}
</style>