// WorkoutCalendar.vue
<template>
  <div class="workout-calendar">
    <div class="calendar-header">
      <h2>{{ getMonthName() }}</h2>
      <div>
        <button @click="prevMonth">←</button>
        <button @click="nextMonth">→</button>
      </div>
    </div>
    
    <div class="weekdays-grid">
      <div v-for="day in weekDays" :key="day" class="weekday">
        {{ day }}
      </div>
    </div>
    
    <div class="days-grid">
      <div 
        v-for="(day, index) in days" 
        :key="index" 
        :class="[
          'day-cell',
          day ? (isToday(day) ? 'today' : 'normal-day') : 'empty-day'
        ]"
      >
        <div v-if="day" class="day-number">{{ day.getDate() }}</div>
        <div 
          v-if="day && getWorkout(day)" 
          :class="[
            'workout-label',
            getWorkoutColor(getWorkout(day).type),
            getWorkout(day).completed ? 'completed' : ''
          ]"
          @click="toggleWorkoutCompletion(day)"
        >
          {{ getWorkout(day).type }}
        </div>
      </div>
    </div>
    
    <div class="legend">
      <div class="legend-item">
        <div class="legend-color cardio"></div>
        <span>Cardio</span>
      </div>
      <div class="legend-item">
        <div class="legend-color strength"></div>
        <span>Sức mạnh</span>
      </div>
      <div class="legend-item">
        <div class="legend-color yoga"></div>
        <span>Yoga</span>
      </div>
      <div class="legend-item">
        <div class="legend-color rest"></div>
        <span>Nghỉ ngơi</span>
      </div>
      <div class="legend-item">
        <div class="legend-color completed-marker"></div>
        <span>Đã hoàn thành</span>
      </div>
    </div>

    <!-- Thông báo đề xuất lịch tập -->
    <div v-if="showSuggestionMessage" class="suggestion-message">
      {{ suggestionMessage }}
      <button @click="showSuggestionMessage = false" class="close-button">
        Đóng
      </button>
    </div>
    
    <!-- Cài đặt tự động đề xuất -->
    <div class="settings-section">
      <div class="settings-header">
        <h3>Cài đặt đề xuất tự động</h3>
        <button 
          @click="suggestWorkoutSchedule" 
          class="suggest-button"
        >
          Tạo đề xuất ngay
        </button>
      </div>
      
      <div class="setting-item">
        <input 
          type="checkbox" 
          id="autoSuggest" 
          v-model="autoSuggestEnabled" 
          @change="saveSettings"
        >
        <label for="autoSuggest">Tự động đề xuất lịch tập</label>
      </div>
      
      <div class="setting-item">
        <input 
          type="checkbox" 
          id="adjustForMissed" 
          v-model="adjustForMissedWorkouts" 
          @change="saveSettings"
        >
        <label for="adjustForMissed">Điều chỉnh theo bài tập đã bỏ lỡ</label>
      </div>
      
      <div class="setting-item">
        <span>Đề xuất trước:</span>
        <select 
          v-model="daysToSuggestAhead" 
          class="days-select"
          @change="saveSettings"
        >
          <option value="7">7 ngày</option>
          <option value="14">14 ngày</option>
          <option value="30">30 ngày</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WorkoutCalendar',
  data() {
    return {
      currentDate: new Date(),
      weekDays: ['CN', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7'],
      workoutData: {
        "2025-03-24": { type: "Cardio", completed: true },
        "2025-03-25": { type: "Sức mạnh", completed: true },
        "2025-03-26": { type: "Nghỉ ngơi", completed: true },
        "2025-03-27": { type: "Cardio", completed: false },
        "2025-03-28": { type: "Sức mạnh", completed: false },
        "2025-03-29": { type: "Yoga", completed: false },
        "2025-03-30": { type: "Nghỉ ngơi", completed: false },
        "2025-03-31": { type: "Cardio", completed: false },
        "2025-04-01": { type: "Sức mạnh", completed: false },
        "2025-04-02": { type: "Yoga", completed: false }
      },
      workoutTypes: ["Cardio", "Sức mạnh", "Yoga", "Nghỉ ngơi"],
      showSuggestionMessage: false,
      suggestionMessage: "",
      // Cài đặt tự động đề xuất
      autoSuggestEnabled: true,
      adjustForMissedWorkouts: true,
      daysToSuggestAhead: 14,
      // Lưu trữ dữ liệu người dùng
      userStats: {
        preferredWorkouts: {},
        completionRate: {},
        missedWorkouts: []
      },
      // Theo dõi lần cuối đề xuất
      lastSuggestionDate: null
    }
  },
  computed: {
    days() {
      return this.getDaysInMonth(
        this.currentDate.getFullYear(),
        this.currentDate.getMonth()
      );
    }
  },
  created() {
    // Tải cài đặt người dùng khi component được tạo
    this.loadSettings();
    // Tính toán thống kê người dùng
    this.calculateUserStats();
    // Kiểm tra và tạo đề xuất tự động nếu cần
    this.checkAutoSuggestion();
  },
  methods: {
    getDaysInMonth(year, month) {
      const date = new Date(year, month, 1);
      const days = [];
      
      const firstDayIndex = new Date(year, month, 1).getDay();
      for (let i = 0; i < firstDayIndex; i++) {
        days.push(null);
      }
      
      while (date.getMonth() === month) {
        days.push(new Date(date));
        date.setDate(date.getDate() + 1);
      }
      
      return days;
    },
    getMonthName() {
      const options = { month: 'long', year: 'numeric' };
      return this.currentDate.toLocaleDateString('vi-VN', options);
    },
    prevMonth() {
      this.currentDate = new Date(
        this.currentDate.getFullYear(),
        this.currentDate.getMonth() - 1,
        1
      );
    },
    nextMonth() {
      this.currentDate = new Date(
        this.currentDate.getFullYear(),
        this.currentDate.getMonth() + 1,
        1
      );
    },
    formatDate(date) {
      if (!date) return '';
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
    getWorkout(date) {
      const dateStr = this.formatDate(date);
      return this.workoutData[dateStr];
    },
    getWorkoutColor(type) {
      switch (type) {
        case 'Cardio': return 'cardio';
        case 'Sức mạnh': return 'strength';
        case 'Yoga': return 'yoga';
        case 'Nghỉ ngơi': return 'rest';
        default: return '';
      }
    },
    isToday(date) {
      return date.toDateString() === new Date().toDateString();
    },
    
    // Đánh dấu hoàn thành / chưa hoàn thành
    toggleWorkoutCompletion(date) {
      const dateStr = this.formatDate(date);
      if (this.workoutData[dateStr]) {
        this.workoutData[dateStr].completed = !this.workoutData[dateStr].completed;
        // Cập nhật thống kê người dùng
        this.calculateUserStats();
        // Lưu dữ liệu
        this.saveWorkoutData();
        // Kiểm tra nếu cần đề xuất lại
        if (this.adjustForMissedWorkouts) {
          this.checkAutoSuggestion(true);
        }
      }
    },
    
    // Lưu cài đặt người dùng
    saveSettings() {
      localStorage.setItem('workoutCalendarSettings', JSON.stringify({
        autoSuggestEnabled: this.autoSuggestEnabled,
        adjustForMissedWorkouts: this.adjustForMissedWorkouts,
        daysToSuggestAhead: this.daysToSuggestAhead,
        lastSuggestionDate: this.lastSuggestionDate
      }));
    },
    
    // Tải cài đặt người dùng
    loadSettings() {
      const savedSettings = localStorage.getItem('workoutCalendarSettings');
      if (savedSettings) {
        const settings = JSON.parse(savedSettings);
        this.autoSuggestEnabled = settings.autoSuggestEnabled;
        this.adjustForMissedWorkouts = settings.adjustForMissedWorkouts;
        this.daysToSuggestAhead = settings.daysToSuggestAhead;
        this.lastSuggestionDate = settings.lastSuggestionDate;
      }
      
      // Tải dữ liệu lịch tập
      const savedWorkoutData = localStorage.getItem('workoutData');
      if (savedWorkoutData) {
        this.workoutData = JSON.parse(savedWorkoutData);
      }
    },
    
    // Lưu dữ liệu lịch tập
    saveWorkoutData() {
      localStorage.setItem('workoutData', JSON.stringify(this.workoutData));
    },
    
    // Tính toán thống kê người dùng
    calculateUserStats() {
      const stats = {
        preferredWorkouts: {},
        completionRate: {},
        missedWorkouts: []
      };
      
      // Tính toán thống kê
      let totalWorkouts = 0;
      let completedWorkouts = 0;
      
      for (const dateStr in this.workoutData) {
        const workout = this.workoutData[dateStr];
        const date = new Date(dateStr);
        const today = new Date();
        
        // Không tính workouts trong tương lai
        if (date <= today) {
          // Đếm loại tập luyện ưa thích
          if (!stats.preferredWorkouts[workout.type]) {
            stats.preferredWorkouts[workout.type] = 0;
          }
          stats.preferredWorkouts[workout.type]++;
          
          // Tính tỷ lệ hoàn thành
          if (workout.type !== "Nghỉ ngơi") {
            totalWorkouts++;
            if (workout.completed) {
              completedWorkouts++;
            } else {
              // Lưu các bài tập bị bỏ lỡ
              stats.missedWorkouts.push({
                date: dateStr,
                type: workout.type,
                dayOfWeek: date.getDay()
              });
            }
          }
        }
      }
      
      // Tính tỷ lệ hoàn thành theo loại
      for (const dateStr in this.workoutData) {
        const workout = this.workoutData[dateStr];
        const date = new Date(dateStr);
        const today = new Date();
        
        if (date <= today && workout.type !== "Nghỉ ngơi") {
          if (!stats.completionRate[workout.type]) {
            stats.completionRate[workout.type] = { total: 0, completed: 0 };
          }
          stats.completionRate[workout.type].total++;
          if (workout.completed) {
            stats.completionRate[workout.type].completed++;
          }
        }
      }
      
      // Tính tỷ lệ hoàn thành theo ngày trong tuần
      for (const dateStr in this.workoutData) {
        const workout = this.workoutData[dateStr];
        const date = new Date(dateStr);
        const today = new Date();
        const dayOfWeek = date.getDay();
        
        if (date <= today && workout.type !== "Nghỉ ngơi") {
          if (!stats.completionRate[`day${dayOfWeek}`]) {
            stats.completionRate[`day${dayOfWeek}`] = { total: 0, completed: 0 };
          }
          stats.completionRate[`day${dayOfWeek}`].total++;
          if (workout.completed) {
            stats.completionRate[`day${dayOfWeek}`].completed++;
          }
        }
      }
      
      this.userStats = stats;
    },
    
    // Kiểm tra và tạo đề xuất tự động nếu cần
    checkAutoSuggestion(forceCheck = false) {
      if (!this.autoSuggestEnabled && !forceCheck) return;
      
      const today = new Date();
      const lastDate = this.getLastScheduledDate();
      
      // Nếu không có dữ liệu gần đây hoặc đã đến lúc đề xuất mới
      const needNewSuggestion = !lastDate || 
        (today.getTime() + (this.daysToSuggestAhead * 24 * 60 * 60 * 1000) > lastDate.getTime());
      
      // Tạo đề xuất nếu cần thiết
      if (needNewSuggestion || forceCheck) {
        this.suggestWorkoutSchedule();
      }
    },
    
    // Lấy ngày cuối cùng trong lịch
    getLastScheduledDate() {
      const dates = Object.keys(this.workoutData).sort();
      if (dates.length === 0) return null;
      
      const lastDateStr = dates[dates.length - 1];
      return new Date(lastDateStr);
    },
    
    // Tạo đề xuất lịch tập
    suggestWorkoutSchedule() {
      // Tìm ngày cuối cùng trong lịch tập hiện tại
      const dates = Object.keys(this.workoutData).sort();
      let lastDate = dates.length > 0 ? new Date(dates[dates.length - 1]) : new Date();
      
      // Nếu ngày cuối cùng trong quá khứ, bắt đầu từ ngày hiện tại
      const today = new Date();
      if (lastDate < today) {
        lastDate = today;
      }
      
      // Tạo lịch tập mới
      const newSchedule = this.generateSmartSchedule(lastDate);
      
      // Cập nhật workoutData với lịch mới
      this.workoutData = { ...this.workoutData, ...newSchedule };
      
      // Cập nhật ngày đề xuất cuối cùng
      this.lastSuggestionDate = new Date();
      
      // Lưu dữ liệu
      this.saveWorkoutData();
      this.saveSettings();
      
      // Hiển thị thông báo
      this.showSuggestionMessage = true;
      this.suggestionMessage = "Đã tạo lịch tập mới dựa trên thói quen và tình trạng tập luyện của bạn!";
      
      // Ẩn thông báo sau 5 giây
      setTimeout(() => {
        this.showSuggestionMessage = false;
      }, 5000);
    },
    
    // Phân tích mẫu lịch tập hiện tại
    analyzeWorkoutPattern() {
      const pattern = {
        dayPatterns: Array(7).fill(null),
        preferredSequence: [],
        avoidedDays: []
      };
      
      // Xác định các mẫu theo ngày trong tuần
      const dayWorkouts = Array(7).fill().map(() => ({}));
      
      for (const dateStr in this.workoutData) {
        const date = new Date(dateStr);
        const dayOfWeek = date.getDay();
        const workout = this.workoutData[dateStr];
        
        if (!dayWorkouts[dayOfWeek][workout.type]) {
          dayWorkouts[dayOfWeek][workout.type] = 0;
        }
        dayWorkouts[dayOfWeek][workout.type]++;
      }
      
      // Xác định loại tập phổ biến nhất cho mỗi ngày
      for (let i = 0; i < 7; i++) {
        const types = dayWorkouts[i];
        let maxCount = 0;
        let preferredType = null;
        
        for (const type in types) {
          if (types[type] > maxCount) {
            maxCount = types[type];
            preferredType = type;
          }
        }
        
        if (preferredType && maxCount >= 2) {
          pattern.dayPatterns[i] = preferredType;
        }
      }
      
      // Xác định các ngày có tỷ lệ hoàn thành thấp
      for (const key in this.userStats.completionRate) {
        if (key.startsWith('day')) {
          const dayIndex = parseInt(key.replace('day', ''));
          const rate = this.userStats.completionRate[key];
          
          if (rate.total >= 3 && rate.completed / rate.total < 0.5) {
            pattern.avoidedDays.push(dayIndex);
          }
        }
      }
      
      return pattern;
    },
    
    // Tạo lịch tập thông minh dựa trên dữ liệu người dùng
    generateSmartSchedule(startDate) {
      const newSchedule = {};
      const pattern = this.analyzeWorkoutPattern();
      
      // Xác định các loại tập có tỷ lệ hoàn thành cao
      const workoutCompletionRates = {};
      for (const type in this.userStats.completionRate) {
        if (!type.startsWith('day')) {
          const rate = this.userStats.completionRate[type];
          if (rate.total > 0) {
            workoutCompletionRates[type] = rate.completed / rate.total;
          }
        }
      }
      
      // Xác định các bài tập bị bỏ lỡ để thêm vào lịch
      const missedWorkoutTypes = [];
      if (this.adjustForMissedWorkouts && this.userStats.missedWorkouts.length > 0) {
        this.userStats.missedWorkouts.forEach(workout => {
          if (workout.type !== "Nghỉ ngơi") {
            missedWorkoutTypes.push(workout.type);
          }
        });
      }
      
      // Tạo lịch tập cho số ngày được chỉ định
      for (let i = 1; i <= parseInt(this.daysToSuggestAhead); i++) {
        const newDate = new Date(startDate);
        newDate.setDate(newDate.getDate() + i);
        const dayOfWeek = newDate.getDay();
        const dateStr = this.formatDate(newDate);
        
        // Kiểm tra nếu ngày đã có lịch tập
        if (this.workoutData[dateStr]) continue;
        
        let workoutType;
        
        // Ưu tiên 1: Bù các bài tập đã bỏ lỡ
        if (this.adjustForMissedWorkouts && missedWorkoutTypes.length > 0 && !pattern.avoidedDays.includes(dayOfWeek)) {
          workoutType = missedWorkoutTypes.shift();
        }
        // Ưu tiên 2: Tuân theo mẫu ngày trong tuần nếu có
        else if (pattern.dayPatterns[dayOfWeek]) {
          workoutType = pattern.dayPatterns[dayOfWeek];
        }
        // Ưu tiên 3: Sử dụng thuật toán thông minh
        else {
          workoutType = this.getSmartWorkoutRecommendation(newDate, newSchedule, workoutCompletionRates);
        }
        
        // Thêm vào lịch mới
        newSchedule[dateStr] = {
          type: workoutType,
          completed: false
        };
      }
      
      return newSchedule;
    },
    
    // Đề xuất bài tập thông minh dựa trên nhiều yếu tố
    getSmartWorkoutRecommendation(date, newSchedule, completionRates) {
      const dayOfWeek = date.getDay();
      const yesterday = new Date(date);
      yesterday.setDate(date.getDate() - 1);
      const yesterdayStr = this.formatDate(yesterday);
      
      // Lấy thông tin về bài tập ngày hôm trước
      const prevWorkout = newSchedule[yesterdayStr] || this.workoutData[yesterdayStr];
      
      // Lấy các loại tập có tỷ lệ hoàn thành cao nhất
      let preferredTypes = Object.keys(completionRates).sort((a, b) => completionRates[b] - completionRates[a]);
      
      // Nếu không có đủ dữ liệu, sử dụng các loại mặc định
      if (preferredTypes.length < 2) {
        preferredTypes = this.workoutTypes.filter(type => type !== "Nghỉ ngơi");
      }
      
      // Quy tắc đề xuất thông minh
      
      // Quy tắc 1: Chủ nhật thường là ngày nghỉ ngơi
      if (dayOfWeek === 0) {
        return "Nghỉ ngơi";
      }
      
      // Quy tắc 2: Không đặt bài tập cường độ cao hai ngày liên tiếp
      if (prevWorkout) {
        if ((prevWorkout.type === "Cardio" || prevWorkout.type === "Sức mạnh")) {
          // Nếu hôm trước tập nặng, hôm nay nên tập nhẹ hoặc nghỉ
          return Math.random() > 0.3 ? "Yoga" : "Nghỉ ngơi";
        }
        
        if (prevWorkout.type === "Yoga") {
          // Sau Yoga có thể tập nặng
          return preferredTypes[0] === "Yoga" ? "Cardio" : preferredTypes[0];
        }
        
        if (prevWorkout.type === "Nghỉ ngơi") {
          // Sau ngày nghỉ, nên tập bài tập yêu thích
          return preferredTypes[0];
        }
      }
      
      // Quy tắc 3: Phân bổ đều các loại tập trong tuần
      // Đếm số lượng mỗi loại tập trong 7 ngày gần nhất
      const recentWorkouts = this.getRecentWorkoutCounts(date);
      
      // Chọn loại tập ít xuất hiện nhất
      const leastFrequent = Object.keys(recentWorkouts)
        .filter(type => type !== "Nghỉ ngơi")
        .sort((a, b) => recentWorkouts[a] - recentWorkouts[b])[0];
      
      if (leastFrequent) {
        return leastFrequent;
      }
      
      // Quy tắc 4: Mặc định đến loại tập có tỷ lệ hoàn thành cao nhất
      return preferredTypes[0];
    },
    
    // Lấy số lượng từng loại tập trong 7 ngày gần đây
    getRecentWorkoutCounts(date) {
      const counts = {};
      this.workoutTypes.forEach(type => {
        counts[type] = 0;
      });
      
      // Tìm trong 7 ngày gần đây
      for (let i = 1; i <= 7; i++) {
        const pastDate = new Date(date);
        pastDate.setDate(date.getDate() - i);
        const pastDateStr = this.formatDate(pastDate);
        
        if (this.workoutData[pastDateStr]) {
          counts[this.workoutData[pastDateStr].type]++;
        }
      }
      
      return counts;
    }
  }
}
</script>

<style>

/* WorkoutCalendar.vue CSS */
.workout-calendar {
  font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
  width: 100%; /* Fill parent width */
  height: 100%; /* Fill parent height */
  max-width: none; /* Remove max-width constraint */
  margin: 0; /* Remove margins */
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  box-sizing: border-box; /* Include padding in width/height calculation */
}

/* Calendar header styling */
.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.calendar-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.5rem;
  text-transform: capitalize;
}

