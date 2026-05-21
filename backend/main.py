from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import asyncio
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HEADERS = {
    "X-IG-App-ID": "936619743392459",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.instagram.com/",
    "Origin": "https://www.instagram.com",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

class CheckRequest(BaseModel):
    username: str

async def sleep_random():
    await asyncio.sleep(random.uniform(0.8, 1.5))

async def get_user_id(client: httpx.AsyncClient, username: str):
    url = f"https://www.instagram.com/api/v1/web/search/topsearch/?context=blended&query={username.lower()}&include_reel=false"
    r = await client.get(url, headers=HEADERS)
    data = r.json()
    users = data.get("users", [])
    result = next((u for u in users if u["user"]["username"].lower() == username.lower()), None)
    if not result:
        return None
    return result["user"]["pk"]

async def fetch_list(client: httpx.AsyncClient, list_type: str, user_id: str, count=50, next_max_id=""):
    url = f"https://www.instagram.com/api/v1/friendships/{user_id}/{list_type}/?count={count}"
    if next_max_id:
        url += f"&max_id={next_max_id}"
    r = await client.get(url, headers=HEADERS)
    data = r.json()
    users = data.get("users", [])
    if data.get("next_max_id"):
        await sleep_random()
        users += await fetch_list(client, list_type, user_id, count, data["next_max_id"])
    return users

@app.post("/check")
async def check(req: CheckRequest):
    username = req.username.strip().lstrip("@")
    async with httpx.AsyncClient(timeout=30) as client:
        user_id = await get_user_id(client, username)
        if not user_id:
            raise HTTPException(status_code=404, detail="User not found or account is private")

        followers_raw = await fetch_list(client, "followers", user_id)
        following_raw = await fetch_list(client, "following", user_id)

    followers = {u["username"].lower() for u in followers_raw}
    following = {u["username"].lower() for u in following_raw}

    not_following_back = sorted(following - followers)
    not_followed_back = sorted(followers - following)

    return {
        "username": username,
        "followers_count": len(followers),
        "following_count": len(following),
        "not_following_back": not_following_back,
        "not_followed_back": not_followed_back,
    }

@app.get("/")
def root():
    return {"status": "ok"}
