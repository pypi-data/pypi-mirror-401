import requests
import logging
from typing import Optional, List, Dict, Any, Union, Iterator
from dataclasses import dataclass
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AgroDigitalSDK")

class AgroDigitalError(Exception):
    """Base exception for AgroDigital SDK errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response_body: Any = None):
        self.message = message
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(f"{message} (Status: {status_code})")

class APIObject:
    """
    Helper class to convert JSON dictionaries into Python objects 
    allowing dot notation access (e.g., obj.id instead of obj['id']).
    """
    def __init__(self, data: Dict[str, Any]):
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, APIObject(value))
            elif isinstance(value, list):
                setattr(self, key, [APIObject(item) if isinstance(item, dict) else item for item in value])
            else:
                setattr(self, key, value)
        self._raw_data = data

    def to_dict(self) -> Dict[str, Any]:
        """Returns the original dictionary representation."""
        return self._raw_data

    def __repr__(self):
        return f"<APIObject {self._raw_data}>"

class BaseManager:
    """Base class for resource managers handling HTTP requests."""
    
    def __init__(self, client, endpoint: str):
        self.client = client
        self.endpoint = endpoint

    def _build_url(self, path: str = "") -> str:
        base = self.endpoint if self.endpoint.endswith("/") else f"{self.endpoint}/"
        return f"{base}{path}"

    def _get(self, path: str = "", params: Optional[Dict] = None) -> Any:
        return self.client._request("GET", self._build_url(path), params=params)

    def _post(self, path: str = "", data: Optional[Dict] = None, json: Optional[Dict] = None) -> Any:
        return self.client._request("POST", self._build_url(path), data=data, json=json)

    def _put(self, path: str = "", json: Optional[Dict] = None) -> Any:
        return self.client._request("PUT", self._build_url(path), json=json)

    def _patch(self, path: str = "", json: Optional[Dict] = None) -> Any:
        return self.client._request("PATCH", self._build_url(path), json=json)

    def _delete(self, path: str = "") -> Any:
        return self.client._request("DELETE", self._build_url(path))

class CRUDManager(BaseManager):
    """
    Standard CRUD Manager for resources that support:
    List, Retrieve, Create, Update, Partial Update, Destroy.
    """

    def list(self, **kwargs) -> List[APIObject]:
        """
        List all resources.
        :param kwargs: Query parameters for filtering (e.g., page, limit, custom filters).
        """
        response = self._get(params=kwargs)
        if isinstance(response, list):
            return [APIObject(item) for item in response]
        # Handle paginated responses if API returns {results: [...]}
        if isinstance(response, dict) and "results" in response:
             return [APIObject(item) for item in response["results"]]
        return APIObject(response)

    def retrieve(self, id: Union[int, str], **kwargs) -> APIObject:
        """Retrieve a single resource by ID."""
        response = self._get(path=str(id), params=kwargs)
        return APIObject(response)

    def create(self, data: Dict[str, Any]) -> APIObject:
        """Create a new resource."""
        response = self._post(json=data)
        return APIObject(response)

    def update(self, id: Union[int, str], data: Dict[str, Any]) -> APIObject:
        """Update (replace) a resource."""
        response = self._put(path=str(id), json=data)
        return APIObject(response)

    def partial_update(self, id: Union[int, str], data: Dict[str, Any]) -> APIObject:
        """Partially update a resource."""
        response = self._patch(path=str(id), json=data)
        return APIObject(response)

    def delete(self, id: Union[int, str]) -> None:
        """Delete a resource."""
        self._delete(path=str(id))

class ReadOnlyManager(BaseManager):
    """Manager for resources that are read-only."""
    
    def list(self, **kwargs) -> List[APIObject]:
        response = self._get(params=kwargs)
        if isinstance(response, list):
            return [APIObject(item) for item in response]
        return APIObject(response)

    def retrieve(self, id: Union[int, str], **kwargs) -> APIObject:
        response = self._get(path=str(id), params=kwargs)
        return APIObject(response)

# --- Specific Managers for Specialized Logic ---

class AuthManager(BaseManager):
    def login(self, username, password) -> str:
        """
        Obtains an auth token. 
        Note: The client handles this internally if initialized with username/password,
        but this is exposed for manual usage.
        """
        data = {"username": username, "password": password}
        response = self._post(path="", json=data)
        return response.get("token")

    def register(self, user_data: Dict[str, Any]) -> APIObject:
        """Register a new user."""
        return APIObject(self._post(path="register/", json=user_data))

    def get_user(self) -> APIObject:
        """Retrieve current user details."""
        return APIObject(self._get(path="user/"))

    def update_user(self, data: Dict[str, Any]) -> APIObject:
        """Update current user details."""
        return APIObject(self._put(path="user/", json=data))
    
    def list_users(self) -> List[APIObject]:
        """List users (likely requires admin privileges)."""
        response = self._get(path="users/")
        return [APIObject(u) for u in response]

class ClusterManager(BaseManager):
    def ee_retrieve(self, from_date: str, to_date: str, polygon_id: str, n_clusters: int) -> APIObject:
        """Retrieve Google Earth Engine clusters."""
        params = {
            "from": from_date, "to": to_date, 
            "polygon": polygon_id, "n": n_clusters
        }
        return APIObject(self._get(path="ee/", params=params))

    def local_retrieve(self, from_date: str, to_date: str, polygon_id: str, 
                      n_clusters: int, source: str, input_type: str) -> APIObject:
        """Retrieve local clusters."""
        params = {
            "from": from_date, "to": to_date, "polygon": polygon_id, 
            "n": n_clusters, "source": source, "type": input_type
        }
        return APIObject(self._get(path="local/", params=params))

class RasterManager(CRUDManager):
    def discard(self, date: str, polygon_id: str, source: str) -> bool:
        """Discard a specific raster."""
        params = {"date": date, "polygon": polygon_id, "source": source}
        # This endpoint returns 200 OK on success, body might be empty or message
        self._get(path="discard/", params=params)
        return True

    def available_dates(self) -> Any:
        return self._get(path="dates/")

class IoTDataManager(CRUDManager):
    def list_data(self, station_id: int, from_date: str = None, to_date: str = None, 
                 variables: List[str] = None, convert: bool = False) -> List[APIObject]:
        """
        specialized list method for IoT Data with specific query params.
        """
        params = {"station": station_id}
        if from_date: params["from"] = from_date
        if to_date: params["to"] = to_date
        if convert: params["convert"] = "true"
        # Handling list of variables for query param array format (e.g. ?variables=1&variables=2)
        # Requests library handles list in params usually, but format depends on API (comma vs repeated)
        if variables: params["variables"] = variables 
        
        response = self._get(params=params)
        return [APIObject(item) for item in response]

class MeteoDataManager(CRUDManager):
    def list_data(self, station_id: int = None, field_id: int = None, 
                 from_date: str = None, to_date: str = None, 
                 variables: List[str] = None) -> List[APIObject]:
        params = {}
        if station_id: params["station"] = station_id
        if field_id: params["field"] = field_id
        if from_date: params["from"] = from_date
        if to_date: params["to"] = to_date
        if variables: params["variables"] = variables
        
        response = self._get(params=params)
        return [APIObject(item) for item in response]


# --- Main Client ---

class AgroDigitalClient:
    """
    Main entry point for the AgroDigital API SDK.
    """
    
    BASE_URL = "https://agrodigital.io/api" # Verify actual base URL

    def __init__(self, token: str = None, username: str = None, password: str = None, base_url: str = None):
        """
        Initialize the client.
        
        :param token: Existing API Token.
        :param username: Username for auth (if token not provided).
        :param password: Password for auth.
        :param base_url: Override default base URL.
        """
        self.base_url = base_url or self.BASE_URL
        self.session = requests.Session()
        
        if token:
            self._set_token(token)
        elif username and password:
            self._authenticate(username, password)
        else:
            logger.warning("Client initialized without credentials. Call login() or set_token() before requests.")

        # -- Initialize Managers --
        
        # Core Agricultural Entities
        self.farms = CRUDManager(self, "farms")
        self.fields = CRUDManager(self, "fields")
        self.polygons = CRUDManager(self, "polygons")
        self.crops = ReadOnlyManager(self, "crops")
        self.varieties = ReadOnlyManager(self, "varieties")
        self.companies = ReadOnlyManager(self, "companies")
        
        # Operations / Logs
        self.logs = CRUDManager(self, "logs")
        self.sowing = CRUDManager(self, "logs") # Polymorphic via logs, strictly speaking logic handled by payload type
        self.applications = CRUDManager(self, "logs") 
        self.fertilizers = ReadOnlyManager(self, "fertilizers")
        self.agrochemicals = ReadOnlyManager(self, "agroq")
        
        # Monitoring / Data
        self.rasters = RasterManager(self, "rasters")
        self.indexes = CRUDManager(self, "indexes")
        self.cluster = ClusterManager(self, "cluster")
        
        # IoT & Meteo
        self.iot_data = IoTDataManager(self, "iot/data")
        self.iot_stations = CRUDManager(self, "iot/stations")
        self.iot_variables = ReadOnlyManager(self, "iot/variables")
        
        self.meteo_data = MeteoDataManager(self, "meteo/data")
        self.meteo_stations = CRUDManager(self, "meteo/stations")
        self.meteo_variables = ReadOnlyManager(self, "meteo/variables")
        
        # Scouts / Issues
        self.bugs = ReadOnlyManager(self, "bugs")
        self.weeds = ReadOnlyManager(self, "weeds")
        self.diseases = ReadOnlyManager(self, "diseases")
        self.waypoints = CRUDManager(self, "waypoints")
        
        # System
        self.auth = AuthManager(self, "auth")
        self.notifications = CRUDManager(self, "notifications")
        self.licenses = CRUDManager(self, "licenses")

    def _authenticate(self, username, password):
        """Internal method to get token using the AuthManager logic."""
        url = f"{self.base_url}/auth/"
        try:
            resp = self.session.post(url, json={"username": username, "password": password})
            resp.raise_for_status()
            data = resp.json()
            self._set_token(data['token'])
        except requests.exceptions.RequestException as e:
            raise AgroDigitalError(f"Authentication failed: {str(e)}")

    def _set_token(self, token: str):
        """Sets the Authorization header for the session."""
        self.token = token
        self.session.headers.update({
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(self, method: str, url: str, **kwargs) -> Any:
        """Centralized request handler with error processing."""
        # Ensure URL is complete
        if not url.startswith("http"):
            url = urljoin(self.base_url + "/", url)

        # Remove None values from params to keep query clean
        if 'params' in kwargs and kwargs['params']:
            kwargs['params'] = {k: v for k, v in kwargs['params'].items() if v is not None}

        logger.debug(f"Request: {method} {url} - Params: {kwargs.get('params')} - JSON: {kwargs.get('json')}")

        try:
            response = self.session.request(method, url, **kwargs)
            
            # Raise generic HTTP errors
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                # Try to extract API specific error message
                try:
                    error_body = response.json()
                except ValueError:
                    error_body = response.text
                raise AgroDigitalError(
                    message=f"API Error {response.status_code}",
                    status_code=response.status_code,
                    response_body=error_body
                )

            # Return None for 204 No Content
            if response.status_code == 204:
                return None
            
            # Attempt to parse JSON
            try:
                return response.json()
            except ValueError:
                return response.content

        except requests.exceptions.ConnectionError:
            raise AgroDigitalError("Network connection error")
        except requests.exceptions.Timeout:
            raise AgroDigitalError("Request timed out")