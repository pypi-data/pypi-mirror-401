import requests
import pandas as pd
import re
import base64
from typing import List, Union, Literal, Optional
from brynq_sdk_brynq import BrynQ


class GetData(BrynQ):
    def __init__(self, system_type: Optional[Literal['source', 'target']] = None, debug: bool = False):
        """"
        For the documentation of SAP, see: https://help.sap.com/docs/SAP_SUCCESSFACTORS_PLATFORM/d599f15995d348a1b45ba5603e2aba9b/0491f8c9f81b4112a18cabcefc082490.html
        """
        super().__init__()
        self.timeout = 3600
        self.base_url, self.headers = self._set_credentials(system_type)

    def _set_credentials(self, system_type):
        """
        Sets the credentials for the SuccessFactors API.
        Supports both OAuth2 with SAML (when client_id is provided) and Basic Authentication (when client_id is None).

        Parameters:
        system_type: The system type for the credentials.

        Returns:
        base_url (str): The base URL for the API.
        headers (dict): The headers for the API request, including the access token or basic auth.
        """
        credentials = self.interfaces.credentials.get(system="successfactors", system_type=system_type)
        credentials = credentials.get('data')
        base_url = credentials['base_url']
        token_url = credentials['auth_url']
        client_id = credentials.get('client_id')
        company_id = credentials['company_id']
        user_id = credentials['username']
        private_key = credentials['password']

        # If client_id is None or empty, use Basic Authentication
        if not client_id:
            credentials_string = f"{user_id}:{private_key}"
            encoded_credentials = base64.b64encode(credentials_string.encode()).decode('utf-8')
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Basic {encoded_credentials}'
            }
            return base_url, headers

        # Get the SAML assertion
        url = f'{base_url}/oauth/idp'
        payload = {
            'client_id': client_id,
            'user_id': user_id,
            'token_url': token_url,
            'private_key': private_key
        }
        response = requests.request("POST", url, data=payload, timeout=self.timeout)
        saml_assertion = response.text

        # Now get the access_token
        payload = {
            'client_id': client_id,
            'grant_type': 'urn:ietf:params:oauth:grant-type:saml2-bearer',
            'company_id': company_id,
            'assertion': saml_assertion
        }
        response = requests.request("POST", url=token_url, data=payload, timeout=self.timeout)
        access_token = response.json()['access_token']
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        return base_url, headers

    @staticmethod
    def _convert_date_columns(df):
        max_timestamp = pd.Timestamp.max.value // 10**6
        min_timestamp = pd.Timestamp.min.value // 10**6
        for col in df.columns:
            if df[col].dtype == 'object' and df[col].apply(lambda x: isinstance(x, str)).any():  # if the column is of object type
                # Check if any cell in the column matches the pattern
                if df[col].str.contains(r'/Date\(-?\d+(\+\d+)?\)/', regex=True).any():
                    # Extract the timestamp and convert it to datetime, including minus sign for negative timestamps
                    df[col] = df[col].str.extract(r'(-?\d+)', expand=False).astype('float')

                    # Convert timestamps to datetime with error handling
                    def safe_convert(x):
                        try:
                            # Check if timestamp is within valid pandas datetime range
                            if x is not None and min_timestamp <= x <= max_timestamp:
                                return pd.to_datetime(x, unit='ms')
                            return None
                        except Exception:
                            return None

                    df[col] = df[col].apply(safe_convert)
        return df

    def get_odata(self, endpoint: str, select: str = None, filter: str = None, filter_date: str = None, orderby: str = None):
        """
        Download data from successfactors via the OData method.
        :param endpoint: give the endpoint you want to call
        :param select: optional. Give a list of fields you want to select. Comma seperated, no spaces in between. Example: seqNumber,startDate,userId
        :param filter: Optional. Enter a filter in OData format. See here more information: https://help.sap.com/docs/SAP_SUCCESSFACTORS_PLATFORM/d599f15995d348a1b45ba5603e2aba9b/ded5808b5edb4bc9a8acfb5e9fe1b025.html
        :param orderby: Optional. Order results by a field. Example: createdDateTime desc.
                       Defaults to 'createdDateTime desc' to ensure all records are retrieved.
                       If endpoint doesn't support ordering, automatically falls back to no ordering.
                       Pass empty string '' to explicitly disable ordering.
        """
        # Default to createdDateTime desc to ensure all records are retrieved (prevents missing recently created records)
        use_default_orderby = orderby is None
        if use_default_orderby:
            orderby = 'createdDateTime desc'

        # Build query parameters
        query_params = []
        query_params.extend([f'$select={select}'] if select else [])
        query_params.extend([f'$filter={filter}'] if filter else [])
        query_params.extend([f'$filter={filter_date}'] if filter_date else [])
        query_params.extend([f'$orderby={orderby}'] if orderby else [])

        # Construct initial URL
        base_endpoint_url = f'{self.base_url}/odata/v2/{endpoint}'
        url = f'{base_endpoint_url}?{"&".join(query_params)}' if query_params else base_endpoint_url

        df = pd.DataFrame()
        max_pages = 10000  # Safety limit to prevent infinite loops
        orderby_failed = False

        for page_count in range(max_pages):
            response = requests.request("GET", url, headers=self.headers, timeout=self.timeout)

            # If we used default ordering and got a 400 error on first page, retry without ordering
            if response.status_code == 400 and use_default_orderby and orderby and page_count == 0 and not orderby_failed:
                # Retry without ordering
                query_params_no_orderby = []
                query_params_no_orderby.extend([f'$select={select}'] if select else [])
                query_params_no_orderby.extend([f'$filter={filter}'] if filter else [])
                query_params_no_orderby.extend([f'$filter={filter_date}'] if filter_date else [])
                url = f'{base_endpoint_url}?{"&".join(query_params_no_orderby)}' if query_params_no_orderby else base_endpoint_url
                response = requests.request("GET", url, headers=self.headers, timeout=self.timeout)
                orderby_failed = True

            response.raise_for_status()

            response_data = response.json()['d']
            data = response_data['results']
            next_url = response_data.get('__next')

            # Append data to DataFrame
            df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)

            # Break if no more pages
            if not next_url:
                break

            # Use __next URL directly (API returns absolute URLs)
            url = next_url

        # Reformat eventual date columns to pd.datetime
        df = self._convert_date_columns(df)
        return df
