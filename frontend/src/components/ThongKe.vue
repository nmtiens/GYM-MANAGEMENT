<template>
  <div class="revenue-statistics">
    <h1 class="page-title">Thống kê doanh Thu</h1>
    
    <!-- Bộ lọc -->
    <div class="filter-section">
      <div class="filter-grid">
        <div class="filter-item">
          <label>Từ ngày</label>
          <input type="date" v-model="filters.fromDate" />
        </div>
        <div class="filter-item">
          <label>Đến ngày</label>
          <input type="date" v-model="filters.toDate" />
        </div>
        <div class="filter-item">
          <label>Gói tập</label>
          <select v-model="filters.goiTap">
            <option value="">Tất cả</option>
            <option v-for="goi in dsGoiTap" :key="goi._id" :value="goi._id">{{ goi.TenGoiTap }}</option>
          </select>
        </div>
        <div class="filter-item">
          <label>Dịch vụ</label>
          <select v-model="filters.dichVu">
            <option value="">Tất cả</option>
            <option v-for="dv in dsDichVu" :key="dv._id" :value="dv._id">{{ dv.TenDichVu }}</option>
          </select>
        </div>
      </div>
      <div class="filter-actions">
        <button @click="applyFilter" class="btn-primary">Lọc</button>
        <button @click="resetFilter" class="btn-secondary">Đặt lại</button>
      </div>
    </div>
    
    <!-- Thống kê tổng doanh thu -->
    <div class="summary-section">
      <h2 class="section-title">Tổng quan doanh thu</h2>
      <div class="summary-grid">
        <div class="stat-card stat-today">
          <div class="stat-label">Hôm nay</div>
          <div class="stat-value">{{ formatCurrency(statistics.today) }}</div>
          <div class="stat-change" :class="{'positive': statistics.todayGrowth >= 0, 'negative': statistics.todayGrowth < 0}">
            {{ statistics.todayGrowth >= 0 ? '+' : '' }}{{ statistics.todayGrowth }}% so với hôm qua
          </div>
        </div>
        
        <div class="stat-card stat-week">
          <div class="stat-label">Tuần này</div>
          <div class="stat-value">{{ formatCurrency(statistics.thisWeek) }}</div>
          <div class="stat-change" :class="{'positive': statistics.weekGrowth >= 0, 'negative': statistics.weekGrowth < 0}">
            {{ statistics.weekGrowth >= 0 ? '+' : '' }}{{ statistics.weekGrowth }}% so với tuần trước
          </div>
        </div>
        
        <div class="stat-card stat-month">
          <div class="stat-label">Tháng này</div>
          <div class="stat-value">{{ formatCurrency(statistics.thisMonth) }}</div>
          <div class="stat-change" :class="{'positive': statistics.monthGrowth >= 0, 'negative': statistics.monthGrowth < 0}">
            {{ statistics.monthGrowth >= 0 ? '+' : '' }}{{ statistics.monthGrowth }}% so với tháng trước
          </div>
        </div>
        
        <div class="stat-card stat-year">
          <div class="stat-label">Năm nay</div>
          <div class="stat-value">{{ formatCurrency(statistics.thisYear) }}</div>
          <div class="stat-change" :class="{'positive': statistics.yearGrowth >= 0, 'negative': statistics.yearGrowth < 0}">
            {{ statistics.yearGrowth >= 0 ? '+' : '' }}{{ statistics.yearGrowth }}% so với năm trước
          </div>
        </div>
      </div>
    </div>
    
    <!-- Biểu đồ doanh thu -->
    <div class="chart-section">
      <h2 class="section-title">Biểu đồ doanh thu</h2>
      <div class="chart-period">
        <button 
          v-for="period in ['day', 'week', 'month', 'year']" 
          :key="period"
          @click="changePeriod(period)"
          class="period-btn"
          :class="{'active': chartPeriod === period}"
        >
          {{ getPeriodName(period) }}
        </button>
      </div>
     <div class="chart-container">
  <canvas v-if="!loading" id="revenueChart"></canvas>
  <div v-else class="chart-placeholder">
    Biểu đồ doanh thu sẽ hiển thị tại đây
  </div>
