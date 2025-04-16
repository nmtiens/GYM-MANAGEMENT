import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import Chatbot from '@/components/Chatbot.vue';
import Admin from '@/views/Admin.vue';
import MemberInfo from '@/components/MemberInfo.vue';
import TheHoiVien from '@/components/TheHoiVien.vue';
import HuanLuyenVien from '@/components/HuanLuyenVien.vue';
import NhanVien from '@/components/NhanVien.vue';
import DichVu from '@/components/DichVu.vue';
import GoiTap from '@/components/GoiTap.vue';
import InfoHLV from '@/components/InfoHLV.vue';
import HoiVien from '@/components/HoiVien.vue';
import DangNhap from '@/components/DangNhap.vue';
import Staff from '@/views/Staff.vue';
import BodyMeasurement from '@/components/BodyMeasurement.vue';
import Users from '@/views/Users.vue';
import NutritionAdvice from '@/components/NutritionAdvice.vue';
import ThongKe from '@/components/ThongKe.vue';
import InfoGoiTap from '@/components/InfoGoiTap.vue';
import BaiTap from '@/components/BaiTap.vue';
import LichTap from '@/components/LichTap.vue';
const routes = [
  { path: '/', component: DangNhap},
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/chatbot', component: Chatbot },
  { path: '/memberinfo', component: MemberInfo},
  { path: '/thehoivien', component: TheHoiVien},
  { path: '/huanluyenvien', component: HuanLuyenVien},
  { path: '/nhanvien', component: NhanVien},
  { path: '/dichvu', component: DichVu},
  { path: '/goitap', component: GoiTap},
  { path: '/infohlv', component: InfoHLV},
  { path: '/hoivien', component: HoiVien},
  { path: '/admin', component: Admin},
  { path: '/staff', component: Staff},
  { path: '/users', component: Users},
  { path: '/bodymea', component: BodyMeasurement},
  { path: '/nutri', component: NutritionAdvice},
  { path: '/thongke', component: ThongKe},
  { path: '/infogoitap', component: InfoGoiTap},
  { path: '/lichtap', component: LichTap},
  { path: '/baitap', component: BaiTap},


];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
