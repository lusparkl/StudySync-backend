import requests
from fastapi import HTTPException
from app.auth.helpers import BACKEND_URL, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

def get_github_user_info(code: str) -> dict:
    url = "https://github.com/login/oauth/access_token"
    
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": f"{BACKEND_URL}/login/callback/github"
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

        user_data = user_response.json()

        if not user_data.get("email"):
            emails_response = requests.get("https://api.github.com/user/emails", headers=headers)
            emails_response.raise_for_status()
            emails = emails_response.json()
            primary_email = next(
                (
                    email["email"]
                    for email in emails
                    if email.get("primary") and email.get("verified")
                ),
                None
            )
            user_data["email"] = primary_email
        
        return user_data
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"GitHub OAuth error: {str(e)}")
