<template>
  <div class="dashboard">
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Đang tải dữ liệu...</p>
    </div>
    
    <template v-else>
      <!-- Sidebar -->
      <div class="sidebar">
        <div class="sidebar-header">
          <div class="logo">
            <span class="logo-text">FITNESS CLUB</span>
          </div>
        </div>
        
        <div class="user-profile">
          <div class="avatar-container">
            <div v-if="hasProfileImage" class="avatar-image">
              <img :src="profileImageUrl" alt="Profile Image">
            </div>
            <div v-else class="avatar">{{ userInitials }}</div>
          </div>
          <div class="user-details">
            <h3>{{ userData.fullName || 'Hội viên' }}</h3>
            <span class="membership-badge">{{ membershipData.GoiTap || 'Chưa có gói' }}</span>
          </div>
        </div>

        <div class="menu">
          <div 
            v-for="(item, index) in menuItems" 
            :key="index"
            :class="['menu-item', { active: activeMenu === item.id }]"
            @click="activeMenu = item.id"
          >
            <div class="menu-icon">
              <i :class="item.icon"></i>
            </div>
            <span class="menu-text">{{ item.name }}</span>
          </div>
        </div>
      </div>
      
      <!-- Main Content -->
      <div class="main">
        <div class="top-header">
          <div class="page-title">
            <h1>{{ getPageTitle() }}</h1>
          </div>
          <div class="header-actions">
            
            <button class="logout-btn" @click="logout">
              <i class="fas fa-sign-out-alt"></i>
            </button>
          </div>
        </div>
        
        <div class="content-container">
          <!-- Dashboard Overview -->
          <div v-if="activeMenu === 'dashboard'" class="dashboard-overview">
            <div class="welcome-card">
              <h2>Xin chào, {{ userData.fullName || 'Hội viên' }}!</h2>
              <p>Chào mừng quay trở lại với buổi tập của bạn. Hôm nay là ngày tốt để tiếp tục hành trình fitness của bạn.</p>
            </div>
            
            <div class="stats-grid">
              <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-calendar-check"></i></div>
                <div class="stat-info">
                  <h3>{{ membershipData.SoNgayConLai  || 0 }}</h3>
                  <p>Buổi tập còn lại</p>
                </div>
              </div>
              
              <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-fire"></i></div>
                <div class="stat-info">
                  <h3>{{ calculateMonthlyProgress() }}%</h3>
                  <p>Mục tiêu tháng</p>
                </div>
              </div>
              
              <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-dumbbell"></i></div>
                <div class="stat-info">
                  <h3>{{ getSessionsThisWeek() }}</h3>
                  <p>Buổi tập tuần này</p>
                </div>
              </div>
              
              <div class="stat-card">
  <div class="stat-icon"><i class="fas fa-clock"></i></div>
  <div class="stat-info">
    <h3>{{ formatVietnameseDate(membershipData.endDate) }}</h3>
    <p>Ngày hết hạn gói tập</p>
  </div>
