import requests
import time
import random

# Tên "thing" trên dweet.io
THING_NAME = "python_hong"

# Hàm gửi dữ liệu lên dweet.io
def send_data_to_dweet(temperature, humidity):
    url = f"https://dweet.io/dweet/for/{THING_NAME}"
    payload = {"temperature": temperature, "humidity": humidity}
    response = requests.post(url, params=payload)

    if response.status_code == 200:
        print(f"Dữ liệu đã được gửi: {response.json()}")
    else:
        print(f"Lỗi gửi dữ liệu: {response.status_code}")

# Gửi dữ liệu mỗi 10 giây
if __name__ == "__main__":
    print("Bắt đầu gửi dữ liệu lên dweet.io")
    try:
        while True:
            # Sinh dữ liệu ngẫu nhiên
            temperature = round(random.uniform(20, 30), 2)
            humidity = round(random.uniform(40, 60), 2)

            # Gửi dữ liệu
            send_data_to_dweet(temperature, humidity)

            # Chờ 10 giây
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nDừng chương trình.")
