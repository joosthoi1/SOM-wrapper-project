import os, requests, json

class AuthenticateError(Exception):
    pass

class Sapi:
    def __init__(self):
#        self.url = ('https://%s.zportal.nl/api/v3/' % school)
        self.session = requests.Session()

    def get_auth(self, school = '', username = '', password = '', use_old=True):
        self.school_uuid = school
        self.username = username
        self.useold = use_old
        if self.useold and os.path.isfile('token.json'):
            with open('token.json') as file:
                read1 = json.loads(file.read())
                self.auth = read1["access_token"]
                self.url = read1["somtoday_api_url"]

        else:
            if not password or not self.username or not self.school_uuid:
                print('When creating a new authentication token, please supply a username, password and school uuid')
                return
            token_url = 'https://production.somtoday.nl/oauth2/token'
            token_response = self.session.post(
                token_url,
                data = {
                    "username": self.school_uuid + '\\' + self.username,
                    "password": password,
                    "scope": "openid",
                    "grant_type": "password"
                    },
                headers = {
                        "Authorization": "Basic RDUwRTBDMDYtMzJEMS00QjQxLUExMzctQTlBODUwQzg5MkMyOnZEZFdkS3dQTmFQQ3loQ0RoYUNuTmV5ZHlMeFNHTkpY"
                    }
                )
            with open('token.json', 'w+') as file:
                if not token_response.text:
                    file.close()
                    os.remove('token.json')
                    raise AuthenticateError('School or code appears to be wrong or not valid')
                    return
                else:
                    data = token_response.json()
                    data.pop("scope")
                    data.pop("somtoday_tenant")
                    data.pop("id_token")
                    data.pop("token_type")
                    data.pop("expires_in")

                    file.write(json.dumps(data, indent = 4))
            self.auth = data["access_token"]
            self.url = data["somtoday_api_url"]

    def get_schools(self):
        data = self.session.get('https://servers.somtoday.nl/organisaties.json')
        return data.json()[0]['instellingen']

    def refresh(self, function, parameter=None):
        token_url = 'https://production.somtoday.nl/oauth2/token'
        with open('token.json', 'r') as file:
            refresh_token = json.loads(file.read())['refresh_token']
        token_response = self.session.post(
            token_url,
            data = {
                "grant_type": "refresh_token",
                'refresh_token': refresh_token,
                'client_id': 'D50E0C06-32D1-4B41-A137-A9A850C892C2',
                'client_secret': 'vDdWdKwPNaPCyhCDhaCnNeydyLxSGNJX'
                }
            )
        with open('token.json', 'w+') as file:
            if not token_response.text:
                file.close()
                os.remove('token.json')
                raise AuthenticateError('Something went wrong, please try logging in again')
                return
            else:
                data = token_response.json()
                data.pop("scope")
                data.pop("somtoday_tenant")
                data.pop("id_token")
                data.pop("token_type")
                data.pop("expires_in")

                file.write(json.dumps(data, indent = 4))
        self.auth = data["access_token"]
        self.url = data["somtoday_api_url"]
        if parameter:
            output = function(parameter)
        else:
            output = function()
        return output

    def get_id(self):
        def select_keys(iterArray):
            keys = [
                'roepnaam', 'achternaam'
                ]
            current = {}
            for i in keys:
                if i in iterArray:
                    current[i] = iterArray[i]
            current['id'] = iterArray['links'][0]['id']

            return current
        if not hasattr(self, 'auth') or not hasattr(self, 'url'):
            raise AuthenticateError('Please make sure you authenticate')
        r = requests.get(
            f"{self.url}/rest/v1/leerlingen",
            headers = {
                "Authorization": f"Bearer {self.auth}",
                "Accept": "application/json"
                }
            )
        if r.status_code == 401:
            id = self.refresh(self.get_id)
            print(id)
            return id
#        print(json.dumps(r.json()['items'], indent=4))
        collections = []
#        print(r.text, '-----')
        for i in r.json()['items']:
            collections.append(select_keys(i))
#        print(collections)
        return collections

    def get_grades(self, id):
        def select_keys(iterArray):
            keys = [
                'herkansingstype', 'resultaat', 'geldendResultaat',
                'resultaatAfwijkendNiveau', 'resultaatLabel',
                'resultaatLabelAfkorting', 'resultaatLabelAfwijkendNiveau',
                'resultaatLabelAfwijkendNiveauAfkorting', 'datumInvoer',
                'teltNietmee', 'toetsNietGemaakt', 'leerjaar', 'periode',
                'overschrevenDoor', 'examenWeging', 'isExamendossierResultaat',
                'vak', 'isVoortgangsdossierResultaat', 'type', 'volgnummer',
                'weging', 'omschrijving'
                ]
            innerkeys = {
                'vak':'naam'
                }
            current = {}
            for i in keys:
                if i in iterArray:
                    current[i] = iterArray[i]
            for i in innerkeys.keys():
                if i in iterArray:
                    for x in iterArray[i]:
                        if innerkeys[i] in x:
                            current[i] = iterArray[i][innerkeys[i]]

            return current

        if not hasattr(self, 'auth') or not hasattr(self, 'url'):
            raise AuthenticateError('Please make sure you authenticate')
        collections = []
        x = 0
        while True:
            r = requests.get(
                f'{self.url}/rest/v1/resultaten/huidigVoorLeerling/{id}',
                headers = {
                    "Authorization": f"Bearer {self.auth}",
                    "Accept": "application/json",
                    "Range":f"items={x*100}-{(x+1)*100}"
                    }
                )
            if r.status_code == 401:
                grades = self.refresh(self.get_grades, id)
                return grades
            values = r.json()['items']
            if not values:
                break
            for i in values:
                collections.append(select_keys(i))
            x += 1
        return collections

if __name__ == "__main__":
    s = Sapi()
#    s.get_schools()
    s.get_auth()
    id = s.get_id()[0]['id']

    grades = s.get_grades(id)
    print(json.dumps(grades, indent=4))
