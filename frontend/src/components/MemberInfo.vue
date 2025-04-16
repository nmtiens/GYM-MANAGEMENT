<template>
  <div 
    v-if="memberInfo" 
    class="info-container" 
    ref="infoContainer" 
    @mousedown="startDrag"
    :style="{ top: initialPosition.top + 'px', left: initialPosition.left + 'px' }"
  >
    <button class="close-btn" @click="closeInfo">✖</button>
    
    <h2 class="title">🔹 Thông Tin Hội Viên 🔹</h2>

    <div class="image-gallery">
      <div v-if="memberInfo.Face_Images && memberInfo.Face_Images.length">
        <img 
          :src="'data:image/jpeg;base64,' + memberInfo.Face_Images[0]" 
          alt="Ảnh khuôn mặt"
          class="face-image"
        />
      </div>
      <p v-else>Không có hình ảnh khuôn mặt.</p>
    </div>

    <p v-if="memberInfo.SoNgayConLai" class="expiration-date">
      <strong>Số ngày còn lại:</strong> {{ memberInfo.SoNgayConLai }}
    </p>

    <table class="info-table">
      <tbody>
        <tr><td><strong>Mã thẻ hội viên:</strong></td><td>{{ memberInfo.MaTheHoiVien }}</td></tr>
        <tr><td><strong>Họ tên:</strong></td><td>{{ memberInfo.HoiVien }}</td></tr>
        <tr><td><strong>Gói tập:</strong></td><td>{{ memberInfo.GoiTap }}</td></tr>
        <tr><td><strong>Huấn luyện viên:</strong></td><td>{{ memberInfo.HuanLuyenVien }}</td></tr>
        <tr><td><strong>Dịch vụ:</strong></td><td>{{ Array.isArray(memberInfo.DichVu) ? memberInfo.DichVu.join(", ") : memberInfo.DichVu }}</td></tr>
        <tr><td><strong>Ngày tạo:</strong></td><td>{{ formatDate(memberInfo.NgayTao) }}</td></tr>
        <tr><td><strong>Ngày hết hạn:</strong></td><td>{{ formatDate(memberInfo.NgayHetHan) }}</td></tr>
      </tbody>
    </table>
  </div>

  <p v-else class="no-data">Không tìm thấy thông tin hội viên.</p>
</template>

<script>
import axios from "axios";

export default {
  props: {
    MaHoiVien: String,
    initialPosition: {
      type: Object,
      default: () => ({ top: 50, left: 150 }) // Vị trí mặc định
    }
  },
  data() {
    return {
      memberInfo: null,
      isDragging: false,
      offsetX: 0,
      offsetY: 0,
    };
  },
  watch: {
    MaHoiVien: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.fetchMemberInfo(newVal);
        }
      },
    },
  },
  methods: {
    async fetchMemberInfo(MaHoiVien) {
  console.log("Fetching member info for:", MaHoiVien);
  try {
    const response = await axios.get(`http://localhost:5000/thehoivien/member/${MaHoiVien}`);
    console.log("Member info response:", response.data);
    
    // Check if response.data exists and has member info properties
    if (response.data && (response.data.HoiVien || response.data.MaTheHoiVien)) {
      // The data appears to be directly in the response, not in a memberCard property
      this.memberInfo = response.data;
      this.autoCloseInfo();
    } 
    // Also check if it's in a memberCard property as originally expected
    else if (response.data && response.data.memberCard) {
      this.memberInfo = response.data.memberCard;
      this.autoCloseInfo();
    } 
    else {
      console.error("No member data in response");
    }
  } catch (error) {
    console.error("Lỗi khi lấy dữ liệu hội viên:", error);
  }
},
    formatDate(dateString) {
      if (!dateString) return "N/A";
      const date = new Date(dateString);
      return date.toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit", year: "numeric" });
    },
    closeInfo() {
      this.memberInfo = null;
    },
    startDrag(e) {
      this.isDragging = true;
      this.offsetX = e.clientX - this.$refs.infoContainer.getBoundingClientRect().left;
      this.offsetY = e.clientY - this.$refs.infoContainer.getBoundingClientRect().top;
      document.addEventListener("mousemove", this.onDrag);
      document.addEventListener("mouseup", this.stopDrag);
    },
    onDrag(e) {
      if (!this.isDragging) return;
      const left = e.clientX - this.offsetX;
      const top = e.clientY - this.offsetY;
      this.$refs.infoContainer.style.left = `${left}px`;
      this.$refs.infoContainer.style.top = `${top}px`;
    },
    stopDrag() {
      this.isDragging = false;
      document.removeEventListener("mousemove", this.onDrag);
      document.removeEventListener("mouseup", this.stopDrag);
    },
    autoCloseInfo() {
      setTimeout(() => {
        this.closeInfo();
      }, 15000);
    },
  },
};
</script>

<style scoped>
.info-container {
  max-width: 600px;  /* Reduced from 800px */
  background: white;
  padding: 20px;  /* Reduced from 30px */
  border-radius: 10px;  /* Slightly reduced */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  position: absolute;
  cursor: grab;
  border-left: 6px solid #007bff;  /* Reduced from 8px */
}

.close-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  font-size: 20px;  /* Reduced from 24px */
  background: none;
  border: none;
  cursor: pointer;
  color: #007bff;
}

.title {
  font-size: 20px;  /* Reduced from 24px */
  font-weight: bold;
  color: #007bff;
  margin-bottom: 15px;  /* Reduced from 20px */
  text-align: center;
}

.info-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 16px;  /* Reduced from 18px */
}

.info-table td {
  padding: 8px 12px;  /* Reduced from 12px 16px */
  border-bottom: 1px solid #ddd;
  text-align: left;
}

.info-table tr:last-child td {
  border-bottom: none;
}

.expiration-date {
  font-size: 18px;  /* Reduced from 22px */
  font-weight: bold;
  background-color: #413b33;
  color: #fff;
  padding: 8px;  /* Reduced from 10px */
  border-radius: 6px;  /* Reduced from 8px */
  text-align: center;
  margin-bottom: 15px;  /* Reduced from 20px */
}

.image-gallery {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  margin-top: 15px;  /* Reduced from 20px */
}

.face-image {
  width: 200px;  /* Reduced from 250px */
  height: auto;
  border-radius: 8px;  /* Reduced from 10px */
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);  /* Slightly reduced */
  margin-top: 8px;  /* Reduced from 10px */
}

.no-data {
  text-align: center;
  color: red;
  font-weight: bold;
  margin-top: 15px;  /* Reduced from 20px */
}
</style>
