import aiohttp


async def find_users(search: str, token: str, session=None):
    """Searches for users with provided string. Users can be searched by username, email or phone number"""
    timeout = aiohttp.ClientTimeout(total=15.0)
    session_status = session
    session = session or aiohttp.ClientSession()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://web.skype.com/",
        "X-Skypetoken": token,
        "X-Skype-Client": "1418/8.83.0.406",
        "X-SkypeGraphServiceSettings": '{"experiment":"MinimumFriendsForAnnotationsEnabled","geoProximity":"disabled","minimumFriendsForAnnotationsEnabled":"true","minimumFriendsForAnnotations":2,"demotionScoreEnabled":"true"}',
        "X-ECS-ETag": '"4Glu6LknsfbW8492bSA+qd/gfdnJjscNfbAjTa01M="',
        "Origin": "https://web.skype.com",
    }
    resp = await session.get(f'https://skypegraph.skype.com/v2.0/search?searchString={search}&requestId=1&locale=en-US',
                             headers=headers, timeout=timeout, allow_redirects=True)
    if resp.status == 200:
        result = await resp.json()
        if session_status is None:
            await session.close()
        return resp.status, result['results']
    else:
        if session_status is None:
            await session.close()
        return resp.status,


async def fetch_profiles(users: list, access_token: str, session=None):
    """Fetches profile information such as date of birth & gender from skype ID"""
    timeout = aiohttp.ClientTimeout(total=15.0)
    session_status = session
    session = session or aiohttp.ClientSession()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://web.skype.com/",
        "X-Skypetoken": access_token,
        "X-Skype-Caller": "Skype4Life Browser Windows (8.83.0.406)",
        "X-Skype-Request-Id": "b351f666-6d5b-4259-a5b3-118174f83ef0",
        "Origin": "https://web.skype.com",
    }
    payload = {
        "mris": [f"8:{user}" for user in users],
        "locale": "en-US"
    }
    resp = await session.post('https://people.skype.com/v2/profiles',
                              headers=headers, json=payload, timeout=timeout, allow_redirects=True)
    if resp.status == 200:
        result = await resp.json()
        if session_status is None:
            await session.close()
        return resp.status, result
    else:
        if session_status is None:
            await session.close()
        return resp.status,
