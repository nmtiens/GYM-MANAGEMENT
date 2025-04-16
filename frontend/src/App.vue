<template>
  <div id="app">
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

</script>

<style>
/* Đảm bảo toàn bộ trang có nền ảnh */
html, body {
  height: 100%;  /* Chiếm toàn bộ chiều cao màn hình */
  margin: 0;  /* Loại bỏ margin mặc định */
  background: url('https://cdn.unityfitness.vn/2024/08/trai-nghiem-phong-gym.jpg') no-repeat center center fixed;
  background-size: cover;  /* Đảm bảo ảnh nền phủ toàn màn hình */
}





/* Styling cho các liên kết */

</style>