</div>
            </div>
            
            <div class="recent-activity">
              <h3 class="section-title">Lịch sử tập gần đây</h3>
              <div class="activity-list">
                <div v-if="!membershipData.Login_History || membershipData.Login_History.length === 0" class="no-activity">
                  Chưa có buổi tập nào được ghi nhận
                </div>
                <div 
                  v-else 
                  v-for="session in groupLoginHistoryByDate().slice(0, 5)" 
                  :key="session.id" 
                  class="activity-item"
                >
                  <div class="activity-date">
                    <div class="date-circle">{{ formatDate(session.date).day }}</div>
                    <div class="date-month">{{ formatDate(session.date).month }}</div>
                  </div>
                  <div class="activity-info">
                    <div class="activity-name">Buổi tập {{ session.sessionCount > 1 ? '(' + session.sessionCount + ' lần check-in)' : '' }}</div>
                    <div class="activity-time">
                      {{ formatTime(session.firstLogin) }} - {{ formatTime(session.lastLogin) }}
                    </div>
                  </div>
                  <div class="activity-duration">
                    <i class="fas fa-clock"></i> {{ session.duration }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Nutrition Advice -->
          <div v-if="activeMenu === 'nutrition'" class="content-section">
            <NutritionAdvice :userId="userData.id" />
          </div>
          
          <!-- Body Measurement -->
          <div v-if="activeMenu === 'measurement'" class="content-section">
            <BodyMeasurement :userId="userData.id" />
          </div>
          
          <!-- Package Info -->
          <div v-if="activeMenu === 'package'" class="content-section">
            <InfoGoiTap :packageInfo="membershipData" />
          </div>
          
          <!-- Trainer Info -->
          <div v-if="activeMenu === 'trainer'" class="content-section">
            <InfoHLV :trainerId="userData.trainerId" />
          </div>
          
          <!-- Schedule Info -->
          <div v-if="activeMenu === 'schedule'" class="content-section">
            <LichTap :trainerId="userData.trainerId" />
          </div>
          
          <!-- Training Programs -->
          <div v-if="activeMenu === 'programs'" class="content-section">
            <BaiTap :userId="userData.id" />
          </div>
          
         
        </div>
      </div>
      
  
      
      <!-- Floating Chatbot Panel -->
         <div class="chatbot-panel-content">
          <Chatbot :userId="userData.id" :userName="userData.fullName" :compact="true" />
        </div>
    </template>
  </div>
</template>

<script>
import NutritionAdvice from '@/components/NutritionAdvice.vue'
import BodyMeasurement from '@/components/BodyMeasurement.vue'
import InfoGoiTap from '@/components/InfoGoiTap.vue'
import InfoHLV from '@/components/InfoHLV.vue'
import LichTap from '@/components/LichTap.vue'
import BaiTap from '@/components/BaiTap.vue'
import Chatbot from '@/components/Chatbot.vue'
import axios from 'axios'

export default {
  name: 'UserDashboard',
  components: {
    NutritionAdvice,
    BodyMeasurement,
    InfoGoiTap,
    InfoHLV,
    LichTap,
    BaiTap,
    Chatbot
  },
  data() {
    return {
      loading: true,
      activeMenu: 'dashboard',
      isChatbotOpen: false,
      userData: {
        id: null,
        fullName: '',
        trainerId: null,
        Face_Images: []
      },
      membershipData: {
        GoiTap: '',
        SoNgayConLai: 0,
        startDate: '',
        endDate: '',
        remainingSessions: 0,
        features: [],
        Login_History: []
      },
      trainingHistory: [],
      menuItems: [
        { id: 'dashboard', name: 'Tổng quan', icon: 'fas fa-home' },
        { id: 'nutrition', name: 'Dinh dưỡng', icon: 'fas fa-apple-alt' },
        { id: 'measurement', name: 'Số đo cơ thể', icon: 'fas fa-weight' },
        { id: 'package', name: 'Gói tập', icon: 'fas fa-award' },
        { id: 'trainer', name: 'Huấn luyện viên', icon: 'fas fa-user-shield' },
        { id: 'schedule', name: 'Lịch tập', icon: 'fas fa-calendar-alt' },
        { id: 'programs', name: 'Bài tập', icon: 'fas fa-dumbbell' }
      ]
    }
  },
  computed: {
    userInitials() {
      if (!this.userData.fullName) return '?';
      return this.userData.fullName
        .split(' ')
        .map(name => name.charAt(0))
        .join('')
        .substring(0, 2)
        .toUpperCase();
    },
    
    hasProfileImage() {
      return this.userData && 
            this.userData.Face_Images && 
            Array.isArray(this.userData.Face_Images) &&
            this.userData.Face_Images.length > 0 &&
            this.userData.Face_Images[0] !== null &&
            this.userData.Face_Images[0] !== undefined;
    },

    profileImageUrl() {
      if (!this.hasProfileImage) return null;
      
      const imageData = this.userData.Face_Images[0];
      
      // Check if data is null or undefined
      if (!imageData) return null;
      
      // Check if it's already a full URL
      if (typeof imageData === 'string') {
        // If it already includes the data:image prefix
        if (imageData.startsWith('data:image')) {
          return imageData;
        }
        
        // If it's an http/https URL
        if (imageData.startsWith('http')) {
          return imageData;
        }
        
        // Assume it's base64 if it's a long string
        if (imageData.length > 100) {
          return `data:image/jpeg;base64,${imageData}`;
        }
      }
      
      // If it's an object with url or src
      if (typeof imageData === 'object' && imageData !== null) {
        if (imageData.url) return imageData.url;
        if (imageData.src) return imageData.src;
        if (imageData.data) return `data:image/jpeg;base64,${imageData.data}`;
      }
      
      // If format can't be determined
      console.log('Unable to format image data:', imageData);
      return null;
    }
  },
  created() {
    this.loadUserData();
  },
  methods: {
    async loadUserData() {
      try {
        this.loading = true;
        
        // Check for token in localStorage
        const token = localStorage.getItem('token');
        if (!token) {
          this.$router.push('/login');
          return;
        }
        
        // Get saved user information
        const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
        
        // Initialize userData with currentUser info
        this.userData = {
          id: currentUser.id || null,
          fullName: currentUser.username || '',
          trainerId: null,
          Face_Images: []
        };
        
        console.log('Current user data:', currentUser);
        
        if (!this.userData.id) {
          console.error('User ID is missing');
          this.$router.push('/login');
          return;
        }
        
        const config = {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        };
        
        // Get detailed member information
        try {
          const userResponse = await axios.get(`http://localhost:5000/${this.userData.id}`, config);
          if (userResponse.data) {
            this.userData = {
              ...this.userData,
              fullName: userResponse.data.HoTen || this.userData.fullName,
              trainerId: userResponse.data.MaHLV || null,
              Face_Images: userResponse.data.Face_Images || []
            };
          }
        } catch (error) {
          console.warn('Could not fetch user data:', error);
        }
        
        // Get membership card information
        try {
          const membershipResponse = await axios.get(`http://localhost:5000/thehoivien/member/${this.userData.id}`, config);
          console.log('Raw membership response:', membershipResponse);
          
          if (membershipResponse.data) {
            // Check data structure
            if (membershipResponse.data.memberCard) {
              // Case when API returns {"memberCard": {...}}
              const cardData = membershipResponse.data.memberCard;
              this.membershipData = {
                GoiTap: cardData.GoiTap || '',
                SoNgayConLai: cardData.SoNgayConLai || 0,
                startDate: cardData.NgayBatDau || '',
                endDate: cardData.NgayHetHan || '',
                features: cardData.Features || [],
                Login_History: cardData.Login_History || [],
                Face_Images: membershipResponse.data.Face_Images || [] 
              };
            } else {
              // Case when API returns data directly
              this.membershipData = {
                GoiTap: membershipResponse.data.GoiTap || '',
                SoNgayConLai: membershipResponse.data.SoNgayConLai || 0,
                remainingSessions: membershipResponse.data.SoBuoiConLai || 0,
                startDate: membershipResponse.data.NgayBatDau || '',
                endDate: membershipResponse.data.NgayHetHan || '',
                features: membershipResponse.data.Features || [],
                Login_History: membershipResponse.data.Login_History || [],
                Face_Images: membershipResponse.data.Face_Images || [] 
              };
            }

            if (this.membershipData.Face_Images && 
                Array.isArray(this.membershipData.Face_Images) && 
                this.membershipData.Face_Images.length > 0) {
              this.userData.Face_Images = this.membershipData.Face_Images;
            }
            console.log('Membership data after processing:', this.membershipData);
            console.log('Login history:', this.membershipData.Login_History);
          }
        } catch (error) {
          console.error('Error fetching membership card information:', 
            error.response ? error.response.data : error.message);
        }
        
      } catch (error) {
        console.error('Error loading user data:', error);
        if (error.response && error.response.status === 401) {
          localStorage.removeItem('token');
          localStorage.removeItem('currentUser');
          this.$router.push('/login');
        }
      } finally {
        this.loading = false;
      }
    },

   // Thêm phương thức formatVietnameseDate với thứ
  formatVietnameseDate(dateString) {
    if (!dateString) return 'Chưa có thông tin';
    
    const date = new Date(dateString);
    
    // Kiểm tra nếu ngày không hợp lệ
    if (isNaN(date.getTime())) return 'Ngày không hợp lệ';
    
    const day = date.getDate();
    const month = date.getMonth() + 1; // Tháng bắt đầu từ 0
    const year = date.getFullYear();
    
    // Lấy thứ trong tuần
    const weekday = date.getDay(); // 0 = Chủ Nhật, 1 = Thứ Hai, ...
    const weekdayNames = [
      'Chủ Nhật', 'Thứ Hai', 'Thứ Ba', 'Thứ Tư', 
      'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy'
    ];
    const weekdayName = weekdayNames[weekday];
    
    // Format: Thứ X, ngày DD tháng MM năm YYYY
    return `${weekdayName}, ngày ${day} tháng ${month} năm ${year}`;
  },
    
    getPageTitle() {
      const activePage = this.menuItems.find(item => item.id === this.activeMenu);
      return activePage ? activePage.name : 'Tổng quan';
    },
    
    groupLoginHistoryByDate() {
      if (!this.membershipData.Login_History || this.membershipData.Login_History.length === 0) {
        return [];
      }
      
      // Sort login times from newest to oldest
      const sortedLogins = [...this.membershipData.Login_History].sort((a, b) => {
        return new Date(b) - new Date(a);
      });
      
      // Group by date (YYYY-MM-DD)
      const groupedSessions = [];
      let currentDate = null;
      let currentDateSessions = [];
      
      sortedLogins.forEach(loginTime => {
        const date = new Date(loginTime);
        const dateString = date.toISOString().split('T')[0]; // Get YYYY-MM-DD
        
        if (dateString !== currentDate) {
          if (currentDate !== null) {
            // Add the previous date's sessions to our result
            groupedSessions.push({
              date: currentDate,
              sessions: currentDateSessions
            });
          }
          
          // Start a new date group
          currentDate = dateString;
          currentDateSessions = [loginTime];
        } else {
          // Add to current date group
          currentDateSessions.push(loginTime);
        }
      });
      
      // Add the last group
      if (currentDate !== null) {
        groupedSessions.push({
          date: currentDate,
          sessions: currentDateSessions
        });
      }
      
      // Transform to the format needed for display
  return groupedSessions.map((group, index) => {
  const sessionDate = new Date(group.date);
  // Sắp xếp lại các session theo thời gian
  const sortedSessions = [...group.sessions].sort((a, b) => new Date(a) - new Date(b));
  
  return {
    id: index,
    date: sessionDate,
    sessionCount: Math.floor(group.sessions.length / 2), // Đếm số phiên tập (mỗi phiên 2 lần check)
    firstLogin: new Date(sortedSessions[0]), // Thời gian check đầu tiên trong ngày
    lastLogin: new Date(sortedSessions[sortedSessions.length - 1]), // Thời gian check cuối cùng trong ngày
    duration: this.calculateSessionDuration(group.sessions)
  };
});
    },
    
calculateSessionDuration(sessions) {
  // Nếu không có sessions hoặc mảng rỗng
  if (!sessions || sessions.length === 0) {
    return "0 phút";
  }
  
  // Sắp xếp thời gian đăng nhập theo thứ tự thời gian
  const sortedSessions = [...sessions].sort((a, b) => new Date(a) - new Date(b));
  
  // Nhóm các session thành các phiên tập (mỗi phiên bao gồm check-in và check-out)
  // Giả định mỗi cặp check liên tiếp là một phiên nếu thời gian giữa chúng < 2 giờ
  const workoutSessions = [];
  let currentSession = [sortedSessions[0]];
  
  for (let i = 1; i < sortedSessions.length; i++) {
    const currentTime = new Date(sortedSessions[i]);
    const prevTime = new Date(sortedSessions[i-1]);
    const timeDiff = currentTime - prevTime;
    
    // Nếu thời gian giữa hai lần check nhỏ hơn 2 giờ (7.200.000ms), 
    // coi như cùng một phiên tập
    if (timeDiff < 7200000) {
      currentSession.push(sortedSessions[i]);
    } else {
      // Kết thúc phiên hiện tại và bắt đầu phiên mới
      if (currentSession.length >= 2) {
        workoutSessions.push({
          start: new Date(currentSession[0]),
          end: new Date(currentSession[currentSession.length - 1])
        });
      }
      currentSession = [sortedSessions[i]];
    }
  }
  
  // Thêm phiên cuối cùng nếu có
  if (currentSession.length >= 2) {
    workoutSessions.push({
      start: new Date(currentSession[0]),
      end: new Date(currentSession[currentSession.length - 1])
    });
  }
  
  // Tính tổng thời lượng các phiên tập
  let totalDuration = 0;
  workoutSessions.forEach(session => {
    totalDuration += session.end - session.start;
  });
  
  // Nếu không có phiên tập hợp lệ, trả về giá trị mặc định
  if (totalDuration === 0 || workoutSessions.length === 0) {
    return "60 phút";
  }
  
  // Tính toán phút và làm tròn
  const durationMinutes = Math.round(totalDuration / (1000 * 60));
  
  return `${durationMinutes} phút`;
},
    calculateMonthlyProgress() {
      // Giả sử mục tiêu tháng là 12 buổi tập
      const totalMonthlyTarget = 30;
      
      // Get grouped sessions
      const sessions = this.groupLoginHistoryByDate();
      
      // Đếm số buổi tập trong tháng hiện tại
      const currentMonth = new Date().getMonth();
      const currentYear = new Date().getFullYear();
      
      const sessionsThisMonth = sessions.filter(session => {
        return session.date.getMonth() === currentMonth && session.date.getFullYear() === currentYear;
      }).length;
      
      const progress = Math.min(Math.round((sessionsThisMonth / totalMonthlyTarget) * 100), 100);
      return progress;
    },
    
    getSessionsThisWeek() {
      const today = new Date();
      
      // Define the start of week as Monday of the current week
      const startOfWeek = new Date(today);
      // If today is Sunday (0), go back 6 days to get to Monday
      // Otherwise, go back to (day of week - 1) to reach Monday
      const dayOfWeek = today.getDay(); // 0 = Sunday, 1 = Monday, etc.
      const daysToSubtract = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
      startOfWeek.setDate(today.getDate() - daysToSubtract);
      startOfWeek.setHours(0, 0, 0, 0);
      
      const sessions = this.groupLoginHistoryByDate();
      const sessionsThisWeek = sessions.filter(session => {
        const sessionDate = new Date(session.date);
        sessionDate.setHours(0, 0, 0, 0);
        return sessionDate.getTime() >= startOfWeek.getTime();
      }).length;
      
      return sessionsThisWeek;
    },
    
    formatDate(dateString) {
      const date = new Date(dateString);
      const day = date.getDate();
      const month = date.toLocaleString('vi-VN', { month: 'short' });
      
      return { day, month };
    },
    
    formatTime(dateString) {
      const date = new Date(dateString);
      return date.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
    },
    
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('currentUser');
      this.$router.push('/');
    },
    
    toggleChatbot() {
      this.isChatbotOpen = !this.isChatbotOpen;
    }
  }
}
</script>

