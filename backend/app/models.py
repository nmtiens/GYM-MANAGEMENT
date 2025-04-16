from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Bảng Hội viên
class HoiVien(Base):
    __tablename__ = 'hoi_vien'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ho_lot = Column(String(100))
    ten = Column(String(50))
    ngay_sinh = Column(Date)
    gioi_tinh = Column(String(10))
    dia_chi = Column(String(200))
    dien_thoai = Column(String(20))
    email = Column(String(100))
    ngay_dang_ky = Column(Date)
    trang_thai = Column(String(50))
    mat_hoi_nhan_dien = Column(String(200))  # Dữ liệu khuôn mặt (được lưu dưới dạng ảnh/chuỗi)
    thoi_gian_tao = Column(Date)

    the_hoi_vien = relationship('TheHoiVien', back_populates='hoi_vien')
    goi_tap = relationship('GoiTap', secondary='hoi_vien_goi_tap')

# Bảng Nhân viên
class NhanVien(Base):
    __tablename__ = 'nhan_vien'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ho_lot = Column(String(100))
    ten = Column(String(50))
    chuc_vu = Column(String(50))
    ngay_sinh = Column(Date)
    gioi_tinh = Column(String(10))
    dien_thoai = Column(String(20))
    email = Column(String(100))
    dia_chi = Column(String(200))
    ngay_vao_lam = Column(Date)
    luong = Column(Float)
    trang_thai = Column(String(50))

# Bảng Huấn luyện viên
class HuanLuyenVien(Base):
    __tablename__ = 'huan_luyen_vien'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ho_lot = Column(String(100))
    ten = Column(String(50))
    chuyen_mon = Column(String(100))
    so_ho_tro = Column(Integer)
    dien_thoai = Column(String(20))
    email = Column(String(100))
    trang_thai = Column(String(50))

# Bảng Dịch vụ
class DichVu(Base):
    __tablename__ = 'dich_vu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_dich_vu = Column(String(100))
    mo_ta = Column(String(500))
    gia = Column(Float)
    thoi_gian_dich_vu = Column(String(50))

# Bảng Thẻ hội viên
class TheHoiVien(Base):
    __tablename__ = 'the_hoi_vien'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_hoi_vien = Column(Integer, ForeignKey('hoi_vien.id'))
    so_the = Column(String(50))
    ngay_bat_dau = Column(Date)
    ngay_het_han = Column(Date)
    loai_the = Column(String(50))
    trang_thai = Column(String(50))

    hoi_vien = relationship('HoiVien', back_populates='the_hoi_vien')

# Bảng Gói tập
class GoiTap(Base):
    __tablename__ = 'goi_tap'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_goi = Column(String(100))
    mo_ta = Column(String(500))
    gia = Column(Float)
    so_luong_lop = Column(Integer)
    thoi_gian_hieu_luc = Column(String(50))

# Bảng kết nối giữa Hội viên và Gói tập
class HoiVienGoiTap(Base):
    __tablename__ = 'hoi_vien_goi_tap'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_hoi_vien = Column(Integer, ForeignKey('hoi_vien.id'))
    id_goi_tap = Column(Integer, ForeignKey('goi_tap.id'))

# Kết nối với cơ sở dữ liệu SQLite
engine = create_engine('sqlite:///gym_management.db', echo=True)

# Tạo các bảng trong cơ sở dữ liệu
Base.metadata.create_all(engine)

# Tạo session để thao tác với cơ sở dữ liệu
Session = sessionmaker(bind=engine)
session = Session()

# Ví dụ thêm một hội viên mới
new_member = HoiVien(
    ho_lot="Nguyen Minh",
    ten="Tuan",
    ngay_sinh="1990-04-15",
    gioi_tinh="Nam",
    dia_chi="Hanoi",
    dien_thoai="0987654321",
    email="tuanminh@example.com",
    ngay_dang_ky="2025-02-09",
    trang_thai="Hoạt động",
    mat_hoi_nhan_dien="image_data_here",  # Dữ liệu ảnh khuôn mặt
    thoi_gian_tao="2025-02-09"
)

session.add(new_member)
session.commit()

# Đóng session sau khi thao tác
session.close()
