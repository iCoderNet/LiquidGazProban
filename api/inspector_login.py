import requests
import time
from typing import Optional, Dict, Any
import os


class EgazAPI:
    """
    A client for interacting with the egaz.uz API.
    
    This class provides methods to login, fetch dictionary data, and retrieve inspector details.
    """
    
    BASE_URL = 'https://egaz.uz/api'
    
    def __init__(
        self,
        auth_token: str = 'f6ef8971c9e7b485e6ee68313e36d982',
        auth_time: Optional[int] = None
    ):
        """
        Initialize the Egaz API client.
        
        Args:
            auth_token: Authorization token for API requests
            auth_time: Authorization timestamp in milliseconds (defaults to current time)
        """
        self.auth_token = auth_token
        self.auth_time = auth_time if auth_time is not None else int(time.time() * 1000)
        self.user_id = None
        self.auth_hash = None
        
    def _get_headers(self) -> Dict[str, str]:
        """
        Get common headers for API requests.
        
        Returns:
            Dict containing HTTP headers
        """
        return {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'egaz.uz',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Authorization-Token': self.auth_token,
            'X-Authorization-Time': str(self.auth_time),
            'X-Device': 'false',
            'X-Unknown': 'true',
            'User-Agent': 'ANDROID/2201117TG/259',
            'CLIENT_NAME': 'EGAZ',
            'Accept-Language': 'en'
        }
    
    def inspector_login(
        self,
        email: str,
        password: str,
        location: str = "41.311081,69.240562",
        ip: str = "10.52.79.219",
        device: str = 'Device:spes Model:2201117TG'
    ) -> Dict[Any, Any]:
        """
        Login to the egaz.uz inspector system.
        
        Args:
            email: Inspector email address (e.g., '01124000104@hgt.uz')
            password: Inspector password
            location: GPS coordinates as 'latitude,longitude' (e.g., '41.311081,69.240562')
            ip: Device IP address
            device: Device information (e.g., 'Device:spes Model:2201117TG')
        
        Returns:
            Dict containing the API response
            Response: {
                "api_status": 1,
                "api_message": "success",
                "api_http": 200,
                "data": {
                    "id": 5975696,
                    "email": "01124000104@hgt.uz",
                    "kod": "01124000104",
                    "lastlogin": "2025-11-23 21:03:51",
                    "name": "MADAMINOV BOBIRJON MIRZAJON О'G'LI",
                    "id_region": 1,
                    "id_district": 4,
                    "id_org": 122,
                    "org_name": "Асака туман ГАЗ",
                    "privileges_id": 3,
                    "privileges_name": "Инспектор Райгаз",
                    "status": "Active"
                }
            }
        
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = f'{self.BASE_URL}/inspector_login'
        
        data = {
            'email': email,
            'psw': password,
            'location': location,
            'ip': ip,
            'device': device
        }
        
        response = requests.post(url, headers=self._get_headers(), data=data)
        response.raise_for_status()
        
        result = response.json()
        
        # Store user_id for subsequent requests
        if result.get('api_status') == 1 and 'data' in result:
            self.user_id = result['data'].get('id')
        
        return result
    
    def dictionary_data(
        self,
        oper: str,
        id_user: Optional[str] = None,
        auth_hash: Optional[str] = None,
        id_region: Optional[str] = None,
        type: Optional[str] = None
    ) -> Dict[Any, Any]:
        """
        Fetch dictionary data from egaz.uz API.
        
        Args:
            oper: Operation type (e.g., 'organizations')
            id_user: User ID (uses stored user_id if not provided)
            auth_hash: Authentication hash
            id_region: Optional region ID
            type: Optional type filter (e.g., 'rgs')
        
        Returns:
            Dict containing the API response
            Response: {
                "api_status": 1,
                "api_message": "success",
                "api_http": 200,
                "data": [
                    {
                        "id": 119,
                        "inn": "306605769",
                        "account": "22604000305113960102",
                        "branch": "00440",
                        "bname": "\"УЗСАНОАТКУРИЛИШБАНКИ\" АТБ РАКАТ ФИЛИА",
                        "name": "Андижон шахар ГАЗ",
                        "region": "Андижон вилояти",
                        "district": "АНДИЖОН ШАХРИ",
                        "org_type": "Районный ГАЗ",
                        "tags": "РАЙГАЗ",
                        "description": null
                    }
                ]
            }
        
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = f'{self.BASE_URL}/dictionary_data'
        
        # Use stored user_id if not provided
        if id_user is None and self.user_id is not None:
            id_user = str(self.user_id)
        
        data = {
            'oper': oper,
            'id_user': id_user,
            'auth_hash': auth_hash
        }
        
        # Add optional parameters if provided
        if id_region is not None:
            data['id_region'] = id_region
        if type is not None:
            data['type'] = type
        
        response = requests.post(url, headers=self._get_headers(), data=data)
        response.raise_for_status()
        
        return response.json()
    
    def inspector_data(
        self,
        oper: str,
        inspector_kod: str,
        type: str,
        id_org: str,
        id_user: Optional[str] = None,
        auth_hash: Optional[str] = None
    ) -> Dict[Any, Any]:
        """
        Fetch inspector data from egaz.uz API.
        
        Args:
            oper: Operation type (e.g., 'detail')
            inspector_kod: Inspector code (e.g., '01124000104')
            type: Type filter (e.g., 'rgs')
            id_org: Organization ID
            id_user: User ID (uses stored user_id if not provided)
            auth_hash: Authentication hash
        
        Returns:
            Dict containing the API response with inspector details
        
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = f'{self.BASE_URL}/inspector_data'
        
        # Use stored user_id if not provided
        if id_user is None and self.user_id is not None:
            id_user = str(self.user_id)
        
        data = {
            'oper': oper,
            'inspector_kod': inspector_kod,
            'type': type,
            'id_org': id_org,
            'id_user': id_user,
            'auth_hash': auth_hash
        }
        
        response = requests.post(url, headers=self._get_headers(), data=data)
        response.raise_for_status()
        
        return response.json()
    
    def ballon_requests_rgs(
        self,
        oper: str,
        id_rgs: Optional[str] = None,
        id_request: Optional[str] = None,
        id_user: Optional[str] = None,
        auth_hash: Optional[str] = None,
        take: int = 20,
        offset: int = 0
    ) -> Dict[Any, Any]:
        """
        Fetch ballon requests for RGS from egaz.uz API.
        
        Args:
            oper: Operation type ('list' or 'planning')
            id_rgs: RGS organization ID (required for 'list' operation)
            id_request: Request ID (required for 'planning' operation)
            id_user: User ID (uses stored user_id if not provided)
            auth_hash: Authentication hash
            take: Number of records to fetch (default: 20, used for 'list' operation)
            offset: Offset for pagination (default: 0, used for 'list' operation)
        
        Returns:
            Dict containing the API response with ballon requests
        
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = f'{self.BASE_URL}/ballon_requests_rgs'
        
        # Use stored user_id if not provided
        if id_user is None and self.user_id is not None:
            id_user = str(self.user_id)
        
        data = {
            'oper': oper,
            'id_user': id_user,
            'auth_hash': auth_hash
        }
        
        # Add parameters based on operation type
        if oper == 'list':
            data['id_rgs'] = id_rgs
            data['take'] = str(take)
            data['offset'] = str(offset)
        elif oper == 'planning':
            data['id_request'] = id_request
        
        response = requests.post(url, headers=self._get_headers(), data=data)
        response.raise_for_status()
        
        return response.json()
    
    def abon_data(
        self,
        oper: str,
        abonent_kod: str,
        id_user: Optional[str] = None,
        auth_hash: Optional[str] = None,
        id_org: Optional[str] = None,
        take: int = 100,
        offset: int = 0
    ) -> Dict[Any, Any]:
        """
        Fetch abonent (subscriber) data from egaz.uz API.
        
        Args:
            oper: Operation type ('detail' or 'realization_history')
            abonent_kod: Abonent code (e.g., '01000444264')
            id_user: User ID (uses stored user_id if not provided)
            auth_hash: Authentication hash
            id_org: Organization ID (required for 'detail' operation)
            take: Number of records to fetch (default: 100, used for 'realization_history')
            offset: Offset for pagination (default: 0, used for 'realization_history')
        
        Returns:
            Dict containing the API response with abonent data
        
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = f'{self.BASE_URL}/abon_data'
        
        # Use stored user_id if not provided
        if id_user is None and self.user_id is not None:
            id_user = str(self.user_id)
        
        data = {
            'oper': oper,
            'abonent_kod': abonent_kod,
            'id_user': id_user,
            'auth_hash': auth_hash
        }
        
        # Add parameters based on operation type
        if oper == 'detail':
            data['id_org'] = id_org
        elif oper == 'realization_history':
            data['take'] = str(take)
            data['offset'] = str(offset)
        
        response = requests.post(url, headers=self._get_headers(), data=data)
        response.raise_for_status()
        
        return response.json()
    
    def ballon_data(
        self,
        oper: str,
        ballon_kod: str,
        id_rgs: str = '0',
        id_user: Optional[str] = None,
        auth_hash: Optional[str] = None
    ) -> Dict[Any, Any]:
        """
        Fetch ballon data from egaz.uz API.
        
        Args:
            oper: Operation type (e.g., 'detail')
            ballon_kod: Ballon code (e.g., '88001290026123059')
            id_rgs: RGS organization ID (default: '0')
            id_user: User ID (uses stored user_id if not provided)
            auth_hash: Authentication hash
        
        Returns:
            Dict containing the API response with ballon details
        
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = f'{self.BASE_URL}/ballon_data'
        
        # Use stored user_id if not provided
        if id_user is None and self.user_id is not None:
            id_user = str(self.user_id)
        
        data = {
            'oper': oper,
            'ballon_kod': ballon_kod,
            'id_rgs': id_rgs,
            'id_user': id_user,
            'auth_hash': auth_hash
        }
        
        response = requests.post(url, headers=self._get_headers(), data=data)
        response.raise_for_status()
        
        return response.json()
    def _get_multipart_headers(self) -> Dict[str, str]:
        """
        Get headers for multipart form data requests (without Content-Type).
        
        Returns:
            Dict containing HTTP headers
        """
        headers = self._get_headers()
        # Remove Content-Type as it will be set automatically by requests library
        del headers['Content-Type']
        return headers
    
    def submit_ballon_request(
        self,
        oper: str,
        id_rgs: int,
        id_request: int,
        ballon_kod: str,
        next_rdt: int,
        abonent_kod: str,
        location_lon: float,
        location_lat: float,
        abon_pinfl: str,
        photo_path: str,
        ballon_hash: Optional[str] = None,
        others: Optional[str] = None,
        abon_relation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Submit a balloon request with photo.
        
        Args:
            oper: Operation type (e.g., "realization")
            id_rgs: RGS ID
            id_request: Request ID
            ballon_kod: Balloon code (17 digits)
            next_rdt: Next RDT value
            abonent_kod: Abonent code (11 digits)
            location_lon: Longitude coordinate
            location_lat: Latitude coordinate
            abon_pinfl: Abonent PINFL (14 digits)
            photo_path: Path to the photo file (JPEG)
            ballon_hash: Optional balloon hash
            others: Optional other data
            abon_relation_id: Optional abonent relation ID
        
        Returns:
            API response as dictionary
        
        Raises:
            requests.exceptions.RequestException: If request fails
            FileNotFoundError: If photo file doesn't exist
            ValueError: If user is not logged in
        """
        # Check if user is logged in
        if not self.user_id or not self.auth_hash:
            raise ValueError("User must be logged in first. Call login() method.")
        
        # Check if photo file exists
        if not os.path.exists(photo_path):
            raise FileNotFoundError(f"Photo file not found: {photo_path}")
        
        # Prepare multipart form data
        files = {
            'oper': (None, oper),
            'id_rgs': (None, str(id_rgs)),
            'auth_hash': (None, self.auth_hash),
            'id_user': (None, str(self.user_id)),
            'id_request': (None, str(id_request)),
            'ballon_kod': (None, ballon_kod),
            'ballon_hash': (None, ballon_hash if ballon_hash else 'null'),
            'next_rdt': (None, str(next_rdt)),
            'abonent_kod': (None, abonent_kod),
            'others': (None, others if others else 'null'),
            'abon_relation_id': (None, abon_relation_id if abon_relation_id else ''),
            'location_lon': (None, str(location_lon)),
            'location_lat': (None, str(location_lat)),
            'abon_pinfl': (None, abon_pinfl),
            'photo': (os.path.basename(photo_path), open(photo_path, 'rb'), 'image/jpeg')
        }
        
        try:
            response = requests.post(
                f'{self.BASE_URL}/ballon_requests_rgs',
                files=files,
                headers=self._get_multipart_headers(),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Failed to submit balloon request: {e}")
        finally:
            # Close the file handle
            if 'photo' in files and hasattr(files['photo'][1], 'close'):
                files['photo'][1].close()


# Example usage
if __name__ == '__main__':
    try:
        # Initialize the API client
        api = EgazAPI(
            auth_token='f6ef8971c9e7b485e6ee68313e36d982',
            auth_time=1763885338884
        )
        
        # Login example
        print('=== LOGIN ===')
        login_result = api.inspector_login(
            email='01124000104@hgt.uz',
            password='SN47NGG2Y2IY'
        )
        print('Login successful!')
        print(login_result)
        
        if login_result['api_status'] != 1:
            print(f'Login failed: {login_result["api_message"]}')
            exit()
        
        # Extract data from login response
        user_data = login_result['data']
        id_region = user_data['id_region']
        user_id = user_data['id']
        inspector_kod = user_data['kod']
        id_org = user_data['id_org']
        
        # Dictionary data example
        print('\n=== DICTIONARY DATA ===')
        dict_result = api.dictionary_data(
            oper='organizations',
            id_region=str(id_region),
            type='rgs',
            auth_hash='5838c81115746ac9ac438dd1934f8792'
        )
        print('Dictionary data fetched successfully!')
        print(dict_result)
        
        # Inspector data example
        print('\n=== INSPECTOR DATA ===')
        inspector_result = api.inspector_data(
            oper='detail',
            inspector_kod=inspector_kod,
            type='rgs',
            id_org=str(id_org),
            auth_hash='5838c81115746ac9ac438dd1934f8792'
        )
        print('Inspector data fetched successfully!')
        print(inspector_result)
        
        # Ballon requests RGS - List example
        print('\n=== BALLON REQUESTS RGS (LIST) ===')
        ballon_requests_list = api.ballon_requests_rgs(
            oper='list',
            id_rgs=str(id_org),
            auth_hash='5838c81115746ac9ac438dd1934f8792',
            take=20,
            offset=0
        )
        print('Ballon requests list fetched successfully!')
        print(ballon_requests_list)
        
        # Ballon requests RGS - Planning example (uncomment when you have a valid request ID)
        # print('\n=== BALLON REQUESTS RGS (PLANNING) ===')
        # ballon_planning = api.ballon_requests_rgs(
        #     oper='planning',
        #     id_request='1269233',
        #     auth_hash='a8f56b5a74791fbd995e6c68f54648ba'
        # )
        # print('Ballon planning fetched successfully!')
        # print(ballon_planning)
        
        # Abonent data - Detail example
        print('\n=== ABONENT DATA (DETAIL) ===')
        abon_detail = api.abon_data(
            oper='detail',
            abonent_kod='01000444264',
            id_org=str(id_org),
            auth_hash='a8f56b5a74791fbd995e6c68f54648ba'
        )
        print('Abonent detail fetched successfully!')
        print(abon_detail)
        
        # Abonent data - Realization history example
        print('\n=== ABONENT DATA (REALIZATION HISTORY) ===')
        abon_history = api.abon_data(
            oper='realization_history',
            abonent_kod='01000444264',
            auth_hash='a8f56b5a74791fbd995e6c68f54648ba',
            take=100,
            offset=0
        )
        print('Abonent realization history fetched successfully!')
        print(abon_history)
        
        # Ballon data - Detail example
        print('\n=== BALLON DATA (DETAIL) ===')
        ballon_detail = api.ballon_data(
            oper='detail',
            ballon_kod='88001290026123059',
            id_rgs='0',
            auth_hash='a8f56b5a74791fbd995e6c68f54648ba'
        )
        print('Ballon detail fetched successfully!')
        print(ballon_detail)
        
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')