</div>
    </div>
    
    <!-- Bảng danh sách chi tiết -->
    <div class="table-section">
      <h2 class="section-title">Chi tiết doanh thu</h2>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Mã thẻ hội viên</th>
              <th>Hội viên</th>
              <th>Gói tập</th>
              <th>Dịch vụ</th>
              <th>Ngày tạo</th>
              <th class="text-right">Giá gói tập</th>
              <th class="text-right">Giá dịch vụ</th>
              <th class="text-right">Tổng chi phí</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in paginatedItems" :key="index">
              <td>{{ item.MaTheHoiVien }}</td>
              <td>{{ item.HoiVien }}</td>
              <td>{{ item.GoiTap }}</td>
              <td>{{ formatDichVu(item.DichVu) }}</td>
              <td>{{ formatDate(item.NgayTao) }}</td>
              <td class="text-right">{{ formatCurrency(getGoiTapPrice(item.GoiTap)) }}</td>
              <td class="text-right">{{ formatCurrency(getDichVuPrice(item.DichVu)) }}</td>
              <td class="text-right total-cost">{{ formatCurrency(calculateTotal(item)) }}</td>
            </tr>
            <tr v-if="filteredItems.length === 0">
              <td colspan="11" class="no-data">Không có dữ liệu</td>
            </tr>
          </tbody>
          <tfoot v-if="filteredItems.length > 0">
            <tr>
              <td colspan="5" class="text-right">Tổng cộng:</td>
              <td class="text-right total-sum">{{ formatCurrency(filteredItems.reduce((total, item) => total + getGoiTapPrice(item.GoiTap), 0)) }}</td>
              <td class="text-right total-sum">{{ formatCurrency(filteredItems.reduce((total, item) => total + getDichVuPrice(item.DichVu), 0)) }}</td>
              <td class="text-right total-sum">{{ formatCurrency(totalFilteredRevenue) }}</td>
            </tr>
          </tfoot>
        </table>
      </div>
      
      <!-- Phân trang -->
      <div class="pagination">
        <div class="pagination-info">
          Hiển thị {{ filteredItems.length > 0 ? (currentPage - 1) * itemsPerPage + 1 : 0 }} - 
          {{ Math.min(currentPage * itemsPerPage, filteredItems.length) }} trong số {{ filteredItems.length }} kết quả
        </div>
        <div class="pagination-controls">
          <button 
            @click="prevPage" 
            :disabled="currentPage === 1"
            class="pagination-btn"
            :class="{'disabled': currentPage === 1}"
          >
            Trước
          </button>
          <button 
            @click="nextPage" 
            :disabled="currentPage >= totalPages"
            class="pagination-btn"
            :class="{'disabled': currentPage >= totalPages}"
          >
            Sau
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
  data() {
    return {
      // Data
      items: [],
      dsGoiTap: [],
      dsDichVu: [],
      dsHoiVien: [],
      dsNhanVien: [],
      dsHuanLuyenVien: [],
      // Filters
      filters: {
        fromDate: '',
        toDate: '',
        goiTap: '',
        dichVu: ''
      },
      // Chart
      chartPeriod: 'month',
      revenueChart: null,
      chartData: {
        day: { labels: [], datasets: [] },
        week: { labels: [], datasets: [] },
        month: { labels: [], datasets: [] },
        year: { labels: [], datasets: [] }
      },
      // Pagination
      currentPage: 1,
      itemsPerPage: 10,
      // Statistics
      statistics: {
        today: 0,
        todayGrowth: 0,
        thisWeek: 0,
        weekGrowth: 0,
        thisMonth: 0,
        monthGrowth: 0,
        thisYear: 0,
        yearGrowth: 0
      },
      // Loading state
      loading: false,
      error: null
    };
  },
  computed: {
    filteredItems() {
      let result = [...this.items];
      
      if (this.filters.fromDate) {
        const fromDate = new Date(this.filters.fromDate);
        result = result.filter(item => new Date(item.NgayTao) >= fromDate);
      }
      
      if (this.filters.toDate) {
        const toDate = new Date(this.filters.toDate);
        toDate.setHours(23, 59, 59, 999); // Set to end of day
        result = result.filter(item => new Date(item.NgayTao) <= toDate);
      }
      
      if (this.filters.goiTap) {
        // Get package name from ID
        const selectedGoiTap = this.dsGoiTap.find(g => g._id === this.filters.goiTap);
        if (selectedGoiTap) {
          result = result.filter(item => item.GoiTap === selectedGoiTap.TenGoiTap);
        }
      }
      
      if (this.filters.dichVu) {
        // Get service name from ID
        const selectedDichVu = this.dsDichVu.find(d => d._id === this.filters.dichVu);
        if (selectedDichVu) {
          result = result.filter(item => item.DichVu === selectedDichVu.TenDichVu);
        }
      }
      
      return result;
    },
    paginatedItems() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredItems.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage);
    },
    totalFilteredRevenue() {
      return this.filteredItems.reduce((total, item) => total + this.calculateTotal(item), 0);
    }
  },
  async created() {
    this.loading = true;
    try {
      // Load membership card data
      const theHoiVienResponse = await axios.get("http://localhost:5000/thehoivien/");
      this.items = theHoiVienResponse.data;
      
      // Load fitness package data
      const goiTapResponse = await axios.get("http://localhost:5000/goitap/");
      this.dsGoiTap = goiTapResponse.data;
      
      // Load service data
      const dichVuResponse = await axios.get("http://localhost:5000/dichvu/");
      this.dsDichVu = dichVuResponse.data;
      
      // Debug sample data if available
      if (this.items.length > 0) {
        const sampleItem = this.items[0];
        console.log("Sample item:", sampleItem);
        console.log("Package name:", sampleItem.GoiTap);
        console.log("Service name:", sampleItem.DichVu);
        console.log("Package price:", this.getGoiTapPrice(sampleItem.GoiTap));
        console.log("Service price:", this.getDichVuPrice(sampleItem.DichVu));
      }
      
      // Calculate statistics
      this.calculateStatistics();
      
      // Prepare chart data
      this.prepareChartData();
    } catch (error) {
      console.error("Error loading data:", error);
      this.error = "An error occurred while loading data. Please try again later.";
    } finally {
      this.loading = false;
    }
  },
  mounted() {
    // Initialize chart when component is mounted
    this.$nextTick(() => {
      this.initChart();
    });
  },
  methods: {
    formatDichVu(DichVu) {
      if (!DichVu) return "No service";
      
      try {
        if (typeof DichVu === "string") {
          if (DichVu.trim().startsWith('[') && DichVu.trim().endsWith(']')) {
            const parsedArray = JSON.parse(DichVu);
            return Array.isArray(parsedArray) ? parsedArray.join(", ") : DichVu;
          }
          return DichVu;
        }
        
        if (Array.isArray(DichVu)) return DichVu.join(", ");
        
        return "No service";
      } catch (error) {
        return DichVu;
      }
    },
    
    // Get package price from name
    getGoiTapPrice(goiTapName) {
      // Check if goiTapName is null or undefined
      if (!goiTapName) return 0;
      
      // Find package info by name
      const goiTapInfo = this.dsGoiTap.find(g => g.TenGoiTap === goiTapName);
      
      // Check if not found, log for debug
      if (!goiTapInfo) {
        console.log(`Package not found with name: ${goiTapName}`);
        return 0;
      }
      
      return goiTapInfo.Gia || 0;
    },

    // Get service price from name
    getDichVuPrice(dichVuName) {
      // Check if dichVuName is null or undefined
      if (!dichVuName) return 0;
      
      let totalPrice = 0;
      
      // Check if dichVuName is an array
      if (Array.isArray(dichVuName)) {
        // If array, calculate total price of all services
        dichVuName.forEach(name => {
          const dichVuInfo = this.dsDichVu.find(d => d.TenDichVu === name);
          if (dichVuInfo) {
            totalPrice += dichVuInfo.Gia || 0;
          } else {
            console.log(`Service not found with name: ${name}`);
          }
        });
      } else if (typeof dichVuName === 'string') {
        // If string, check if it's multiple services separated by commas
        if (dichVuName.includes(',')) {
          // Split string by comma and process each service
          const services = dichVuName.split(',').map(s => s.trim());
          services.forEach(name => {
            const dichVuInfo = this.dsDichVu.find(d => d.TenDichVu === name);
            if (dichVuInfo) {
              totalPrice += dichVuInfo.Gia || 0;
            } else {
              console.log(`Service not found with name: ${name}`);
            }
          });
        } else {
          // If only one service
          const dichVuInfo = this.dsDichVu.find(d => d.TenDichVu === dichVuName);
          if (dichVuInfo) {
            totalPrice = dichVuInfo.Gia || 0;
          } else {
            console.log(`Service not found with name: ${dichVuName}`);
          }
        }
      }
      
      return totalPrice;
    },

    // Calculate total cost
    calculateTotal(item) {
      const goiTapPrice = this.getGoiTapPrice(item.GoiTap);
      const dichVuPrice = this.getDichVuPrice(item.DichVu);
      return goiTapPrice + dichVuPrice;
    },
    
    // Format currency
    formatCurrency(value) {
      return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(value);
    },
    
    // Format date
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('vi-VN').format(date);
    },
    
    // Apply filter
    applyFilter() {
      this.currentPage = 1;
    },
    
    // Reset filter
    resetFilter() {
      this.filters = {
        fromDate: '',
        toDate: '',
        goiTap: '',
        dichVu: ''
      };
      this.currentPage = 1;
    },
    
    // Initialize chart
    initChart() {
      const ctx = document.getElementById('revenueChart');
      if (!ctx) {
        console.error("Canvas element for chart not found!");
        return;
      }
      
      // Destroy existing chart if it exists
      if (this.revenueChart) {
        this.revenueChart.destroy();
      }
      
      // Create new chart with current period data
      this.revenueChart = new Chart(ctx, {
        type: 'line',
        data: this.chartData[this.chartPeriod],
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: `Revenue chart by ${this.getPeriodName(this.chartPeriod).toLowerCase()}`
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  let label = context.dataset.label || '';
                  if (label) {
                    label += ': ';
                  }
                  if (context.parsed.y !== null) {
                    label += new Intl.NumberFormat('vi-VN', { 
                      style: 'currency', 
                      currency: 'VND' 
                    }).format(context.parsed.y);
                  }
                  return label;
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: function(value) {
                  return new Intl.NumberFormat('vi-VN', { 
                    style: 'currency', 
                    currency: 'VND',
                    notation: 'compact',
                    compactDisplay: 'short'
                  }).format(value);
                }
              }
            }
          }
        }
      });
    },
    
    // Change chart period and update chart
    changePeriod(period) {
      this.chartPeriod = period;
      this.$nextTick(() => {
        this.initChart();
      });
    },
    
    // Get period name
    getPeriodName(period) {
      const periodNames = {
        'day': 'Day',
        'week': 'Week',
        'month': 'Month',
        'year': 'Year'
      };
      return periodNames[period] || 'Period';
    },
    
    // Pagination: next page
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage += 1;
      }
    },
    
    // Pagination: previous page
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage -= 1;
      }
    },
    
    // Prepare data for all chart periods
    prepareChartData() {
      this.prepareChartDataByDay();
      this.prepareChartDataByWeek();
      this.prepareChartDataByMonth();
      this.prepareChartDataByYear();
    },
    
    // Prepare daily chart data (last 30 days)
    prepareChartDataByDay() {
      const endDate = new Date();
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - 29); // Last 30 days including today
      
      const labels = [];
      const goiTapData = [];
      const dichVuData = [];
      const totalData = [];
      
      // Create array of days
      for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
        const dateStr = d.toISOString().split('T')[0];
        labels.push(this.formatDate(dateStr));
        
        // Filter items for this day
        const dayItems = this.items.filter(item => {
          const itemDate = new Date(item.NgayTao).toISOString().split('T')[0];
          return itemDate === dateStr;
        });
        
        // Calculate revenue for each category
        const goiTapRevenue = dayItems.reduce((total, item) => 
          total + this.getGoiTapPrice(item.GoiTap), 0);
        const dichVuRevenue = dayItems.reduce((total, item) => 
          total + this.getDichVuPrice(item.DichVu), 0);
        const totalRevenue = goiTapRevenue + dichVuRevenue;
        
        goiTapData.push(goiTapRevenue);
        dichVuData.push(dichVuRevenue);
        totalData.push(totalRevenue);
      }
      
      this.chartData.day = {
        labels: labels,
        datasets: [
          {
            label: 'Fitness Packages',
            data: goiTapData,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          },
          {
            label: 'Services',
            data: dichVuData,
            backgroundColor: 'rgba(255, 206, 86, 0.2)',
            borderColor: 'rgba(255, 206, 86, 1)',
            borderWidth: 1
          },
          {
            label: 'Total',
            data: totalData,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2
          }
        ]
      };
    },
    
    // Prepare weekly chart data (last 12 weeks)
    prepareChartDataByWeek() {
      const endDate = new Date();
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - 83); // Last 12 weeks
      
      const labels = [];
      const goiTapData = [];
      const dichVuData = [];
      const totalData = [];
      
      // Create array of weeks
      for (let w = 0; w < 12; w++) {
        const weekStart = new Date(endDate);
        weekStart.setDate(weekStart.getDate() - 7 * (11 - w));
        const weekEnd = new Date(weekStart);
        weekEnd.setDate(weekEnd.getDate() + 6);
        
        // Week label (e.g., "01/03 - 07/03")
        const weekLabel = `${this.formatDate(weekStart)} - ${this.formatDate(weekEnd)}`;
        labels.push(weekLabel);
        
        // Filter items for this week
        const weekItems = this.items.filter(item => {
          const itemDate = new Date(item.NgayTao);
          return itemDate >= weekStart && itemDate <= weekEnd;
        });
        
        // Calculate revenue for each category
        const goiTapRevenue = weekItems.reduce((total, item) => 
          total + this.getGoiTapPrice(item.GoiTap), 0);
        const dichVuRevenue = weekItems.reduce((total, item) => 
          total + this.getDichVuPrice(item.DichVu), 0);
        const totalRevenue = goiTapRevenue + dichVuRevenue;
        
        goiTapData.push(goiTapRevenue);
        dichVuData.push(dichVuRevenue);
        totalData.push(totalRevenue);
      }
      
      this.chartData.week = {
        labels: labels,
        datasets: [
          {
            label: 'Fitness Packages',
            data: goiTapData,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          },
          {
            label: 'Services',
            data: dichVuData,
            backgroundColor: 'rgba(255, 206, 86, 0.2)',
            borderColor: 'rgba(255, 206, 86, 1)',
            borderWidth: 1
          },
          {
            label: 'Total',
            data: totalData,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2
          }
        ]
      };
    },
    
    // Prepare monthly chart data (last 12 months)
    prepareChartDataByMonth() {
      const endDate = new Date();
      const labels = [];
      const goiTapData = [];
      const dichVuData = [];
      const totalData = [];
      
      // Create array of months
      for (let m = 11; m >= 0; m--) {
        const monthStart = new Date(endDate.getFullYear(), endDate.getMonth() - m, 1);
        const monthEnd = new Date(endDate.getFullYear(), endDate.getMonth() - m + 1, 0);
        
        // Month label (e.g., "March 2024")
        const monthLabel = `${monthStart.toLocaleString('vi-VN', { month: 'long' })} ${monthStart.getFullYear()}`;
        labels.push(monthLabel);
        
        // Filter items for this month
        const monthItems = this.items.filter(item => {
          const itemDate = new Date(item.NgayTao);
          return itemDate >= monthStart && itemDate <= monthEnd;
        });
        
        // Calculate revenue for each category
        const goiTapRevenue = monthItems.reduce((total, item) => 
          total + this.getGoiTapPrice(item.GoiTap), 0);
        const dichVuRevenue = monthItems.reduce((total, item) => 
          total + this.getDichVuPrice(item.DichVu), 0);
        const totalRevenue = goiTapRevenue + dichVuRevenue;
        
        goiTapData.push(goiTapRevenue);
        dichVuData.push(dichVuRevenue);
        totalData.push(totalRevenue);
      }
      
      this.chartData.month = {
        labels: labels,
        datasets: [
          {
            label: 'Fitness Packages',
            data: goiTapData,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          },
          {
            label: 'Services',
            data: dichVuData,
            backgroundColor: 'rgba(255, 206, 86, 0.2)',
            borderColor: 'rgba(255, 206, 86, 1)',
            borderWidth: 1
          },
          {
            label: 'Total',
            data: totalData,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2
          }
        ]
      };
    },
    
    // Prepare yearly chart data (last 5 years)
    prepareChartDataByYear() {
      const currentYear = new Date().getFullYear();
      const labels = [];
      const goiTapData = [];
      const dichVuData = [];
      const totalData = [];
      
      // Create array of years
      for (let y = 4; y >= 0; y--) {
        const year = currentYear - y;
        const yearStart = new Date(year, 0, 1);
        const yearEnd = new Date(year, 11, 31, 23, 59, 59);
        
        labels.push(year.toString());
        
        // Filter items for this year
        const yearItems = this.items.filter(item => {
          const itemDate = new Date(item.NgayTao);
          return itemDate >= yearStart && itemDate <= yearEnd;
        });
        
        // Calculate revenue for each category
        const goiTapRevenue = yearItems.reduce((total, item) => 
          total + this.getGoiTapPrice(item.GoiTap), 0);
        const dichVuRevenue = yearItems.reduce((total, item) => 
          total + this.getDichVuPrice(item.DichVu), 0);
        const totalRevenue = goiTapRevenue + dichVuRevenue;
        
        goiTapData.push(goiTapRevenue);
        dichVuData.push(dichVuRevenue);
        totalData.push(totalRevenue);
      }
      
      this.chartData.year = {
        labels: labels,
        datasets: [
          {
            label: 'Fitness Packages',
            data: goiTapData,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          },
          {
            label: 'Services',
            data: dichVuData,
            backgroundColor: 'rgba(255, 206, 86, 0.2)',
            borderColor: 'rgba(255, 206, 86, 1)',
            borderWidth: 1
          },
          {
            label: 'Total',
            data: totalData,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2
          }
        ]
      };
    },
    
    // Calculate statistics
    // Calculate statistics
