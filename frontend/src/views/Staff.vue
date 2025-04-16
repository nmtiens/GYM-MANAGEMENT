<template>
  <div class="dashboard-container">
    <!-- Navigation Bar -->
    <nav class="main-navigation">
      <div class="nav-logo">
        <span class="logo-icon">💼</span>
        <span class="logo-text">Thu Ngân - Hội Viên</span>
      </div>

      <div class="nav-menu">
        <div 
          v-for="(item, index) in menuItems" 
          :key="index"
          class="nav-item"
          :class="{ 'active': selectedComponent === item.component }"
          @click="selectedComponent = item.component"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-label">{{ item.label }}</span>
        </div>
      </div>

      <div class="nav-actions">
        <div class="user-profile">
      
          <div class="logout-button" @click="logout">
            <span class="logout-icon">🚪</span>
            <span class="logout-text">Đăng xuất</span>
          </div>
        </div>
      </div>
    </nav>

    <!-- Content Area -->
    <main class="content-area">
      <div class="component-wrapper">
        <transition name="fade" mode="out-in">
          <component :is="selectedComponent" />
        </transition>
      </div>
    </main>
  </div>
</template>

<script>
import HoiVien from "@/components/HoiVien.vue";
import TheHoiVien from "@/components/TheHoiVien.vue";
import DangKy from "@/components/Register.vue";
import DangNhap from "@/components/Login.vue";

export default {
  components: { HoiVien, TheHoiVien, DangKy, DangNhap },
  data() {
    return {
      userAvatar: "/avatar-placeholder.jpg",
      selectedComponent: "HoiVien",
      searchQuery: "",
      menuItems: [
        { 
          component: "HoiVien", 
          label: "Danh sách hội viên", 
          icon: "👥" 
        },
        { 
          component: "TheHoiVien", 
          label: "Quản lý thẻ", 
          icon: "💳" 
        },
        { 
          component: "DangKy", 
          label: "Đăng ký hội viên", 
          icon: "🆕" 
        },
        { 
          component: "DangNhap", 
          label: "Điểm danh", 
          icon: "📋" 
        }
      ]
    };
  },
  computed: {
    getCurrentPageTitle() {
      const currentItem = this.menuItems.find(
        item => item.component === this.selectedComponent
      );
      return currentItem ? currentItem.label : "Quản Lý Hội Viên";
    }
  },
  methods: {
    logout() {
      // Implement logout logic here
      // For example:
      // - Clear localStorage/sessionStorage tokens
      // - Reset user state
      // - Redirect to login page
      
      // Example implementation:
      localStorage.removeItem('authToken');
      // Redirect to login page
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.dashboard-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: 'Roboto', sans-serif;
  background-color: #f5f7fa;
}

.main-navigation {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.nav-logo {
  display: flex;
  align-items: center;
}

.logo-icon {
  font-size: 1.8rem;
  margin-right: 12px;
  color: #3b82f6;
}

.logo-text {
  font-weight: bold;
  font-size: 1.2rem;
  color: #1e3a8a;
}

.nav-menu {
  display: flex;
  align-items: center;
  background-color: #f1f5f9;
  border-radius: 8px;
  padding: 5px;
}

.nav-item {
  display: flex;
  align-items: center;
  margin: 0 5px;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background-color: #e2e8f0;
}

.nav-item.active {
  background-color: #3b82f6;
  color: white;
}

.nav-icon {
  margin-right: 8px;
  font-size: 1.1rem;
}

.nav-actions {
  display: flex;
  align-items: center;
}

.search-box {
  position: relative;
  margin-right: 20px;
}

.search-box input {
  padding: 10px 12px 10px 38px;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  width: 250px;
  background-color: #f8fafc;
  transition: all 0.3s ease;
}

.search-box input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
  width: 280px;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #64748b;
}

.user-profile {
  display: flex;
  align-items: center;
  background-color: #f1f5f9;
  padding: 6px 12px;
  border-radius: 30px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
  border: 2px solid #3b82f6;
}

.user-info {
  display: flex;
  flex-direction: column;
  margin-right: 12px;
}

.username {
  font-weight: 600;
  font-size: 0.9rem;
  color: #1e293b;
}

.status {
  font-size: 0.7rem;
  color: #10b981;
}

.logout-button {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 6px 12px;
  background-color: #dc2626;  /* Bright red background */
  border-radius: 20px;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(220, 38, 38, 0.2);
}

.logout-button:hover {
  background-color: #b91c1c;  /* Darker red on hover */
  box-shadow: 0 2px 6px rgba(185, 28, 28, 0.3);
  transform: translateY(-1px);
}

.logout-icon {
  font-size: 1rem;
  margin-right: 6px;
  color: white;  /* White icon */
}

.logout-text {
  font-size: 0.8rem;
  font-weight: 500;
  color: white;  /* White text */
}
.content-area {
  flex-grow: 1;
  padding: 20px 30px;
  overflow-y: auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn span {
  margin-right: 6px;
}

.btn.primary {
  background-color: #3b82f6;
  color: white;
}

.btn.primary:hover {
  background-color: #2563eb;
}

.btn.secondary {
  background-color: #f1f5f9;
  color: #475569;
}

.btn.secondary:hover {
  background-color: #e2e8f0;
}

.quick-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  font-size: 2rem;
  margin-right: 16px;
  background-color: #f1f5f9;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-weight: bold;
  font-size: 1.5rem;
  color: #1e293b;
}

.stat-label {
  font-size: 0.8rem;
  color: #64748b;
}

.component-wrapper {
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  min-height: 500px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

@media (max-width: 1024px) {
  .quick-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .nav-label {
    display: none;
  }
  
  .nav-icon {
    margin-right: 0;
    font-size: 1.2rem;
  }
  
  .nav-item {
    padding: 10px;
  }
}

@media (max-width: 768px) {
  .action-buttons {
    display: none;
  }
  
  .user-info {
    display: none;
  }
  
  .logout-text {
    display: none;
  }
  
  .logout-button {
    padding: 6px;
  }
  
  .search-box input {
    width: 150px;
  }
  
  .search-box input:focus {
    width: 180px;
  }
}
</style>