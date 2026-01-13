"""
CheatLab API Client
"""

import requests
from typing import Optional, Dict, Any, Union


class CheatLabError(Exception):
    """Base exception for CheatLab errors"""
    pass


class AuthenticationError(CheatLabError):
    """Raised when authentication fails"""
    pass


class APIError(CheatLabError):
    """Raised when API returns an error"""
    pass


class Cheat:
    """
    CheatLab API Client
    
    Args:
        username: Your CheatLab username
        auth_key: Your authentication key
        base_url: API base URL (default: https://cheatlab.onrender.com)
    
    Example:
        >>> cheat = Cheat("myusername", "my_auth_key")
        >>> cheat.post("Hello World", key="greeting")
        >>> print(cheat.get("greeting"))
    """
    
    def __init__(self, username: str, auth_key: str, base_url: str = "https://cheatlab.onrender.com"):
        self.username = username
        self.auth_key = auth_key
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "x-username": username,
            "x-auth-key": auth_key
        })
    
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make an authenticated request to the API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            # Handle authentication errors
            if response.status_code == 401:
                raise AuthenticationError(f"Authentication failed: {response.text}")
            
            # Handle forbidden errors
            if response.status_code == 403:
                raise APIError(f"Access denied: {response.text}")
            
            # Handle other errors
            if response.status_code >= 400:
                raise APIError(f"API error ({response.status_code}): {response.text}")
            
            return response
            
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")
    
    def ping(self) -> str:
        """
        Check if API is alive
        
        Returns:
            "pong" if API is responding
        """
        response = self._request("GET", "/ping")
        return response.text
    
    def get(self, target: Union[str, int], password: Optional[str] = None, 
            details: bool = False, admin_pass: Optional[str] = None) -> Union[str, Dict[str, Any]]:
        """
        Retrieve a message by ID, key, or 'latest'
        
        Args:
            target: Message ID (int), key (str), or "latest"
            password: Password for protected messages
            details: If True, return full JSON details; if False, return text only
            admin_pass: Admin password to bypass protection
        
        Returns:
            Message text (str) or full message details (dict) if details=True
        
        Examples:
            >>> cheat.get("latest")
            >>> cheat.get(47)
            >>> cheat.get("mykey")
            >>> cheat.get("mykey", password="secret", details=True)
            >>> cheat.get("mykey", admin_pass="admin_password")
        """
        params = {}
        if password:
            params["password"] = password
        if details:
            params["details"] = "true"
        if admin_pass:
            params["admin_pass"] = admin_pass
        
        # Determine endpoint
        if target == "latest":
            endpoint = "/latest"
        elif isinstance(target, int) or (isinstance(target, str) and target.isdigit()):
            endpoint = f"/{target}"
        else:
            endpoint = f"/key/{target}"
        
        response = self._request("GET", endpoint, params=params)
        
        if details:
            return response.json()
        return response.text
    
    def post(self, text: str, key: Optional[str] = None, password: Optional[str] = None,
             who: Optional[str] = None, protect_view: bool = False, 
             protect_delete: bool = False) -> Dict[str, Any]:
        """
        Create a new message
        
        Args:
            text: Message content
            key: Custom key for easy retrieval (must be unique)
            password: Password for protection
            who: Author/creator name
            protect_view: Require password to view
            protect_delete: Require password to delete
        
        Returns:
            Dict with 'success' and 'id' of created message
        
        Examples:
            >>> cheat.post("Hello World")
            >>> cheat.post("My snippet", key="greet")
            >>> cheat.post("Private data", key="secret", password="pass123", 
            ...            protect_view=True, protect_delete=True)
        """
        data = {
            "text": text,
            "protect_view": protect_view,
            "protect_delete": protect_delete
        }
        
        if key:
            data["key"] = key
        if password:
            data["password"] = password
        if who:
            data["who"] = who
        
        response = self._request("POST", "/new", json=data)
        return response.json()
    
    def add(self, text: str, key: Optional[str] = None, password: Optional[str] = None,
            who: Optional[str] = None, protect_view: bool = False, 
            protect_delete: bool = False) -> str:
        """
        Create a new message using GET method (alternative to post)
        
        Args:
            text: Message content
            key: Custom key for easy retrieval (must be unique)
            password: Password for protection
            who: Author/creator name
            protect_view: Require password to view
            protect_delete: Require password to delete
        
        Returns:
            "ok:{id}" on success
        """
        params = {
            "text": text,
            "protect_view": str(protect_view).lower(),
            "protect_delete": str(protect_delete).lower()
        }
        
        if key:
            params["key"] = key
        if password:
            params["password"] = password
        if who:
            params["who"] = who
        
        response = self._request("GET", "/add", params=params)
        return response.text
    
    def delete(self, target: Union[str, int], password: Optional[str] = None, 
               admin_pass: Optional[str] = None) -> str:
        """
        Delete a message by ID, key, or 'latest'
        
        Args:
            target: Message ID (int), key (str), or "latest"
            password: Password if message is protected
            admin_pass: Admin password to bypass protection
        
        Returns:
            "deleted" on success
        
        Examples:
            >>> cheat.delete(47)
            >>> cheat.delete("latest")
            >>> cheat.delete("mykey", password="secret")
            >>> cheat.delete("mykey", admin_pass="admin_password")
        """
        params = {}
        if password:
            params["password"] = password
        if admin_pass:
            params["admin_pass"] = admin_pass
        
        # Determine endpoint
        if target == "latest":
            endpoint = "/latest"
        elif isinstance(target, int) or (isinstance(target, str) and target.isdigit()):
            endpoint = f"/{target}"
        else:
            endpoint = f"/key/{target}"
        
        response = self._request("DELETE", endpoint, params=params)
        return response.text
    
    def ai(self, prompt: str) -> str:
        """
        Ask the AI assistant a question
        
        Args:
            prompt: Your question or prompt
        
        Returns:
            AI response text
        
        Example:
            >>> response = cheat.ai("what is recursion?")
            >>> print(response)
        
        Note:
            Requires AI access enabled on your account
        """
        params = {"prompt": prompt}
        response = self._request("GET", "/ai", params=params)
        return response.text
    
    def get_all(self, admin_pass: str) -> Dict[str, Any]:
        """
        Get all messages (requires admin password)
        
        Args:
            admin_pass: Admin password
        
        Returns:
            Dict with 'count' and 'messages' list
        
        Example:
            >>> data = cheat.get_all("admin_password")
            >>> print(f"Total messages: {data['count']}")
        """
        params = {"admin_pass": admin_pass}
        response = self._request("GET", "/all", params=params)
        return response.json()
    
    def get_uidata(self) -> Dict[str, Any]:
        """
        Get safe list of all messages (protected content hidden)
        
        Returns:
            Dict with 'count' and 'messages' list
        
        Example:
            >>> data = cheat.get_uidata()
            >>> for msg in data['messages']:
            ...     print(f"{msg['id']}: {msg.get('text', '[protected]')}")
        """
        response = self._request("GET", "/uidata")
        return response.json()
    
    def __repr__(self) -> str:
        return f"Cheat(username='{self.username}', base_url='{self.base_url}')"
