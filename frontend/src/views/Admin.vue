<template>
  <div class="admin-dashboard">
    <!-- Navigation Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-content">
        <h2 class="logo">Fitness Admin</h2>
        <nav>
          <ul>
            <li 
              v-for="item in menuItems" 
              :key="item.component"
              @click="selectedComponent = item.component"
              :class="{ active: selectedComponent === item.component }"
            >
              <span>{{ item.label }}</span>
            </li>
          </ul>
        </nav>
      </div>
      <button class="logout-btn" @click="logout">
        Đăng Xuất
      </button>
    </aside>

    <!-- Main Content Area -->
    <main class="content">
      <header class="content-header">
        <h1>Dashboard</h1>
        <div class="quick-stats">
          <div 
            v-for="(stat, index) in stats" 
            :key="index" 
            class="stat-item"
          >
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </div>
      </header>

      <div class="dynamic-content">
        <component :is="selectedComponent" />
      </div>
    </main>
  </div>
</template>

<script>
import axios from "axios";
import { useRouter } from "vue-router";
import HoiVien from "@/components/HoiVien.vue";
import NhanVien from "@/components/NhanVien.vue";
import HLV from "@/components/HuanLuyenVien.vue";
import GoiTap from "@/components/GoiTap.vue";
import DichVu from "@/components/DichVu.vue";
import TheHoiVien from "@/components/TheHoiVien.vue";
import ThongKe from "@/components/ThongKe.vue";

export default {
  components: { 
    HoiVien, NhanVien, HLV, 
    GoiTap, DichVu, TheHoiVien, ThongKe 
  },
  data() {
    return {
      selectedComponent: "HoiVien",
      menuItems: [
        { component: "HoiVien", label: "Hội Viên" },
        { component: "NhanVien", label: "Nhân Viên" },
        { component: "HLV", label: "Huấn Luyện Viên" },
        { component: "GoiTap", label: "Gói Tập" },
        { component: "DichVu", label: "Dịch Vụ" },
        { component: "TheHoiVien", label: "Thẻ Hội Viên" },
        { component: "ThongKe", label: "Thống Kê Doanh Thu" }
      ],
      stats: [
        { label: "Hội Viên", value: 0 },
        { label: "Nhân Viên", value: 0 },
        { label: "HLV", value: 0 },
        { label: "Gói Tập", value: 0 },
        { label: "Dịch Vụ", value: 0 },
        { label: "Thẻ Hội Viên", value: 0 }
      ],
    };
  },
  mounted() {
    this.fetchStats();
  },
  methods: {
    async fetchStats() {
      try {
        const collections = ["HoiVien", "NhanVien", "HuanLuyenVien", "GoiTap", "DichVu", "TheHoiVien"];
        const responses = await Promise.all(
          collections.map((collection) =>
            axios.get(`http://localhost:5000/api/count/${collection}`)
          )
        );

        this.stats = responses.map((response, index) => ({
          label: collections[index].replace(/([A-Z])/g, " $1").trim(),
          value: response.data.count
        }));
      } catch (error) {
        console.error("Failed to fetch stats:", error);
      }
    },
    logout() {
       localStorage.removeItem('authToken');
  localStorage.removeItem('tokenExpiry');
  localStorage.removeItem('userRole');
      this.$router.push("/");
    }
  }
};
</script>

<style scoped>
.admin-dashboard {
  display: flex;
  height: 100vh;
  background-color: #f4f7f9;
  font-family: 'Inter', sans-serif;
}

/* Sidebar Styling */
.sidebar {
  width: 250px;
  background-color: #ffffff;
  border-right: 1px solid #e6e9ec;
  display: flex;
  flex-direction: column;
  padding: 30px 0;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.05);
}

.sidebar-content {
  flex-grow: 1;
}

.logo {
  text-align: center;
  color: #2c3e50;
  font-size: 1.5rem;
  margin-bottom: 40px;
  font-weight: 700;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar ul li {
  padding: 12px 25px;
  cursor: pointer;
  color: #7f8c8d;
  transition: all 0.3s ease;
  position: relative;
}

.sidebar ul li:hover, .sidebar ul li.active {
  background-color: #f1f4f7;
  color: #2980b9;
}

.sidebar ul li.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background-color: #2980b9;
}

.logout-btn {
  margin: 20px;
  padding: 10px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-btn:hover {
  background-color: #c0392b;
}

/* Main Content Styling */
.content {
  flex-grow: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.content-header {
  padding: 30px;
  background-color: white;
  border-bottom: 1px solid #e6e9ec;
}

.content-header h1 {
  margin-bottom: 20px;
  color: #2c3e50;
  font-size: 1.8rem;
}

.quick-stats {
  display: flex;
  gap: 20px;
}

.stat-item {
  background-color: #f1f4f7;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  flex: 1;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2980b9;
}

.stat-label {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-top: 5px;
}

.dynamic-content {
  flex-grow: 1;
  overflow-y: auto;
  padding: 30px;
  background-color: #f4f7f9;
}
</style>  