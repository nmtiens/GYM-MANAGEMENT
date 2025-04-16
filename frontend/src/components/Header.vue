<template>
  <header class="header">
    <div class="container">
      <div class="logo">
        <h1>GYM HUB</h1>
      </div>
      <nav class="nav">
        <router-link to="/infogoitap" class="nav-link">
          <i class="fas fa-home"></i> Trang Chủ
        </router-link>
        <router-link to="/nutri" class="nav-link">
          <i class="fas fa-chart-bar"></i> Tra cứu thực phẩm
        </router-link>
        <router-link to="/bodymea" class="nav-link">
          <i class="fas fa-dumbbell"></i> Đo chỉ số
        </router-link>
      </nav>
      <div class="menu-toggle">
        <i class="fas fa-bars"></i>
      </div>
    </div>
  </header>
</template>

<style scoped>
.header {
  background: linear-gradient(to right, #0d1b2a, #1b263b);
  padding: 15px 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo h1 {
  color: #e0e1dd;
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.nav {
  display: flex;
  align-items: center;
  gap: 10px;
}

.nav-link {
  color: #e0e1dd;
  text-decoration: none;
  padding: 10px 15px;
  border-radius: 6px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.nav-link.router-link-exact-active {
  background-color: #415a77;
  color: white;
}

.auth-buttons {
  display: flex;
  margin-left: 20px;
  gap: 10px;
}

.auth-btn {
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  font-weight: 600;
  transition: all 0.2s ease;
}

.login {
  color: #e0e1dd;
  border: 1px solid #e0e1dd;
}

.login:hover {
  background-color: rgba(224, 225, 221, 0.1);
}

.register {
  background-color: #e63946;
  color: white;
}

.register:hover {
  background-color: #d62b3a;
  transform: translateY(-2px);
}

.menu-toggle {
  display: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

/* Responsive design */
@media (max-width: 768px) {
  .nav {
    display: none;
  }
  
  .menu-toggle {
    display: block;
  }
  
  /* Show this when menu is active */
  .nav.active {
    display: flex;
    flex-direction: column;
    position: absolute;
    top: 70px;
    left: 0;
    right: 0;
    background: #0d1b2a;
    padding: 20px;
    align-items: flex-start;
  }
  
  .nav.active .auth-buttons {
    margin-left: 0;
    margin-top: 15px;
    width: 100%;
  }
  
  .nav.active .auth-btn {
    width: 100%;
    text-align: center;
  }
}
</style>