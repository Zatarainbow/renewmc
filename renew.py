import asyncio
import websockets
import aiohttp
import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

sryzenhd1={"Cookie":"connect.sid=s%3Af-9bZ9RxC2760zbmTraekOINSQqp2X1u.I0eImANx8Ez5Occa4CCJLxy%2F1gmSaOdYYZmOYL2mdog"}
sryzenhd2={"Cookie":"connect.sid=s%3ApsoFob1rBrAMB77kCmGe6c_MEL7Mq6fA.dYNcruTX2nkWK08WIl0FBXkfaRi3axCO8pfweFuQk5g"}

lemem_headers = {
      "Cookie": "cf_clearance=vgmkuUwQ019oKGMXruGeWDGmlq4l_X_vv9pEnS76_AA-1750171779-1.2.1.1-cNZw.euTuXsubr25YkkEGPbez8KQtsE79OX.9bp1OSNrXbw6FRhn.tBd5ju9yTfDL.Ba6iLbfAwgClqnLAR2ajK9HklWmDMjg7Jkk4VRHSwX2.J_xTZ4sAU11WQJv4_tRfZgXkYYek5sGDA66wXIj9AcWR_.jhKQYrWy33Jo9Pw9WKxoKYqWPsOoMxiMmeJ.EV8p9o5gZa2lYRGCKJPtkCmVtwNLP.ggi18FUa0TqzHEuydT0afedp2MsIS3jh5BMfjY.mH3dmlz4VOFaszycktrNf1pCowNeIhWz6tpMTYaT72HF4w_s9KAEQe2uShUnAEnRmJYX6K8dlgInVMNyasWD_EgKx.el82Eherv9xABa80I2RBceIXmGUPgsAt5; sid=s.X05wUcfxaY33YSpNoar82ltJFxKXwZlbd8S8egCXtx56eg17D0aBD4HyZ9ig",
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0",
}

@app.route("/")
def index():
    return "Flask is running"

async def sryzen1():
    try:
        async with websockets.connect("wss://my.sryzen.cloud/ws", extra_headers=sryzenhd1) as ws:
            async for message in ws:
                print("sryzen1:", message)
    except Exception as e:
        print("sryzen1 error:", e)

async def sryzen2():
    try:
        async with websockets.connect("wss://my.sryzen.cloud/ws", extra_headers=sryzenhd2) as ws:
            async for message in ws:
                print("sryzen2:", message)
    except Exception as e:
        print("sryzen2 error:", e)

async def lemem():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect('wss://dash.lemem.dev/afk/ws', headers=lemem_headers) as ws:
                async for msg in ws:
                    print("lemem:", msg.data)
    except Exception as e:
        print("lemem error:", e)

async def main():
    await asyncio.gather(
        sryzen1(),
        sryzen2(),
        lemem()
    )

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Start Flask in a thread
    Thread(target=run_flask, daemon=True).start()
    # Run WebSocket clients
    asyncio.run(main())
