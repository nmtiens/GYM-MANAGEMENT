<template>
  <div class="container">
    <h1 class="title">Tính toán chỉ số cơ thể</h1>
    
    <div class="card">
      <h2 class="subtitle">Thông tin cá nhân</h2>
      
      <div class="form-grid">
        <div class="form-group">
          <label>Giới tính:</label>
          <select v-model="gender">
            <option value="male">Nam</option>
            <option value="female">Nữ</option>
          </select>
        </div>
        
        <div class="form-group">
          <label>Tuổi:</label>
          <input type="number" v-model="age" />
        </div>
        
        <div class="form-group">
          <label>Chiều cao (cm):</label>
          <input type="number" v-model="height" />
        </div>
        
        <div class="form-group">
          <label>Cân nặng (kg):</label>
          <input type="number" v-model="weight" />
        </div>
        
        <div class="form-group">
          <label>Số đo vòng eo (cm):</label>
          <input type="number" v-model="waistCircumference" />
        </div>
        
        <div class="form-group">
          <label>Số đo vòng hông (cm):</label>
          <input type="number" v-model="hipCircumference" />
        </div>
        
        <div class="form-group">
          <label>Số đo vòng cổ (cm):</label>
          <input type="number" v-model="neckCircumference" />
        </div>
        
        <div class="form-group">
          <label>Mức độ hoạt động:</label>
          <select v-model="activityLevel">
            <option value="1.2">Ít vận động (công việc văn phòng)</option>
            <option value="1.375">Nhẹ nhàng (tập luyện 1-3 ngày/tuần)</option>
            <option value="1.55">Vừa phải (tập luyện 3-5 ngày/tuần)</option>
            <option value="1.725">Nặng (tập luyện 6-7 ngày/tuần)</option>
            <option value="1.9">Rất nặng (tập luyện 2 lần/ngày)</option>
          </select>
        </div>
      </div>
      
      <div class="form-group button-group">
        <button @click="calculateMetrics" class="button primary">Tính toán</button>
        <button @click="resetResults" class="button secondary" v-if="showResults">Reset kết quả</button>
      </div>
      
      <div v-if="showResults" class="results">
        <h2 class="subtitle">Kết quả</h2>
        
        <div class="metrics-grid">
          <div class="metric-card" :class="getBMIClass">
            <h3>BMI (Chỉ số khối cơ thể)</h3>
            <div class="metric-value">{{ bmi.toFixed(2) }}</div>
            <div class="metric-status">{{ getBMIStatus }}</div>
          </div>
          
          <div class="metric-card" :class="getBFPClass">
            <h3>BFP (Tỷ lệ mỡ cơ thể)</h3>
            <div class="metric-value">{{ bodyFatPercentage.toFixed(2) }}%</div>
            <div class="metric-status">{{ getBFPStatus }}</div>
          </div>
          
          <div class="metric-card">
            <h3>BMR (Tỷ lệ trao đổi chất cơ bản)</h3>
            <div class="metric-value">{{ bmr.toFixed(0) }} kcal</div>
          </div>
          
          <div class="metric-card">
            <h3>TDEE (Tổng năng lượng tiêu thụ hàng ngày)</h3>
            <div class="metric-value">{{ tdee.toFixed(0) }} kcal</div>
          </div>
          
          <div class="metric-card" :class="getWHRClass">
            <h3>WHR (Tỷ lệ eo-hông)</h3>
            <div class="metric-value">{{ waistToHipRatio.toFixed(2) }}</div>
            <div class="metric-status">{{ getWHRStatus }}</div>
          </div>
        </div>
        
        <div class="recommendations">
          <h2 class="subtitle">Phân tích và đề xuất</h2>
          <div class="recommendation-content">
            <h3>Đánh giá chung</h3>
            <p>{{ overallAssessment }}</p>
            
            <h3>Đề xuất chế độ dinh dưỡng</h3>
            <p>{{ nutritionRecommendation }}</p>
            
            <h3>Đề xuất bài tập</h3>
            <p>{{ exerciseRecommendation }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      gender: 'male',
      age: 30,
      height: 170,
      weight: 70,
      waistCircumference: 80,
      hipCircumference: 100,
      neckCircumference: 35,
      activityLevel: '1.55',
      
      // Kết quả
      bmi: 0,
      bodyFatPercentage: 0,
      bmr: 0,
      tdee: 0,
      waistToHipRatio: 0,
      
      showResults: false,
      overallAssessment: '',
      nutritionRecommendation: '',
      exerciseRecommendation: ''
    };
  },
  
  computed: {
    getBMIStatus() {
      if (this.bmi < 18.5) return 'Thiếu cân';
      if (this.bmi < 25) return 'Bình thường';
      if (this.bmi < 30) return 'Thừa cân';
      return 'Béo phì';
    },
    
    getBMIClass() {
      if (this.bmi < 18.5) return 'warning';
      if (this.bmi < 25) return 'success';
      if (this.bmi < 30) return 'warning';
      return 'danger';
    },
    
    getBFPStatus() {
      if (this.gender === 'male') {
        if (this.bodyFatPercentage < 6) return 'Quá thấp';
        if (this.bodyFatPercentage < 14) return 'Người lực sĩ';
        if (this.bodyFatPercentage < 18) return 'Phù hợp';
        if (this.bodyFatPercentage < 25) return 'Trung bình';
        return 'Cao';
      } else {
        if (this.bodyFatPercentage < 16) return 'Quá thấp';
        if (this.bodyFatPercentage < 24) return 'Người lực sĩ';
        if (this.bodyFatPercentage < 30) return 'Phù hợp';
        if (this.bodyFatPercentage < 32) return 'Trung bình';
        return 'Cao';
      }
    },
    
    getBFPClass() {
      if (this.gender === 'male') {
        if (this.bodyFatPercentage < 6) return 'warning';
        if (this.bodyFatPercentage < 18) return 'success';
        if (this.bodyFatPercentage < 25) return 'warning';
        return 'danger';
      } else {
        if (this.bodyFatPercentage < 16) return 'warning';
        if (this.bodyFatPercentage < 30) return 'success';
        if (this.bodyFatPercentage < 32) return 'warning';
        return 'danger';
      }
    },
    
    getWHRStatus() {
      if (this.gender === 'male') {
        if (this.waistToHipRatio <= 0.95) return 'Tốt';
        return 'Nguy cơ cao';
      } else {
        if (this.waistToHipRatio <= 0.80) return 'Tốt';
        return 'Nguy cơ cao';
      }
    },
    
    getWHRClass() {
      if (this.gender === 'male') {
        return this.waistToHipRatio <= 0.95 ? 'success' : 'danger';
      } else {
        return this.waistToHipRatio <= 0.80 ? 'success' : 'danger';
      }
    }
  },
  
  methods: {
    calculateMetrics() {
      // Kiểm tra dữ liệu nhập hợp lệ
      if (!this.validateInputs()) {
        return;
      }
      
      // Tính BMI
      this.bmi = this.weight / ((this.height / 100) ** 2);
      
      // Tính BFP (Tỷ lệ mỡ cơ thể) dùng công thức US Navy
      if (this.neckCircumference) {
        // Nếu có số đo vòng cổ - dùng công thức US Navy (chính xác hơn)
        if (this.gender === 'male') {
          this.bodyFatPercentage = 86.010 * Math.log10(this.waistCircumference - this.neckCircumference) - 
                                  70.041 * Math.log10(this.height) + 36.76;
        } else {
          if (this.hipCircumference) {
            this.bodyFatPercentage = 163.205 * Math.log10(this.waistCircumference + this.hipCircumference - this.neckCircumference) - 
                                    97.684 * Math.log10(this.height) - 78.387;
          } else {
            // Nếu không có số đo hông, dùng công thức dựa trên BMI
            this.bodyFatPercentage = (1.20 * this.bmi) + (0.23 * this.age) - 5.4;
          }
        }
      } else {
        // Nếu không có số đo vòng cổ - dùng công thức dựa trên BMI
        const genderConstant = this.gender === 'male' ? 1 : 0;
        this.bodyFatPercentage = (1.20 * this.bmi) + (0.23 * this.age) - (10.8 * genderConstant) - 5.4;
      }
      
      // Đảm bảo tỷ lệ mỡ không âm
      this.bodyFatPercentage = Math.max(this.bodyFatPercentage, 0);
      
      // Tính BMR (Tỷ lệ trao đổi chất cơ bản) bằng công thức Mifflin-St Jeor
      if (this.gender === 'male') {
        this.bmr = 10 * this.weight + 6.25 * this.height - 5 * this.age + 5;
      } else {
        this.bmr = 10 * this.weight + 6.25 * this.height - 5 * this.age - 161;
      }
      
      // Tính TDEE
      this.tdee = this.bmr * parseFloat(this.activityLevel);
      
      // Tính WHR (Tỷ lệ eo-hông)
      if (this.hipCircumference) {
        this.waistToHipRatio = this.waistCircumference / this.hipCircumference;
      } else {
        // Ước tính số đo hông từ số liệu thống kê nếu không có
        const estimatedHip = this.gender === 'male' ? 
                            this.waistCircumference * 1.05 : // Nam thường có hông lớn hơn eo ~5%
                            this.waistCircumference * 1.2;  // Nữ thường có hông lớn hơn eo ~20%
        this.waistToHipRatio = this.waistCircumference / estimatedHip;
      }
      
      // Tạo đánh giá và đề xuất
      this.generateRecommendations();
      
      this.showResults = true;
    },
    
    validateInputs() {
      // Kiểm tra các giá trị cơ bản
      if (!this.height || !this.weight || !this.age) {
        alert('Vui lòng nhập các thông tin cơ bản: tuổi, chiều cao và cân nặng');
        return false;
      }
      
      // Kiểm tra số đo vòng eo
      if (!this.waistCircumference) {
        alert('Vui lòng nhập số đo vòng eo để tính các chỉ số WHR và BFP chính xác hơn');
        return false;
      }
      
      return true;
    },
    
    resetResults() {
      // Reset kết quả
      this.showResults = false;
      this.bmi = 0;
      this.bodyFatPercentage = 0;
      this.bmr = 0;
      this.tdee = 0;
      this.waistToHipRatio = 0;
      this.overallAssessment = '';
      this.nutritionRecommendation = '';
      this.exerciseRecommendation = '';
    },
    
    generateRecommendations() {
      // Đánh giá tổng thể
      if (this.bmi < 18.5) {
        this.overallAssessment = `Bạn đang thiếu cân với BMI ${this.bmi.toFixed(2)}. Cần tăng cân hợp lý để đạt được cân nặng lý tưởng.`;
      } else if (this.bmi < 25) {
        this.overallAssessment = `Chỉ số BMI của bạn là ${this.bmi.toFixed(2)}, nằm trong phạm vi khỏe mạnh. Tuy nhiên, cần xem xét chỉ số mỡ cơ thể (${this.bodyFatPercentage.toFixed(1)}%) và tỷ lệ eo-hông (${this.waistToHipRatio.toFixed(2)}) để đánh giá đầy đủ hơn.`;
      } else if (this.bmi < 30) {
        this.overallAssessment = `Bạn đang thừa cân với BMI ${this.bmi.toFixed(2)}. Cần có kế hoạch giảm cân hợp lý để đạt được cân nặng khỏe mạnh.`;
      } else {
        this.overallAssessment = `Bạn đang ở mức béo phì với BMI ${this.bmi.toFixed(2)}. Nên tham khảo ý kiến của chuyên gia dinh dưỡng hoặc bác sĩ để có kế hoạch giảm cân an toàn.`;
      }
      
      // Đánh giá thêm về tỷ lệ mỡ cơ thể
      if ((this.gender === 'male' && this.bodyFatPercentage > 25) || 
          (this.gender === 'female' && this.bodyFatPercentage > 32)) {
        this.overallAssessment += ` Tỷ lệ mỡ cơ thể của bạn (${this.bodyFatPercentage.toFixed(1)}%) hiện ở mức cao, điều này có thể làm tăng nguy cơ mắc các bệnh tim mạch và rối loạn chuyển hóa.`;
      }
      
      // Đánh giá thêm về tỷ lệ eo-hông
      if ((this.gender === 'male' && this.waistToHipRatio > 0.95) || 
          (this.gender === 'female' && this.waistToHipRatio > 0.80)) {
        this.overallAssessment += ` Tỷ lệ eo-hông (${this.waistToHipRatio.toFixed(2)}) của bạn hiển thị dấu hiệu tích tụ mỡ ở vùng bụng, điều này liên quan đến nguy cơ cao về bệnh tim mạch và tiểu đường loại 2.`;
      }
      
      // Đề xuất dinh dưỡng
      if (this.bmi < 18.5) {
        this.nutritionRecommendation = `Tăng lượng calo tiêu thụ lên khoảng ${(this.tdee + 300).toFixed(0)} kcal mỗi ngày. Tập trung vào các thực phẩm giàu protein như thịt nạc, cá, trứng, sữa, các loại đậu; và carbohydrate phức hợp như gạo, khoai, ngũ cốc nguyên hạt. Ăn nhiều bữa nhỏ trong ngày và bổ sung các loại hạt, bơ đậu phộng.`;
      } else if (this.bmi < 25) {
        this.nutritionRecommendation = `Duy trì lượng calo tiêu thụ ở mức ${this.tdee.toFixed(0)} kcal mỗi ngày. Cân đối các thành phần dinh dưỡng với tỷ lệ protein (20-35%), carbohydrate (45-65%), và chất béo lành mạnh (20-35%). Ưu tiên thực phẩm nguyên hạt, protein nạc, trái cây, rau xanh và chất béo không bão hòa.`;
      } else {
        this.nutritionRecommendation = `Giảm lượng calo tiêu thụ xuống còn khoảng ${(this.tdee - 500).toFixed(0)} kcal mỗi ngày để giảm cân an toàn (0.5-1kg/tuần). Tăng cường rau xanh, trái cây, protein nạc và ngũ cốc nguyên hạt. Hạn chế đường, thực phẩm chế biến sẵn, đồ chiên rán và đồ uống có cồn. Chia nhỏ bữa ăn và uống đủ nước mỗi ngày (khoảng 2-3 lít).`;
      }
      
      // Đề xuất bài tập
      if (this.bmi < 18.5) {
        this.exerciseRecommendation = `Tập trung vào các bài tập sức mạnh để phát triển cơ bắp: squat, deadlift, bench press, pull-up. Tập 3-4 ngày/tuần, mỗi buổi 45-60 phút. Hạn chế cardio cường độ cao và dài, chỉ nên tập cardio nhẹ nhàng 1-2 lần/tuần trong 20-30 phút.`;
      } else if (this.bmi < 25) {
        if ((this.gender === 'male' && this.bodyFatPercentage > 18) || 
            (this.gender === 'female' && this.bodyFatPercentage > 25)) {
          this.exerciseRecommendation = `Kết hợp tập cardio và tập sức mạnh. Cardio 3-5 lần/tuần, mỗi buổi 30-45 phút (chạy bộ, đạp xe, bơi lội). Tập sức mạnh 2-3 lần/tuần, tập toàn thân với các bài tập cơ bản. Bổ sung các bài tập HIIT 1-2 lần/tuần để đốt cháy mỡ hiệu quả.`;
        } else {
          this.exerciseRecommendation = `Duy trì thói quen tập luyện hiện tại với sự kết hợp giữa cardio và tập sức mạnh. Tập cardio 2-3 lần/tuần, mỗi buổi 30 phút. Tập sức mạnh 2-3 lần/tuần, tập toàn thân hoặc chia nhóm cơ. Thêm các bài tập linh hoạt và cân bằng như yoga hoặc pilates.`;
        }
      } else {
        this.exerciseRecommendation = `Bắt đầu với các bài tập cardio nhẹ nhàng như đi bộ 30 phút mỗi ngày. Sau đó tăng dần cường độ lên đi bộ nhanh, đạp xe hoặc bơi. Tập 5-6 ngày/tuần, mỗi buổi 30-60 phút. Kết hợp với tập sức mạnh 2 lần/tuần với cường độ vừa phải, tập toàn thân. Tránh các bài tập gây áp lực lên khớp.`;
      }
    }
  }
};
</script>

