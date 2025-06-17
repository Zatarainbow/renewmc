import asyncio
import websockets
import aiohttp
import os
from flask import Flask

sryzenhd1={"Cookie":"connect.sid=s%3Af-9bZ9RxC2760zbmTraekOINSQqp2X1u.I0eImANx8Ez5Occa4CCJLxy%2F1gmSaOdYYZmOYL2mdog"}
sryzenhd2={"Cookie":"connect.sid=s%3ApsoFob1rBrAMB77kCmGe6c_MEL7Mq6fA.dYNcruTX2nkWK08WIl0FBXkfaRi3axCO8pfweFuQk5g"}

lemem_headers = {
      "Cookie": "cf_clearance=3ZE8Z3znpczPP0kjn6pNZOnxPp8xvMrNnwUbiKXkpLA-1750152115-1.2.1.1-Jlg.uBBHBs5R.MKRrfp.RmUN9JGD82sib0L4Z0RpMBogapury.VV68aTSKQ8uEt.Z35kfSY6U.c9MacYo13b29Mww2bUe7f6ZiCK.BmEHB1Vvegj65f__c_MX9ZU3s6S3wj5zMXOCMl03wOq5zF.2iVnM3JV_rYxnVJboVefambluAG9DucPYpO.n7QmNSzzDzU2rDSv0tcxkirDQigr864MiWEiTmj3lZ6KDaq.HrYGLrILXXzeggE640.CiXgDa3htZysEg0OHZ4YFAygWiB8oKcKW1F0JUEv_AhhB6yWXYLXNs7QsOpn2LR35oXTq40DVeyYKIpl89CAlXI4tQ6dN7gUrtcTXxSk4cI3DKXMpYGCuu9Iyjo83QZ3ARt2y; sid=s.X05wUcfxaY33YSpNoar82ltJFxKXwZlbd8S8egCXtx56eg17D0aBD4HyZ9ig",
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0",
}

async def sryzen1():
    try:
        async with websockets.connect("wss://my.sryzen.cloud/ws", extra_headers=sryzenhd1) as ws:
            async for message in ws:
                print("sryzen:", message)
    except Exception as e:
        print("sryzen1")

async def sryzen2():
    try:
        async with websockets.connect("wss://my.sryzen.cloud/ws", extra_headers=sryzenhd2) as ws:
            async for message in ws:
                print("sryzen:", message)
    except Exception as e:
        print("sryzen2")


async def lemem():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect('wss://dash.lemem.dev/afk/ws', headers=lemem_headers) as ws:
                async for msg in ws:
                    print("lemem:", msg)
    except Exception as e:
        print("lemem")

async def main():
    await asyncio.gather(
        sryzen1(),
        sryzen2(),
        lemem()
    )

if __name__ == "__main__":
    asyncio.run(main())

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
