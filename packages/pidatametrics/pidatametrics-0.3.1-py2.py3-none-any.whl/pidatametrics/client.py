import requests
from requests.auth import HTTPBasicAuth

class PiDataMetrics:
    def __init__(self, client_id, client_secret, account_id=1505):
        self.account_id = account_id
        self.auth_url = "https://app.pi-datametrics.com/api/auth"
        self.base_url = f"https://app.pi-datametrics.com/api/accounts/{account_id}"
        self.access_token = self._get_access_token(client_id, client_secret)
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def _get_access_token(self, client_id, client_secret):
        data = {"grant_type": "client_credentials"}
        auth = HTTPBasicAuth(client_id, client_secret)
        try:
            response = requests.post(self.auth_url, data=data, auth=auth)
            response.raise_for_status()
            return response.json()['access_token']
        except requests.exceptions.RequestException as e:
            raise SystemExit(f"Authentication Failed: {e}")

    def fetch_endpoint(self, endpoint_path, params=None):
        url = f"{self.base_url}/{endpoint_path}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json().get('data', [])

    def get_workspaces(self):
        return self.fetch_endpoint("workspaces")

    def get_stgs(self, workspace_id):
        return self.fetch_endpoint(f"workspaces/{workspace_id}/search-term-groups")

    def get_search_terms(self, workspace_id, stg_id):
        return self.fetch_endpoint(f"workspaces/{workspace_id}/search-term-groups/{stg_id}/search-terms")

    def get_bulk_serp_data(self, workspace_id, search_engine_id, period, **kwargs):
        params = {"search-engine-id": search_engine_id, "period": period}
        params.update(kwargs)
        return self.fetch_endpoint(f"workspaces/{workspace_id}/search-data/bulk-search-results", params=params)

    def get_bulk_volume(self, workspace_id, start_date=None, end_date=None):
        params = {}
        if start_date and end_date:
            params = {'start-period': start_date, 'end-period': end_date}
        return self.fetch_endpoint(f"workspaces/{workspace_id}/volume-data/bulk-search-volume", params=params)

    # --- UPDATED: LLM Mentions Endpoint ---
    def get_llm_mentions(self, workspace_id, search_engine_id, start_period, end_period, stg_ids=None):
        url = "https://app.pi-datametrics.com/api/data/llm/mentions"
        
        # STRICT ORDERING: Account -> Workspace -> Start -> End -> Engine
        params = {
            "account-id": self.account_id,
            "workspace-id": workspace_id,
            "start-period": start_period,
            "end-period": end_period,
            "search-engine-id": search_engine_id
        }

        if stg_ids:
            params["search-term-group-id[]"] = stg_ids

        # We pass params to requests, which preserves insertion order in Python 3.7+
        response = requests.get(url, headers=self.headers, params=params)
        
        # Error Handling with detailed message
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"API Error: {e}")
            print(f"Requested URL: {response.url}") # Print the actual URL generated
            print(f"Response Body: {response.text}") # Print what the server said
            raise e

        return response.json().get('data', [])