calculateStatistics() {
  // Today's date
  const today = new Date();
  const todayStr = today.toISOString().split('T')[0];
  
  // Yesterday's date
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);
  const yesterdayStr = yesterday.toISOString().split('T')[0];
  
  // Calculate revenue for today
  const todayItems = this.items.filter(item => {
    const itemDate = new Date(item.NgayTao).toISOString().split('T')[0];
    return itemDate === todayStr;
  });
  this.statistics.today = todayItems.reduce((total, item) => total + this.calculateTotal(item), 0);
  
  // Calculate revenue for yesterday
  const yesterdayItems = this.items.filter(item => {
    const itemDate = new Date(item.NgayTao).toISOString().split('T')[0];
    return itemDate === yesterdayStr;
  });
  const yesterdayRevenue = yesterdayItems.reduce((total, item) => total + this.calculateTotal(item), 0);
  
  // Calculate today's growth percentage
  this.statistics.todayGrowth = yesterdayRevenue === 0 ? 0 : 
    ((this.statistics.today - yesterdayRevenue) / yesterdayRevenue * 100).toFixed(1);
  
  // Calculate this week's revenue
  const startOfWeek = new Date(today);
  startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay());
  startOfWeek.setHours(0, 0, 0, 0);
  
  const weekItems = this.items.filter(item => {
    const itemDate = new Date(item.NgayTao);
    return itemDate >= startOfWeek && itemDate <= today;
  });
  this.statistics.thisWeek = weekItems.reduce((total, item) => total + this.calculateTotal(item), 0);
  
  // Calculate last week's revenue (7-13 days ago)
  const startOfLastWeek = new Date(startOfWeek);
  startOfLastWeek.setDate(startOfLastWeek.getDate() - 7);
  const endOfLastWeek = new Date(startOfWeek);
  endOfLastWeek.setDate(endOfLastWeek.getDate() - 1);
  endOfLastWeek.setHours(23, 59, 59, 999);
  
  const lastWeekItems = this.items.filter(item => {
    const itemDate = new Date(item.NgayTao);
    return itemDate >= startOfLastWeek && itemDate <= endOfLastWeek;
  });
  const lastWeekRevenue = lastWeekItems.reduce((total, item) => total + this.calculateTotal(item), 0);
  
  // Calculate this week's growth percentage
  this.statistics.weekGrowth = lastWeekRevenue === 0 ? 0 : 
    ((this.statistics.thisWeek - lastWeekRevenue) / lastWeekRevenue * 100).toFixed(1);
  
  // Calculate this month's revenue
  const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
  const monthItems = this.items.filter(item => {
    const itemDate = new Date(item.NgayTao);
    return itemDate >= startOfMonth && itemDate <= today;
  });
  this.statistics.thisMonth = monthItems.reduce((total, item) => total + this.calculateTotal(item), 0);
  
  // Calculate last month's revenue
  const startOfLastMonth = new Date(today.getFullYear(), today.getMonth() - 1, 1);
  const endOfLastMonth = new Date(today.getFullYear(), today.getMonth(), 0);
  endOfLastMonth.setHours(23, 59, 59, 999);
  
  const lastMonthItems = this.items.filter(item => {
    const itemDate = new Date(item.NgayTao);
    return itemDate >= startOfLastMonth && itemDate <= endOfLastMonth;
  });
  const lastMonthRevenue = lastMonthItems.reduce((total, item) => total + this.calculateTotal(item), 0);
  
  // Calculate this month's growth percentage
  this.statistics.monthGrowth = lastMonthRevenue === 0 ? 0 : 
    ((this.statistics.thisMonth - lastMonthRevenue) / lastMonthRevenue * 100).toFixed(1);
  
  // Calculate this year's revenue
  const startOfYear = new Date(today.getFullYear(), 0, 1);
  const yearItems = this.items.filter(item => {
    const itemDate = new Date(item.NgayTao);
    return itemDate >= startOfYear && itemDate <= today;
  });
  this.statistics.thisYear = yearItems.reduce((total, item) => total + this.calculateTotal(item), 0);
  
  // Calculate last year's revenue
  const startOfLastYear = new Date(today.getFullYear() - 1, 0, 1);
  const endOfLastYear = new Date(today.getFullYear() - 1, 11, 31);
  endOfLastYear.setHours(23, 59, 59, 999);
  
  const lastYearItems = this.items.filter(item => {
    const itemDate = new Date(item.NgayTao);
    return itemDate >= startOfLastYear && itemDate <= endOfLastYear;
  });
  const lastYearRevenue = lastYearItems.reduce((total, item) => total + this.calculateTotal(item), 0);
  
  // Calculate this year's growth percentage
  this.statistics.yearGrowth = lastYearRevenue === 0 ? 0 : 
    ((this.statistics.thisYear - lastYearRevenue) / lastYearRevenue * 100).toFixed(1);
}
  }
};
</script>


