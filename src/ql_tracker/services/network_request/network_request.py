import requests


class NetworkRequestService:
    """
    Service for making network requests.
    """
    
    def __init__(self,base_url:str,api_key) -> None:
        """
        Initialize the network request service.
        """
        assert base_url, "Base URL must be provided"
        assert api_key, "API key must be provided"
        self.base_url = base_url
        self.api_key = api_key
        self._running = True
        self._session = requests.Session()
        self._session.headers.update({
            'api_key': self.api_key,
            'Content-Type': 'application/json',
        })

    def batch_post(
        self,
        endpoint: str,
        data: list,
        timeout: int = 10
    ) -> requests.Response:
        """
        Send a batch POST request to the specified endpoint.
        
        Args:
            endpoint: API endpoint to send the request to
            data: List of data to send in the request body
            timeout: Timeout for the request in seconds
            
        Returns:
            Response object from the request library
        """
        # Send logs to the API
        url = f"{self.base_url}/{endpoint}"
        print(f"Sending POST request to: {url}")
        print(f"Data count: {len(data)} logs")

        response = self._session.post(url, json=data, timeout=timeout)
        response.raise_for_status()
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.json()}")
        return response