// ExerciseList.vue
<template>
  <div class="exercise-list">
    <h2>Danh sách bài tập</h2>
    
    <div class="filter-buttons">
      <button 
        @click="filter = 'all'" 
        :class="['filter-button', filter === 'all' ? 'filter-active' : '']"
      >
        Tất cả
      </button>
      <button 
        @click="filter = 'completed'" 
        :class="['filter-button', filter === 'completed' ? 'filter-active' : '']"
      >
        Đã hoàn thành
      </button>
      <button 
        @click="filter = 'pending'" 
        :class="['filter-button', filter === 'pending' ? 'filter-active' : '']"
      >
        Chưa hoàn thành
      </button>
    </div>
    
    <div class="exercises-container">
      <div 
        v-for="exercise in filteredExercises" 
        :key="exercise.id"
        class="exercise-item"
      >
        <div class="exercise-header" @click="toggleExpand(exercise.id)">
          <div class="exercise-title">
            <div 
              :class="['category-dot', getCategoryClass(exercise.category)]"
            ></div>
            <h3>{{ exercise.name }}</h3>
            <span 
              :class="['category-tag', getCategoryTagClass(exercise.category)]"
            >
              {{ exercise.category }}
            </span>
          </div>
          
          <div class="exercise-status">
            <span 
              :class="['status-tag', exercise.completed ? 'status-completed' : 'status-pending']"
            >
              {{ exercise.completed ? 'Hoàn thành' : 'Chưa hoàn thành' }}
            </span>
            <span class="expand-icon">
              {{ expandedId === exercise.id ? '▲' : '▼' }}
            </span>
          </div>
        </div>
        
        <div v-if="expandedId === exercise.id" class="exercise-details">
          <p class="exercise-description">{{ exercise.description }}</p>
          <div class="exercise-stats">
            <div v-if="exercise.duration" class="stat-item">
              <span class="stat-label">Thời gian:</span>
              {{ exercise.duration }} phút
            </div>
            <div v-if="exercise.sets" class="stat-item">
              <span class="stat-label">Số hiệp:</span>
              {{ exercise.sets }}
            </div>
            <div v-if="exercise.reps" class="stat-item">
              <span class="stat-label">Số lần:</span>
              {{ exercise.reps }}
            </div>
            <div class="stat-item">
              <span class="stat-label">Calories:</span>
              {{ exercise.calories }}
            </div>
          </div>
          
          <div class="action-buttons">
            <button 
              @click="toggleComplete(exercise.id)"
              :class="['toggle-button', exercise.completed ? 'toggle-completed' : 'toggle-pending']"
            >
              {{ exercise.completed ? 'Đánh dấu chưa hoàn thành' : 'Đánh dấu hoàn thành' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="filteredExercises.length === 0" class="empty-message">
      Không có bài tập nào {{ filter === 'completed' ? 'đã hoàn thành' : filter === 'pending' ? 'chưa hoàn thành' : '' }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExerciseList',
  data() {
    return {
      filter: 'all',
      expandedId: null,
      exercises: [
        {
          id: 1,
          name: "Chạy bộ",
          category: "Cardio",
          duration: 30,
          calories: 300,
          description: "Chạy với tốc độ vừa phải",
          completed: false
        },
        {
          id: 2,
          name: "Gập bụng",
          category: "Sức mạnh",
          reps: 3,
          sets: 15,
          calories: 120,
          description: "Tập trung vào cơ bụng",
          completed: true
        },
        {
          id: 3,
          name: "Hít đất",
          category: "Sức mạnh",
          reps: 3,
          sets: 10,
          calories: 150,
          description: "Giữ cơ thể thẳng",
          completed: false
        },
        {
          id: 4,
          name: "Yoga buổi sáng",
          category: "Yoga",
          duration: 20,
          calories: 180,
          description: "Các tư thế cơ bản để khởi động ngày mới",
          completed: true
        },
        {
          id: 5,
          name: "Squat",
          category: "Sức mạnh",
          reps: 3,
          sets: 12,
          calories: 200,
          description: "Tập trung vào nhóm cơ chân",
          completed: false
        }
      ]
    }
  },
  computed: {
    filteredExercises() {
      if (this.filter === 'all') return this.exercises;
      return this.exercises.filter(ex => 
        this.filter === 'completed' ? ex.completed : !ex.completed
      );
    }
  },
  methods: {
    toggleExpand(id) {
      this.expandedId = this.expandedId === id ? null : id;
    },
    toggleComplete(id) {
      const exercise = this.exercises.find(ex => ex.id === id);
      if (exercise) {
        exercise.completed = !exercise.completed;
      }
    },
    getCategoryClass(category) {
      switch (category) {
        case 'Cardio': return 'category-cardio';
        case 'Sức mạnh': return 'category-strength';
        case 'Yoga': return 'category-yoga';
        default: return 'category-default';
      }
    },
    getCategoryTagClass(category) {
      switch (category) {
        case 'Cardio': return 'tag-cardio';
        case 'Sức mạnh': return 'tag-strength';
        case 'Yoga': return 'tag-yoga';
        default: return 'tag-default';
      }
    }
  }
}
</script>

<style>
/* ExerciseList.css */
.exercise-list {
  font-family: 'Roboto', sans-serif;
  width: 100%; /* Fill parent width */
  height: 100%; /* Fill parent height */
  max-width: none; /* Remove max-width constraint */
  margin: 0; /* Remove auto margins */
  padding: 1rem;
  background-color: #ffffff;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  box-sizing: border-box; /* Include padding in width/height calculation */
}


.exercise-list h2 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.filter-buttons {
  display: flex;
  margin-bottom: 1rem;
}

.filter-buttons > * + * {
  margin-left: 0.5rem;
}

.filter-button {
  padding-left: 0.75rem;
  padding-right: 0.75rem;
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  background-color: #e5e7eb;
  transition: opacity 0.2s;
}

.filter-button:hover {
  opacity: 0.9;
}

.filter-active {
  background-color: #3b82f6;
  color: #ffffff;
}

.exercises-container > * + * {
  margin-top: 0.75rem;
}

.exercise-item {
  border-width: 1px;
  border-style: solid;
  border-color: #e5e7eb;
  border-radius: 0.25rem;
  padding: 0.75rem;
}

.exercise-item:hover {
  border-color: #d1d5db;
}

.exercise-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.exercise-title {
  display: flex;
  align-items: center;
}

.category-dot {
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 9999px;
  margin-right: 0.5rem;
}

.category-cardio {
  background-color: #ef4444;
}

.category-strength {
  background-color: #3b82f6;
}

.category-yoga {
  background-color: #10b981;
}

.category-default {
  background-color: #6b7280;
}

.exercise-title h3 {
  font-weight: 500;
}

.category-tag {
  margin-left: 0.5rem;
  font-size: 0.75rem;
  padding-left: 0.5rem;
  padding-right: 0.5rem;
  padding-top: 0.125rem;
  padding-bottom: 0.125rem;
  border-radius: 0.25rem;
}

.tag-cardio {
  background-color: #fee2e2;
  color: #991b1b;
}

.tag-strength {
  background-color: #dbeafe;
  color: #1e40af;
}

.tag-yoga {
  background-color: #d1fae5;
  color: #065f46;
}

.tag-default {
  background-color: #f3f4f6;
  color: #1f2937;
}

.exercise-status {
  display: flex;
  align-items: center;
}

.status-tag {
  font-size: 0.75rem;
  padding-left: 0.5rem;
  padding-right: 0.5rem;
  padding-top: 0.125rem;
  padding-bottom: 0.125rem;
  border-radius: 0.25rem;
  margin-right: 0.5rem;
}

.status-completed {
  background-color: #d1fae5;
  color: #065f46;
}

.status-pending {
  background-color: #fef3c7;
  color: #92400e;
}

.expand-icon {
  color: #6b7280;
}

.exercise-details {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top-width: 1px;
  border-top-style: solid;
  border-top-color: #e5e7eb;
  font-size: 0.875rem;
}

.exercise-description {
  margin-bottom: 0.5rem;
}

.exercise-stats {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.5rem;
}

.stat-item {
  display: flex;
  align-items: center;
}

.stat-label {
  color: #6b7280;
  margin-right: 0.25rem;
}

.action-buttons {
  margin-top: 0.75rem;
  display: flex;
  justify-content: flex-end;
}

.toggle-button {
  padding-left: 0.75rem;
  padding-right: 0.75rem;
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  transition: opacity 0.2s;
}

.toggle-button:hover {
  opacity: 0.9;
}

.toggle-completed {
  background-color: #f59e0b;
  color: #ffffff;
}

.toggle-pending {
  background-color: #10b981;
  color: #ffffff;
}

.empty-message {
  text-align: center;
  padding-top: 1rem;
  padding-bottom: 1rem;
  color: #6b7280;
}

/* Animations */
.detail-enter-active,
.detail-leave-active {
  transition: max-height 0.3s ease, opacity 0.3s ease;
  max-height: 500px;
  overflow: hidden;
}

.detail-enter,
.detail-leave-to {
  max-height: 0;
  opacity: 0;
}
</style>