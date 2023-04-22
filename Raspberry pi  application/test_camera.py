import cv2

# Tạo đối tượng để truy cập camera
cap = cv2.VideoCapture(0)

# Kiểm tra xem camera có mở được hay không
if not cap.isOpened():
    print("Không thể mở camera")
    exit()

# Đọc dữ liệu từ camera
ret, frame = cap.read()

# Nếu đọc dữ liệu thành công, thì hiển thị ảnh
if ret:
    cv2.imwrite("anh.jpg", frame)

# Giải phóng camera
cap.release()



