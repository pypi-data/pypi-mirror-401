"""HTTP client for MCE Server API."""

import json
import requests
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin, quote

from .config import Config
from .exceptions import MCEClientError, MCEServerError


class MCEClient:
    """HTTP client for MCE Server API."""
    
    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        self.session.timeout = config.timeout
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to MCE Server."""
        url = urljoin(self.config.server_url, endpoint)
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            
            # Handle empty response
            if not response.content:
                return {}
            
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            # Try to extract error message from response
            try:
                error_data = e.response.json()
                message = error_data.get('message', str(e))
                error = error_data.get('error', 'HTTP Error')
            except (ValueError, AttributeError):
                message = str(e)
                error = 'HTTP Error'
            
            raise MCEServerError(f"{error}: {message}", status_code=e.response.status_code)
            
        except requests.exceptions.RequestException as e:
            raise MCEClientError(f"Request failed: {str(e)}")
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make GET request."""
        return self._make_request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make POST request."""
        json_data = json.dumps(data) if data else None
        return self._make_request('POST', endpoint, data=json_data)
    
    def put(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make PUT request."""
        json_data = json.dumps(data) if data else None
        return self._make_request('PUT', endpoint, data=json_data)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request."""
        return self._make_request('DELETE', endpoint)
    
    # Health check
    def health_check(self) -> Dict[str, Any]:
        """Check server health."""
        return self.get('/health')
    
    # Project API methods
    def create_project(self, name: str, description: str = "", region: str = "default", 
                      tags: Optional[Dict[str, str]] = None, 
                      quota: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new project."""
        auth_info = self.config.auth_info
        data = {
            "name": name,
            "description": description,
            "region": region,
            "tags": tags or {},
            "quota": quota,
            **auth_info
        }
        return self.post('/api/v1/projects', data)
    
    def list_projects(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """List projects."""
        params = {"page": page, "pageSize": page_size}
        return self.get('/api/v1/projects', params)
    
    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project by ID."""
        return self.get(f'/api/v1/projects/{quote(project_id)}')
    
    def update_project(self, project_id: str, name: Optional[str] = None, 
                      description: Optional[str] = None, 
                      tags: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Update project."""
        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if tags is not None:
            data["tags"] = tags
        
        return self.put(f'/api/v1/projects/{quote(project_id)}', data)
    
    def delete_project(self, project_id: str) -> Dict[str, Any]:
        """Delete project."""
        return self.delete(f'/api/v1/projects/{quote(project_id)}')
    
    # Queue API methods
    def create_queue(self, project_id: str, name: str, weight: int = 1, 
                    flavor_name: str = "default") -> Dict[str, Any]:
        """Create a queue in project."""
        data = {
            "name": name,
            "weight": weight,
            "flavorName": flavor_name
        }
        return self.post(f'/api/v1/projects/{quote(project_id)}/queues', data)
    
    def list_queues(self, project_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """List queues in project."""
        params = {"page": page, "pageSize": page_size}
        return self.get(f'/api/v1/projects/{quote(project_id)}/queues', params)
    
    def get_queue(self, project_id: str, queue_id: str) -> Dict[str, Any]:
        """Get queue by ID."""
        return self.get(f'/api/v1/projects/{quote(project_id)}/queues/{quote(queue_id)}')
    
    def update_queue(self, project_id: str, queue_id: str, name: Optional[str] = None, 
                    weight: Optional[int] = None) -> Dict[str, Any]:
        """Update queue."""
        data = {}
        if name is not None:
            data["name"] = name
        if weight is not None:
            data["weight"] = weight
        
        return self.put(f'/api/v1/projects/{quote(project_id)}/queues/{quote(queue_id)}', data)
    
    def delete_queue(self, project_id: str, queue_id: str) -> Dict[str, Any]:
        """Delete queue."""
        return self.delete(f'/api/v1/projects/{quote(project_id)}/queues/{quote(queue_id)}')
    
    def get_queue_status(self, project_id: str, queue_id: str) -> Dict[str, Any]:
        """Get queue status."""
        return self.get(f'/api/v1/projects/{quote(project_id)}/queues/{quote(queue_id)}/status')
    
    # Compute Config API methods
    def create_compute_config(self, project_id: str, name: str, ray_version: str,
                            head_config: Dict[str, Any], 
                            worker_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create compute configuration."""
        data = {
            "name": name,
            "rayVersion": ray_version,
            "headConfig": head_config,
            "workerConfig": worker_config
        }
        return self.post(f'/api/v1/projects/{quote(project_id)}/compute-configs', data)
    
    def list_compute_configs(self, project_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """List compute configurations."""
        params = {"page": page, "pageSize": page_size}
        return self.get(f'/api/v1/projects/{quote(project_id)}/compute-configs', params)
    
    def get_compute_config(self, project_id: str, config_id: str) -> Dict[str, Any]:
        """Get compute configuration by ID."""
        return self.get(f'/api/v1/projects/{quote(project_id)}/compute-configs/{quote(config_id)}')
    
    def update_compute_config(self, project_id: str, config_id: str, 
                            name: Optional[str] = None,
                            ray_version: Optional[str] = None,
                            head_config: Optional[Dict[str, Any]] = None,
                            worker_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update compute configuration."""
        data = {}
        if name is not None:
            data["name"] = name
        if ray_version is not None:
            data["rayVersion"] = ray_version
        if head_config is not None:
            data["headConfig"] = head_config
        if worker_config is not None:
            data["workerConfig"] = worker_config
        
        return self.put(f'/api/v1/projects/{quote(project_id)}/compute-configs/{quote(config_id)}', data)
    
    def delete_compute_config(self, project_id: str, config_id: str) -> Dict[str, Any]:
        """Delete compute configuration."""
        return self.delete(f'/api/v1/projects/{quote(project_id)}/compute-configs/{quote(config_id)}')
    
    # Job API methods
    def create_job(self, project_id: str, name: str, entrypoint: str, image: str,
                  queue_id: Optional[str] = None, compute_config_id: Optional[str] = None,
                  ray_version: Optional[str] = None, pip_packages: Optional[List[str]] = None,
                  env_vars: Optional[Dict[str, str]] = None, working_dir: Optional[str] = None,
                  volume_mounts: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Create a job."""
        auth_info = self.config.auth_info
        data = {
            "type": "ray",
            "name": name,
            "entrypoint": entrypoint,
            "image": image,
            "projectId": project_id,
            **auth_info
        }
        
        if queue_id:
            data["queueId"] = queue_id
        if compute_config_id:
            data["computeConfigId"] = compute_config_id
        if ray_version:
            data["rayVersion"] = ray_version
        if pip_packages:
            data["pipPackages"] = pip_packages
        if env_vars:
            data["envVars"] = env_vars
        if working_dir:
            data["workingDir"] = working_dir
        if volume_mounts:
            data["volumeMounts"] = volume_mounts
        
        return self.post(f'/api/v1/projects/{quote(project_id)}/jobs', data)
    
    def list_jobs(self, project_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """List jobs in project."""
        params = {"page": page, "pageSize": page_size}
        return self.get(f'/api/v1/projects/{quote(project_id)}/jobs', params)
    
    def get_job(self, project_id: str, job_id: str) -> Dict[str, Any]:
        """Get job by ID."""
        return self.get(f'/api/v1/projects/{quote(project_id)}/jobs/{quote(job_id)}')
    
    def stop_job(self, project_id: str, job_id: str) -> Dict[str, Any]:
        """Stop a job."""
        return self.post(f'/api/v1/projects/{quote(project_id)}/jobs/{quote(job_id)}/stop')
    
    def retry_job(self, project_id: str, job_id: str) -> Dict[str, Any]:
        """Retry a job."""
        return self.post(f'/api/v1/projects/{quote(project_id)}/jobs/{quote(job_id)}/retry')
    
    def delete_job(self, project_id: str, job_id: str) -> Dict[str, Any]:
        """Delete a job."""
        return self.delete(f'/api/v1/projects/{quote(project_id)}/jobs/{quote(job_id)}')
    
    def get_job_events(self, project_id: str, job_id: str) -> Dict[str, Any]:
        """Get job events."""
        return self.get(f'/api/v1/projects/{quote(project_id)}/jobs/{quote(job_id)}/events')
    
    # Log API methods
    def get_job_logs(self, project_id: str, job_id: str, lines: Optional[int] = None,
                    since: Optional[str] = None) -> Dict[str, Any]:
        """Get job logs."""
        params = {}
        if lines is not None:
            params["lines"] = lines
        if since is not None:
            params["since"] = since
        
        return self.get(f'/api/v1/projects/{quote(project_id)}/jobs/{quote(job_id)}/logs', params)
    
    def get_log_file_info(self, project_id: str, job_id: str) -> Dict[str, Any]:
        """Get log file information."""
        return self.get(f'/api/v1/projects/{quote(project_id)}/jobs/{quote(job_id)}/logs/info')