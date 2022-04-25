import aiohttp

from skype import *


class Profile:
    def __init__(self, skype_id, email=None, email_username=None, handle=None, avatar_url=None, is_default_avatar=None,
                 city=None, state=None, country=None, display_name=None, date_of_birth=None, gender=None, creation_time=None):
        self.skype_id = skype_id
        self.email = email
        self.email_username = email_username
        self.handle = handle
        self.avatar_url = avatar_url
        self.is_default_avatar = is_default_avatar
        self.display_name = display_name
        self.city = city
        self.state = state,
        self.country = country,
        self.date_of_birth = date_of_birth,
        self.gender = gender,
        self.creation_time = creation_time


async def search(text, token):
    if text is None:
        print('Please enter valid text to search in Skype.')
        return

    async with aiohttp.ClientSession() as session:

        # Searching Skype for search parameter
        users = await find_users(text, token, session)

        if users[0] != 200:
            if users[0] == 429:
                print(f'{users[0]} | Ratelimited by API, try again in a minute.')
                return
            elif users[0] == 403:
                print(f'{users[0]} | Invalid or expired access token.')
                return
            else:
                print(f'{users[0]} | An unknown error occured.')
                return

        if len(users[1]) == 0:
            print('\n[-] Could not find any skype users')
            return
        else:
            print(f'\n[+] Found {len(users[1])} users')

        # Fetching user profiles
        profiles = await fetch_profiles([profile["nodeProfileData"]["skypeId"] for profile in users[1]], token, session)

        if profiles[0] != 200:
            if profiles[0] == 429:
                print(f'{users[0]} | Ratelimited by API, try again in a minute.')
                return
            elif users[0] == 403:
                print(f'{users[0]} | Invalid or expired access token.')
                return
            else:
                print(f'{users[0]} | An unknown error occured.')
                return

        for user in users[1]:
            profile = Profile(skype_id=user["nodeProfileData"]["skypeId"])

            # Checking if email can be found for account
            if profile.skype_id.startswith('live:') and profile.skype_id.startswith('live:.cid.') is False:
                email_username = profile.skype_id[5:]
                if email_username.split('_')[-1].isdigit():
                    profile.email_username = '_'.join(email_username.split('_')[:-1])

                    # Common email providers
                    email_domains = ['gmail.com', 'icloud.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
                                     'aol.com', 'mail.com', 'mail.ru', 'gmx.at', 'gmx.com',
                                     'gmx.de', 'gmx.fr', 'gmx.net', 'gmx.us']

                    # Attempting to find email
                    for email_domain in email_domains:

                        check = await find_users(f'{profile.email_username}@{email_domain}', token, session)

                        if users[0] != 200:
                            if users[0] == 429:
                                print(f'{users[0]} | Ratelimited by API, try again in a minute.')
                                return
                            else:
                                print(f'{users[0]} | An unknown error occured.')
                                return

                        for user_profile in check[1]:
                            if profile.skype_id == user_profile["nodeProfileData"]["skypeId"]:
                                profile.email = f'{profile.email_username}@{email_domain}'
                                break

            if 'skypeHandle' in user['nodeProfileData']:
                profile.handle = user['nodeProfileData']['skypeHandle']

            if 'name' in user['nodeProfileData']:
                profile.display_name = user['nodeProfileData']['name']

            profile.avatar_url = f"https://avatar.skype.com/v1/avatars/{profile.skype_id}/public"

            if 'avatarUrl' in profiles[1]['profiles'][f'8:{profile.skype_id}']['profile']:
                profile.is_default_avatar = False
            else:
                profile.is_default_avatar = True

            if 'city' in user['nodeProfileData']:
                profile.city = user['nodeProfileData']['city']

            if 'state' in user['nodeProfileData']:
                profile.state = user['nodeProfileData']['state']

            if 'country' in user['nodeProfileData']:
                profile.country = user['nodeProfileData']['country']

            if 'birthday' in profiles[1]['profiles'][f'8:{profile.skype_id}']['profile']:
                profile.date_of_birth = profiles[1]['profiles'][f'8:{profile.skype_id}']['profile']['birthday']

            if 'gender' in profiles[1]['profiles'][f'8:{profile.skype_id}']['profile']:
                profile.gender = profiles[1]['profiles'][f'8:{profile.skype_id}']['profile']['gender']

            if not profile.skype_id.startswith('live:'):
                profile.creation_time = '< 2016'
            elif profile.skype_id.startswith('live:.cid.'):
                profile.creation_time = '> late 2019'
            else:
                profile.creation_time = 'between 2016 - late 2019'

            print('---------------------------------------\n')

            print(f'Skype ID: {profile.skype_id}')
            if profile.display_name not in [None, (None,)]:
                print(f'Display Name: {profile.display_name}')
            print(f'\nProfile Avatar: {profile.avatar_url}')
            if profile.is_default_avatar:
                print(f'[-] Default Avatar')

            if [profile.city, profile.state, profile.country] != [None, (None,), (None,)]:
                print('\n[+] Location found!')
            if profile.city not in [None, (None,)]:
                print(f'- City: {profile.city}')
            if profile.state not in [None, (None,)]:
                print(f'- State: {profile.state}')
            if profile.country not in [None, (None,)]:
                print(f'- Country: {profile.country}')

            if [profile.date_of_birth, profile.gender, profile.email] != [(None,), 'Unspecified', None]:
                print('\n[+] Other info found!')

            if profile.date_of_birth != (None,):
                print(f'- Date of Birth: {profile.date_of_birth}')
            if profile.gender is not None and profile.gender != 'Unspecified':
                print(f'- Gender: {profile.gender}')
            if profile.email is not None:
                print(f'- Email: {profile.email}')

            if profile.creation_time is not None:
                print(f'\n=> The account was created {profile.creation_time}')

        print('---------------------------------------')