.calendar-header button {
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  font-size: 1rem;
  cursor: pointer;
  margin: 0 5px;
  transition: background-color 0.2s;
}

.calendar-header button:hover {
  background-color: #3a7bc8;
}

/* Weekdays grid */
.weekdays-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
  margin-bottom: 5px;
}

.weekday {
  text-align: center;
  font-weight: bold;
  padding: 10px 0;
  background-color: #4a90e2;
  color: white;
  border-radius: 5px;
}

/* Days grid */
.days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
  margin-bottom: 20px;
}

.day-cell {
  min-height: 80px;
  border-radius: 5px;
  padding: 5px;
  position: relative;
}

.empty-day {
  background-color: #eaeaea;
}

.normal-day {
  background-color: white;
  border: 1px solid #ddd;
}

.today {
  background-color: #f0f8ff;
  border: 2px solid #4a90e2;
}

.day-number {
  font-size: 0.9rem;
  font-weight: bold;
  color: #555;
  margin-bottom: 5px;
}

/* Workout labels */
.workout-label {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 30px;
  border-radius: 5px;
  color: white;
  font-size: 0.9rem;
  cursor: pointer;
  margin-top: 8px;
  transition: transform 0.2s;
}

.workout-label:hover {
  transform: scale(1.05);
}

.cardio {
  background-color: #ff7675;
}

