from flask import Flask
import threading,requests,time,os
app = Flask(__name__)
url = "https://www.mcserverhost.com/api/servers/3dae0225/subscription"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.mcserverhost.com",
    "Referer": "https://www.mcserverhost.com/servers/3dae0225/dashboard",
    "Connection": "keep-alive",
}

cookies = {
"twk_uuid_674201982480f5b4f5a2f121":"%7B%22uuid%22%3A%221.2Bj3BgGOznciNQOGYVfm9V3hZKMebydcEb4yDh5hMOpWNyB28UjymE8rWNhdRX96Haofk2rwitoxQXlaGpVqe3PBLVX4BKh7I4Bxl0rHfLoo6Nzckvv2IjG55es%22%2C%22version%22%3A3%2C%22domain%22%3A%22mcserverhost.com%22%2C%22ts%22%3A1749777700207%7D",
"__stripe_mid":"742e384b-b16a-49f4-98ab-f51c9d77dc7a382fd6",
"mcserverhost":"8d98a627-fa55-4277-9a0e-8ece51e18621",
"_ga_SRYKCFQGK0":"GS2.1.s1749775533$o9$g1$t1749777939$j60$l0$h0", 
"_ga":"GA1.1.1400443293.1749715965; TawkConnectionTime=0",
"__stripe_sid":"072d86e0-d8d8-42e3-b0a1-b177b32ad51bf64599"
}
def background_task():
    while True:
        response = requests.post(url, headers=headers, cookies=cookies)
        if response.status_code == 200 :
            print("Đã renew server thành công vào lúc:", time.strftime('%H:%M:%S %Y-%m-%d'))
        time.sleep(3000)
@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":

    thread = threading.Thread(target=background_task)
    thread.daemon = True
    thread.start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