<style scoped>
.revenue-statistics {
  font-family: 'Roboto', sans-serif;
  color: #333;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 24px;
  color: #000;
}

/* Filter styles */
.filter-section {
  background-color: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

.filter-item label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
  color: #4b5563;
}

.filter-item input,
.filter-item select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 14px;
}

.filter-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.btn-primary,
.btn-secondary {
  padding: 8px 16px;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
  border: none;
}

.btn-primary:hover {
  background-color: #2563eb;
}

.btn-secondary {
  background-color: #6b7280;
  color: white;
  border: none;
}

.btn-secondary:hover {
  background-color: #4b5563;
}

/* Summary section styles */
.summary-section,
.chart-section,
.table-section {
  background-color: white;
  padding: 24px;
  border-radius: 8px;
  margin-bottom: 24px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 16px;
  color: #2c3e50;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 24px;
}

.stat-card {
  padding: 16px;
  border-radius: 8px;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-today {
  background-color: #e0f2fe;
}

.stat-week {
  background-color: #ecfdf5;
}

.stat-month {
  background-color: #f3e8ff;
}

.stat-year {
  background-color: #fff7ed;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 22px;
  font-weight: bold;
  color: #1e3a8a;
  margin-bottom: 8px;
}

.stat-today .stat-value {
  color: #1e40af;
}

.stat-week .stat-value {
  color: #065f46;
}

.stat-month .stat-value {
  color: #6b21a8;
}

.stat-year .stat-value {
  color: #9a3412;
}

.stat-change {
  font-size: 12px;
}

.positive {
  color: #059669;
}

.negative {
  color: #dc2626;
}

/* Chart styles */
.chart-period {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.period-btn {
  padding: 6px 12px;
  background-color: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}

.period-btn.active {
  background-color: #3b82f6;
  border-color: #2563eb;
  color: white;
}

.chart-container {
  height: 256px;
  background-color: #f9fafb;
  border-radius: 8px;
}

.chart-placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  font-size: 15px;
}

/* Table styles */
.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

th {
  background-color: #f9fafb;
  font-weight: 600;
  color: #4b5563;
}

tr:hover {
  background-color: #f9fafb;
}

.text-right {
  text-align: right;
}

.total-cost {
  font-weight: 600;
  color: #1e40af;
}

.total-sum {
  font-weight: 700;
  color: #1e3a8a;
}

.no-data {
  text-align: center;
  padding: 32px;
  color: #6b7280;
  font-style: italic;
}

/* Pagination styles */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
}

.pagination-info {
  font-size: 14px;
  color: #6b7280;
}

.pagination-controls {
  display: flex;
  gap: 8px;
}

.pagination-btn {
  padding: 6px 12px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background-color: white;
  color: #3b82f6;
  cursor: pointer;
}

.pagination-btn:hover:not(.disabled) {
  background-color: #f3f4f6;
}

.pagination-btn.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: #f3f4f6;
  color: #9ca3af;
}

/* Responsive styles */
@media (max-width: 768px) {
  .filter-grid {
    grid-template-columns: 1fr;
  }
  
  .summary-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .pagination {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
}
</style>