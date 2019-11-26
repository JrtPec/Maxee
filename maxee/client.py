import requests

URL = "https://api.maxee.eu/api"


def request_token(api_key: str) -> str:
    auth_url = f'{URL}/Auth/token'
    r = requests.post(auth_url, json={"apiKey": api_key})
    r.raise_for_status()
    token = r.json()['auth_token']
    return token


class Client:
    """Simple JSON client that returns raw responses"""
    def __init__(self, token: str):
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'bearer {token}'})

    def req_companies(self) -> dict:
        companies_url = f'{URL}/Companies'
        r = self.session.get(companies_url)
        r.raise_for_status()
        return r.json()

    def req_divisions(self, company_id: int = None) -> dict:
        division_url = f'{URL}/Divisions'
        if company_id:
            division_url = f'{division_url}?filter=(companyId~eq~{company_id})'
        r = self.session.get(division_url)
        r.raise_for_status()
        return r.json()

    def req_devices(self, division_id: int = None) -> dict:
        devices_url = f'{URL}/Devices'
        if division_id:
            devices_url = f'{devices_url}?filter=(divisionId~eq~{division_id})'
        r = self.session.get(devices_url)
        r.raise_for_status()
        return r.json()

    def req_channels(self, device_id: int, unit: str = None) -> dict:
        channels_url = f'{URL}/Channels/{device_id}'
        if unit:
            channels_url = f"{channels_url}?filter=(unit~eq~'{unit}')"
        r = self.session.get(channels_url)
        r.raise_for_status()
        return r.json()

    def req_data(self, channel_id: int, start: str = None) -> dict:
        """Mind timestamp syntax: '2019-11-01T00-00-00' """
        data_url = f'{URL}/data?filter=(channelId~eq~{channel_id}'
        if start:
            data_url = f"{data_url}~and~timeStamp~gte~datetime'{start}'"
        data_url = data_url + ')'

        r = self.session.get(data_url)
        r.raise_for_status()
        return r.json()
