import requests
from fastapi import HTTPException
from app.auth.helpers import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

def get_github_user_info(code: str) -> dict:
    url = "https://github.com/login/oauth/access_token"
    
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000/login/callback/github"
    }
    
    try:
        response = requests.post(url, data=params, headers={"Accept": "application/json"})
        response.raise_for_status()
        token_data = response.json()
        token = token_data.get("access_token")
        
        if not token:
            raise HTTPException(status_code=400, detail="Failed to retrieve access token from GitHub")
            
        url_user = "https://api.github.com/user"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        user_response = requests.get(url_user, headers=headers)
        user_response.raise_for_status()
        
        return user_response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"GitHub OAuth error: {str(e)}")
