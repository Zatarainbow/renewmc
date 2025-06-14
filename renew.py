# -*- coding: utf-8 -*-

# --- 1. IMPORT CÁC THƯ VIỆN CẦN THIẾT ---
import os
import time
import json
import threading
import requests
import websocket
from flask import Flask

# --- 2. KHỞI TẠO FLASK APP ---
# Flask app giúp script luôn chạy trên các nền tảng hosting
app = Flask(__name__)

# --- BIẾN TOÀN CỤC ĐỂ THEO DÕI TRẠNG THÁI IN LOG ---
# Chỉ in log thành công của McServer Bot một lần duy nhất
mcserver_first_success_logged = False

# --- 3. CẤU HÌNH CHO BOT SRYZEN.CLOUD (AFK COIN) ---
SRYZEN_COOKIE = "connect.sid=s%3A5SvGQ4k1LBOdI8ZSVOutqVpRo1J8csxj.tOTzks2ibsKvRVj7r2o9qu03H3Pp1GUK%2BYgclsO8HqE"
SRYZEN_API_URL = "https://my.sryzen.cloud/api/v5/state"
SRYZEN_WS_URL = "wss://my.sryzen.cloud/ws"
SRYZEN_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0"

# --- 4. CẤU HÌNH CHO BOT MCSERVERHOST (RENEW SERVER) ---
MCSERVER_URL = "https://www.mcserverhost.com/api/servers/3dae0225/subscription"
MCSERVER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.mcserverhost.com",
    "Referer": "https://www.mcserverhost.com/servers/3dae0225/dashboard",
    "Connection": "keep-alive",
}
MCSERVER_COOKIES = {
    "twk_uuid_674201982480f5b4f5a2f121": "%7B%22uuid%22%3A%221.2Bj3BgGOznciNQOGYVfm9V3hZKMebydcEb4yDh5hMOpWNyB28UjymE8rWNhdRX96Haofk2rwitoxQXlaGpVqe3PBLVX4BKh7I4Bxl0rHfLoo6Nzckvv2IjG55es%22%2C%22version%22%3A3%2C%22domain%22%3A%22mcserverhost.com%22%2C%22ts%22%3A1749777700207%7D",
    "__stripe_mid": "742e384b-b16a-49f4-98ab-f51c9d77dc7a382fd6",
    "mcserverhost": "8d98a627-fa55-4277-9a0e-8ece51e18621",
    "_ga_SRYKCFQGK0": "GS2.1.s1749775533$o9$g1$t1749777939$j60$l0$h0",
    "_ga": "GA1.1.1400443293.1749715965; TawkConnectionTime=0",
    "__stripe_sid": "072d86e0-d8d8-42e3-b0a1-b177b32ad51bf64599"
}

# --- 5. LOGIC CHO BOT SRYZEN.CLOUD ---

# Hàm xử lý khi WebSocket mở
def sryzen_on_open(ws):
    print("[Sryzen Bot] ✅ Kết nối WebSocket đã được mở.")

# Hàm xử lý khi nhận được tin nhắn
def sryzen_on_message(ws, message):
    # Đã tắt log ở đây để không in ra các thông báo trạng thái AFK liên tục
    pass

# Hàm xử lý khi có lỗi
def sryzen_on_error(ws, error):
    print(f"[Sryzen Bot] ❌ Lỗi WebSocket: {error}")

# Hàm xử lý khi WebSocket đóng
def sryzen_on_close(ws, close_status_code, close_msg):
    print("[Sryzen Bot] 🔌 Kết nối WebSocket đã bị đóng. Sẽ thử kết nối lại sau 30 giây...")
    time.sleep(30)
    run_sryzen_afk() # Tự động kết nối lại

def run_sryzen_afk():
    """Hàm chính để chạy bot Sryzen AFK."""
    print("[Sryzen Bot] 🚀 Bắt đầu xác thực và kết nối...")
    http_headers = {
        'Cookie': SRYZEN_COOKIE, 'User-Agent': SRYZEN_USER_AGENT,
        'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive', 'Host': 'my.sryzen.cloud',
        'Referer': 'https://my.sryzen.cloud/coins/afk', 'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin',
    }
    try:
        response = requests.get(SRYZEN_API_URL, headers=http_headers)
        response.raise_for_status()
        print(f"[Sryzen Bot] ✅ Yêu cầu GET thành công! Bắt đầu kết nối WebSocket...")
        # Đã xóa phần in dữ liệu người dùng để log gọn hơn
        
        ws_headers = {
            'Cookie': SRYZEN_COOKIE, 'User-Agent': SRYZEN_USER_AGENT,
            'Origin': 'https://my.sryzen.cloud'
        }
        ws = websocket.WebSocketApp(SRYZEN_WS_URL,
                                  header=ws_headers,
                                  on_open=sryzen_on_open,
                                  on_message=sryzen_on_message,
                                  on_error=sryzen_on_error,
                                  on_close=sryzen_on_close)
        ws.run_forever()
    except requests.exceptions.RequestException as e:
        print(f"[Sryzen Bot] 🔥 Lỗi khi gửi yêu cầu HTTP GET: {e}")
        print("[Sryzen Bot] Vui lòng kiểm tra lại Cookie hoặc kết nối mạng.")


# --- 6. LOGIC CHO BOT MCSERVERHOST ---

def run_mcserver_renewer():
    """Hàm chính để chạy bot renew server McServerHost."""
    global mcserver_first_success_logged
    print("[McServer Bot] 🚀 Bot renew server đã được khởi động.")
    while True:
        try:
            response = requests.post(MCSERVER_URL, headers=MCSERVER_HEADERS, cookies=MCSERVER_COOKIES, timeout=30)
            if response.status_code == 200:
                # Chỉ in ra màn hình ở lần renew thành công đầu tiên
                if not mcserver_first_success_logged:
                    print(f"[McServer Bot] ✅ Đã renew server thành công lần đầu vào lúc: {time.strftime('%H:%M:%S %d-%m-%Y')}")
                    mcserver_first_success_logged = True
            else:
                # In ra nếu có lỗi
                print(f"[McServer Bot] ⚠️ Renew thất bại! Status Code: {response.status_code}, Response: {response.text}")
        except requests.exceptions.RequestException as e:
            # In ra nếu có lỗi mạng
            print(f"[McServer Bot] 🔥 Lỗi khi gửi yêu cầu renew: {e}")
        
        # Chờ 50 phút (3000 giây) trước khi gửi yêu cầu tiếp theo
        time.sleep(3000)

# --- 7. FLASK WEB ROUTE ---

@app.route('/')
def index():
    """Trang chủ đơn giản để kiểm tra bot có đang chạy không."""
    return "<h1>Cả hai bot AFK đều đang hoạt động! (Chế độ yên lặng)</h1>"

# --- 8. KHỞI CHẠY CÁC BOT VÀ WEB SERVER ---

if __name__ == "__main__":
    # Tạo và khởi chạy luồng cho bot Sryzen
    sryzen_thread = threading.Thread(target=run_sryzen_afk)
    sryzen_thread.daemon = True
    sryzen_thread.start()

    # Tạo và khởi chạy luồng cho bot McServerHost
    mcserver_thread = threading.Thread(target=run_mcserver_renewer)
    mcserver_thread.daemon = True
    mcserver_thread.start()

    # Chạy Flask app ở luồng chính để giữ cho toàn bộ script hoạt động
    print("[Main Thread] 🚀 Khởi chạy Web Server...")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