<style scoped>
/* CSS remains unchanged */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.dashboard {
  display: flex;
  width: 100%;
  min-height: 100vh;
  font-family: 'Montserrat', sans-serif;
  color: #333;
  background-color: #f4f7fa;
}

/* Loading styles */
.loading-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100vh;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #38b2ac;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Sidebar Styles */
.sidebar {
  width: 280px;
  background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
  color: #fff;
  display: flex;
  flex-direction: column;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
}

.sidebar-header {
  padding: 25px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 1px;
}

.logo-text {
  background: linear-gradient(45deg, #38b2ac, #4fd1c5);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent; /* For browsers that don't support -webkit-text-fill-color */
}

.user-profile {
  display: flex;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.avatar-container {
  margin-right: 15px;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(45deg, #38b2ac, #4fd1c5);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 18px;
  color: #fff;
}

.user-details {
  flex: 1;
}

.user-details h3 {
  font-size: 16px;
  margin-bottom: 5px;
  font-weight: 600;
}

.membership-badge {
  font-size: 12px;
  background-color: rgba(56, 178, 172, 0.2);
  color: #4fd1c5;
  padding: 3px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.menu {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 12px 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin: 2px 0;
  border-left: 3px solid transparent;
}

.menu-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.menu-item.active {
  background-color: rgba(255, 255, 255, 0.1);
  border-left: 3px solid #4fd1c5;
}

.menu-icon {
  margin-right: 15px;
  width: 20px;
  text-align: center;
}

.menu-text {
  font-weight: 500;
  font-size: 14px;
}

/* Main Content Styles */
.main {
  flex: 1;
  margin-left: 280px;
  padding: 20px;
  overflow: auto;
}

.top-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e2e8f0;
}

.page-title h1 {
  font-size: 24px;
  font-weight: 600;
  color: #1a202c;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.notification-btn, .settings-btn, .logout-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #fff;
  border: none;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.logout-btn {
  color: #e53e3e;
}

.notification-btn:hover, .settings-btn:hover, .logout-btn:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.content-container {
  margin-top: 20px;
}

/* Dashboard Overview Styles */
.welcome-card {
  background-color: #fff;
  border-radius: 10px;
  padding: 25px;
  margin-bottom: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.welcome-card h2 {
  font-size: 20px;
  margin-bottom: 10px;
  color: #2d3748;
}

.welcome-card p {
  color: #718096;
  line-height: 1.6;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: #fff;
  border-radius: 10px;
  padding: 25px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: linear-gradient(45deg, rgba(56, 178, 172, 0.2), rgba(79, 209, 197, 0.2));
  display: flex;
  align-items: center;
  justify-content: center;
  color: #38b2ac;
  font-size: 18px;
  margin-right: 15px;
}

.stat-info h3 {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 5px;
  color: #2d3748;
}

.stat-info p {
  font-size: 13px;
  color: #718096;
}

.content-section {
  background-color: #fff;
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

/* Recent activity */
.recent-activity {
  background-color: #fff;
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.section-title {
  margin-bottom: 20px;
  font-size: 18px;
  color: #2d3748;
  font-weight: 600;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.no-activity {
  color: #718096;
  font-style: italic;
  text-align: center;
  padding: 20px 0;
}

.activity-item {
  display: flex;
  align-items: center;
  padding: 15px;
  background-color: #f8fafc;
  border-radius: 8px;
  transition: transform 0.2s;
}

.activity-item:hover {
  transform: translateX(5px);
  background-color: #f0f9ff;
}

.activity-date {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 20px;
}

.date-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #38b2ac;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 16px;
}

.date-month {
  font-size: 12px;
  margin-top: 4px;
  color: #718096;
}

.activity-info {
  flex: 1;
}

.activity-name {
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 4px;
}

.activity-time {
  font-size: 12px;
  color: #718096;
}

.activity-duration {
  font-size: 13px;
  color: #38b2ac;
  font-weight: 500;
}

@media (max-width: 1024px) {
  .sidebar {
    width: 220px;
  }
  
  .main {
    margin-left: 220px;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .sidebar {
    width: 80px;
    overflow-x: hidden;
  }
  
  .sidebar-header, .user-profile {
    align-items: center;
    justify-content: center;
    padding: 15px 5px;
  }
  
  .logo-text, .user-details {
    display: none;
  }
  
  .menu-text {
    display: none;
  }
  
  .menu-item {
    justify-content: center;
    padding: 15px 5px;
  }
  
  .menu-icon {
    margin-right: 0;
  }
  
  .main {
    margin-left: 80px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}

.avatar-container {
  margin-right: 15px;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(45deg, #38b2ac, #4fd1c5);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 18px;
  color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.avatar-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.avatar-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.user-details {
  flex: 1;
}

.user-details h3 {
  font-size: 16px;
  margin-bottom: 5px;
  font-weight: 600;
  color: #fff;
}

.membership-badge {
  font-size: 12px;
  background-color: rgba(56, 178, 172, 0.2);
  color: #4fd1c5;
  padding: 3px 8px;
  border-radius: 12px;
  font-weight: 500;
  display: inline-block;
}
</style>