from typing import overload
import pandas as pd
import os
import requests
import json
from datetime import datetime, timedelta
import nemreader
from bs4 import BeautifulSoup
from functools import reduce
import tempfile
import logging
from pprint import pprint

logger = logging.getLogger('sapnmeterdatalib')

class LoginError(Exception):
    """Raised when login fails."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    pass
class AuthError(Exception):
    """Raised when failed to retrieved csrf and/or authorization."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    pass
class FetchError(Exception):
    """Raised when failed to retrieved meterdata."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    pass

class login:
    def __init__(self, email:str, password:str):
        self.email = email
        self._session = requests.sessions.Session()
        CADSiteLogin_url = 'https://customer.portal.sapowernetworks.com.au/meterdata/CADSiteLogin'
        CADSiteLogin_response = self._session.post(CADSiteLogin_url)

        if CADSiteLogin_response.status_code == 200:
            soup = BeautifulSoup(CADSiteLogin_response.text, 'html.parser')
            ViewState = soup.find('input', {'type': 'hidden', 'id': 'com.salesforce.visualforce.ViewState'})['value']  # type: ignore
            ViewStateMAC = soup.find('input', {'type': 'hidden', 'id': 'com.salesforce.visualforce.ViewStateMAC'})['value']  # type: ignore
        else:
            raise LoginError("failed to access login page")

        if ViewState[:2] != "i:" or ViewStateMAC[:3] != "AGV":
            raise LoginError("failed to retrieve ViewState or ViewStateMAC")
        
        CADSiteLogin_url = 'https://customer.portal.sapowernetworks.com.au/meterdata/CADSiteLogin'
        CADSiteLogin_form_data = {
            "loginPage:SiteTemplate:siteLogin:loginComponent:loginForm": "loginPage:SiteTemplate:siteLogin:loginComponent:loginForm",
            "loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:username": email,
            "loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:password": password,
            "loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:loginButton": "Login",
            "com.salesforce.visualforce.ViewState": ViewState,
            "com.salesforce.visualforce.ViewStateMAC": ViewStateMAC
        }
        CADSiteLogin_response = self._session.post(CADSiteLogin_url, data=CADSiteLogin_form_data)
        if(CADSiteLogin_response.status_code == 200):
            logger.info("successfully logged in")
        else:
            raise LoginError("failed to login")
        self._methods = {}
        text = CADSiteLogin_response.text
        link = text[text.find(".handleRedirect('")+17:text.find("'); }",text.find(".handleRedirect('")+17)]
        self._session.get(link)
    def _updateMethods(self, path: str) -> tuple:
        cadenergydashboard_url = f"https://customer.portal.sapowernetworks.com.au/meterdata/{path}"

        try:
            cadenergydashboard_response = self._session.get(cadenergydashboard_url)
            cadenergydashboard_response_data = cadenergydashboard_response.text
            cadenergydashboard_raw = cadenergydashboard_response_data[cadenergydashboard_response_data.find('{"vf":{"vid":"'):cadenergydashboard_response_data.find('"}));',cadenergydashboard_response_data.find('{"vf":{"vid":"'))+2]
            DataKeys_raw = json.loads(cadenergydashboard_raw)
        except:
            raise AuthError("Failed to retrive csrf and or authorization")
        action = ""
        for action in DataKeys_raw['actions']:
            self._methods[action] = {}
            for method in DataKeys_raw['actions'][action]['ms']:
                self._methods[action][method['name']] = {}
                self._methods[action][method['name']]['service'] = DataKeys_raw['service']
                self._methods[action][method['name']]['vf'] = DataKeys_raw['vf']
                for i in method:
                    if i != 'name':
                        self._methods[action][method['name']][i] = method[i]
            
        logger.debug(self._methods)
        return self._methods, action
    def _datafromMethod(self, path: str, method: str, data: list | None = None):
        methods, action = self._updateMethods(path)
        CADEnergyDashboardController_url = f"https://customer.portal.sapowernetworks.com.au/{self._methods[action][method]['service']}"
        CADEnergyDashboardController_body = {
            "action": action,
            "method": method,
            "type": "rpc",
            "tid": 1,
            "data": data,
            "ctx": {
                "csrf": self._methods[action][method]['csrf'],
                "vid": self._methods[action][method]['vf']['vid'],
                "ns": self._methods[action][method]['ns'],
                "ver": self._methods[action][method]['ver'],
                "authorization": self._methods[action][method]['authorization']
            }
        }
        if data is None:
            CADEnergyDashboardController_headers = {
                "referer": f"https://customer.portal.sapowernetworks.com.au/meterdata/{path}"
            }
        else:
            CADEnergyDashboardController_headers = {
                "Content-Type": "application/json",
                "referer": f"https://customer.portal.sapowernetworks.com.au/meterdata/{path}"
            }
        CADEnergyDashboardController_response = self._session.post(CADEnergyDashboardController_url, headers=CADEnergyDashboardController_headers, json=CADEnergyDashboardController_body)
        CADEnergyDashboardController_response_data = CADEnergyDashboardController_response.text
        CADEnergyDashboardController = json.loads(CADEnergyDashboardController_response_data)
        return CADEnergyDashboardController

    def getNMIs(self) -> list[int]:
        data = self._datafromMethod("CADAccountPage", "getNMIAssignments")
        nmis = []
        for nmi in data[0]['result']:
            nmis.append(nmi['theNMI'])
        return nmis
    
    def getAllData(self, start: datetime, end: datetime):
        nmis = self.getNMIs()
        data = getall(nmis, start, end, self)
        return data

class meter:
    def __init__(self, NMI:int, login_details:login):
        self.nmi = NMI
        self.login_details = login_details
    def getdata(self, startdate:datetime = datetime.today() - timedelta(2), enddate:datetime = datetime.today()):
        data = [
                self.nmi,
                "SAPN",
                startdate.strftime("%a, %d %b %Y %H:%M:%S GMT"),
                enddate.strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "Customer Access NEM12",
                "Detailed Report (CSV)",
                0
            ]
        downloadNMIData = self.login_details._datafromMethod("CADRequestMeterData", "downloadNMIData", data)
        try:
            self.data = downloadNMIData[0]['result']['results']
        except:
            return pd.DataFrame(columns=pd.MultiIndex.from_tuples([(str(self.nmi), "None")], names=['meter', 'channel']))

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(self.data)
            temp_path = f.name
        self.dataframes = nemreader.output_as_data_frames(temp_path, split_days=True, set_interval=None, strict=False)
        os.remove(temp_path)

        df = self.dataframes[0][1].drop(columns=['t_end', 'quality_method', 'evt_code', 'evt_desc'])
        for col in df.drop(columns=['t_start']).columns:
            df = df.rename(columns={col: f"{self.nmi}_{col}"})
        df.set_index('t_start', inplace=True)
        df.index = pd.to_datetime(df.index)
        df.columns = pd.MultiIndex.from_tuples([(str(self.nmi), c[-2:]) for c in df.columns], names=['meter', 'channel'])
        return df
        
@overload
def getall(meterlist: list[meter], start: datetime, end: datetime) -> pd.DataFrame: ...

@overload
def getall(meterlist: list[int], start: datetime, end: datetime, login_obj: login) -> pd.DataFrame: ...

def getall(meterlist, start, end, login_obj=None):
    meters = {}
    data = {}
    df = {}
    if isinstance(meterlist[0], meter):
        for nmi in meterlist:
            meters[nmi.nmi] = nmi
        nmis = list(meters.keys())
    else:
        if login_obj is None:
            raise ValueError("login must be provided when meterlist contains NMIs")
        for nmi in meterlist:
            meters[nmi] = meter(nmi, login_obj)
        nmis = meterlist
    for nmi in nmis:
        df[nmi] = meters[nmi].getdata(start, end)
    merged_df = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True, how='outer'), df.values())
    return merged_df.dropna(axis=1, how='all')