<style>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
}

.title {
  font-size: 28px;
  text-align: center;
  margin-bottom: 30px;
  color: #444;
}

.subtitle {
  font-size: 20px;
  margin-bottom: 20px;
  color: #444;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 25px;
  margin-bottom: 30px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

input, select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

input:focus, select:focus {
  outline: none;
  border-color: #4a90e2;
}

.button {
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-right: 10px;
}

.button-group {
  display: flex;
  margin-top: 20px;
}

.button.primary {
  background-color: #059669;
  color: white;
}

.button.primary:hover {
  background-color: #047857;
}

.button.secondary {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
}

.button.secondary:hover {
  background-color: #e8e8e8;
}

.results {
  margin-top: 30px;
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.metric-card {
  padding: 15px;
  border-radius: 6px;
  background-color: #f8f9fa;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.metric-card h3 {
  font-size: 16px;
  margin-bottom: 10px;
  color: #333;
}

.metric-value {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 5px;
}

.metric-status {
  font-size: 14px;
  font-weight: 500;
}

.metric-card.success {
  background-color: #e8f5e9;
  border-left: 4px solid #4caf50;
}

.metric-card.warning {
  background-color: #fff8e1;
  border-left: 4px solid #ffc107;
}

.metric-card.danger {
  background-color: #ffebee;
  border-left: 4px solid #f44336;
}

.recommendations {
  background-color: #f8f8f8;
  border-radius: 6px;
  padding: 20px;
}

.recommendation-content h3 {
  font-size: 18px;
  margin: 15px 0 10px;
  color: #333;
}

.recommendation-content p {
  margin-bottom: 15px;
  line-height: 1.6;
  color: #555;
}

@media (max-width: 768px) {
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .button-group {
    flex-direction: column;
  }
  
  .button {
    margin-right: 0;
    margin-bottom: 10px;
  }
}
</style>