.strength {
  background-color: #74b9ff;
}

.yoga {
  background-color: #55efc4;
  color: #333;
}

.rest {
  background-color: #a29bfe;
}

.completed {
  position: relative;
}

.completed::after {
  content: '✓';
  position: absolute;
  right: 8px;
  font-weight: bold;
  color: white;
}

/* Legend */
.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin: 15px 0 25px;
  padding: 10px;
  background-color: white;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-right: 10px;
}

.legend-color {
  width: 20px;
  height: 20px;
  border-radius: 3px;
  margin-right: 5px;
}

.completed-marker {
  background-color: #ddd;
  position: relative;
}

.completed-marker::after {
  content: '✓';
  position: absolute;
  right: 3px;
  top: -2px;
  font-weight: bold;
  color: #333;
  font-size: 0.9rem;
}

/* Suggestion message */
.suggestion-message {
  position: relative;
  padding: 15px;
  background-color: #55efc4;
  color: #333;
  border-radius: 5px;
  margin: 20px 0;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.5s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.close-button {
  position: absolute;
  right: 10px;
  top: 10px;
  background: none;
  border: none;
  color: #333;
  cursor: pointer;
  font-weight: bold;
}

.close-button:hover {
  color: #000;
}

/* Settings section */
.settings-section {
  background-color: white;
  border-radius: 5px;
  padding: 15px;
  border: 1px solid #ddd;
}

.settings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.settings-header h3 {
  margin: 0;
  color: #333;
}

.suggest-button {
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.suggest-button:hover {
  background-color: #3a7bc8;
}

.setting-item {
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.setting-item input[type="checkbox"] {
  margin-right: 10px;
}

.setting-item label {
  cursor: pointer;
}

.days-select {
  margin-left: 10px;
  padding: 5px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

/* Responsive styles */
@media (max-width: 768px) {
  .workout-calendar {
    padding: 10px;
  }
  
  .days-grid {
    gap: 3px;
  }
  
  .day-cell {
    min-height: 60px;
  }
  
  .day-number {
    font-size: 0.8rem;
  }
  
  .workout-label {
    font-size: 0.8rem;
    height: 25px;
  }
  
  .legend {
    flex-direction: column;
    gap: 8px;
  }
}

@media (max-width: 480px) {
  .weekday {
    font-size: 0.8rem;
    padding: 5px 0;
  }
  
  .day-cell {
    min-height: 50px;
  }
  
  .settings-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .suggest-button {
    margin-top: 10px;
  }
}
</style>