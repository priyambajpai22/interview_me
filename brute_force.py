import requests
import asyncio
import concurrent.futures

async def fetch_url(url):
    response = await loop.run_in_executor(None, lambda: requests.get(url))
    return response.status_code

async def run():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        urls = ['https://www.peekyou.com/rahul_tiwari'] * 100000
        responses = await asyncio.gather(
            *[loop.run_in_executor(executor, fetch_url, url) for url in urls]
        )

    for x, status_code in enumerate(responses):
        print(f'Request {x + 1}: Status Code {status_code}')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
