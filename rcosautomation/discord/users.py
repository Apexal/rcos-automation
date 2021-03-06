import requests
from .constants import API_BASE, RCOS_SERVER_ID, VERIFIED_ROLE_ID, DISCORD_BOT_TOKEN, DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET, DISCORD_RETURN_URL, HEADERS


def get_tokens(code):
    '''Given an authorization code, request the access and refresh tokens for a Discord user. Returns the tokens. Throws an error if invalid request.'''
    response = requests.post(f'{API_BASE}/oauth2/token',
                             data={
                                 'client_id': DISCORD_CLIENT_ID,
                                 'client_secret': DISCORD_CLIENT_SECRET,
                                 'grant_type': 'authorization_code',
                                 'code': code,
                                 'redirect_uri': DISCORD_RETURN_URL,
                                 'scope': 'identity guilds.join'
                             },
                             headers={
                                 'Content-Type': 'application/x-www-form-urlencoded'
                             }
                             )
    response.raise_for_status()
    tokens = response.json()
    return tokens


def get_user_info(access_token):
    '''Given an access token, get a Discord user's info including id, username, discriminator, avatar url, etc. Throws an error if invalid request.'''
    response = requests.get(f'{API_BASE}/users/@me', headers={
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    )
    response.raise_for_status()
    user = response.json()
    return user


def add_user_to_server(access_token: str, user_id: str, nickname: str):
    '''Given a Discord user's id, add them to the RCOS server with their nickname set as their RCS ID and with the 'Verified Student' role.'''
    print('Access Token', access_token)
    print('User ID', user_id)
    print('Discord Bot Token', DISCORD_BOT_TOKEN)
    response = requests.put(f'{API_BASE}/guilds/{RCOS_SERVER_ID}/members/{user_id}',
                            json={
                                'access_token': access_token,
                                'nick': nickname,
                                'roles': [VERIFIED_ROLE_ID],
                            },
                            headers=HEADERS
                            )
    response.raise_for_status()
    return response


def kick_user_from_server(user_id: str):
    '''Given a Discord user's id, kick them from the RCOS server.'''
    response = requests.delete(
        f'{API_BASE}/guilds/{RCOS_SERVER_ID}/members/{user_id}', headers=HEADERS)
    response.raise_for_status()
    return response


def set_member_nickname(user_id: str, nickname: str):
    '''Given a Discord user's id, set their nickname on the server.'''
    response = requests.patch(f'{API_BASE}/guilds/{RCOS_SERVER_ID}/members/{user_id}',
                              json={
                                  'nick': nickname
                              },
                              headers=HEADERS
                              )
    response.raise_for_status()
    return response


def add_role_to_member(user_id: str, role_id: str):
    '''Add a role (identified by its id) to a member.'''
    response = requests.put(
        f'{API_BASE}/guilds/{RCOS_SERVER_ID}/members/{user_id}/roles/{role_id}', headers=HEADERS)
    response.raise_for_status()
    return response
