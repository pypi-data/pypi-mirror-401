"""External API client for notifying about discovered APIs."""

import requests
from typing import Dict, Any, Optional, List
from datetime import datetime
from .apisec_config import APISecConfig
from .state_manager import DiscoveryStateManager


class APIClient:
    """Client for interacting with external API endpoints."""

    def __init__(
        self,
        endpoint: str,
        auth_token: Optional[str] = None,
        timeout: int = 30,
    ):
        """
        Initialize API client.

        Args:
            endpoint: External API endpoint URL.
            auth_token: Authentication token (optional).
            timeout: Request timeout in seconds.
        """
        self.endpoint = endpoint
        self.auth_token = auth_token
        self.timeout = timeout

    def send_openapi_spec(
        self,
        openapi_spec: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
        state_manager: Optional[DiscoveryStateManager] = None,
    ) -> bool:
        """
        Send or update OpenAPI specification to external API.

        Args:
            openapi_spec: OpenAPI specification as dictionary.
            metadata: Additional metadata to send (optional).
            state_manager: State manager instance for tracking application/instance IDs.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.endpoint:
            print("Warning: No external API endpoint configured. Skipping upload.")
            return False

        try:
            # Check if we have existing state (update mode)
            existing_app_id = None
            existing_instance_id = None
            if state_manager:
                existing_app_id = state_manager.get_application_id()
                existing_instance_id = state_manager.get_instance_id()

            if existing_app_id and existing_instance_id:
                # Update existing application instance
                print(f"Found existing application (ID: {existing_app_id}, Instance: {existing_instance_id})")
                print("Updating existing application with new OpenAPI spec...")
                return self._reload_spec(
                    openapi_spec,
                    existing_app_id,
                    existing_instance_id,
                    state_manager
                )
            else:
                # Create new application
                print("No existing application found. Creating new application...")
                return self._upload_openapi_file(openapi_spec, metadata, state_manager)

        except Exception as e:
            print(f"✗ Unexpected error sending to external API: {e}")
            return False
            return False

    def _upload_openapi_file(
        self,
        openapi_spec: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
        state_manager: Optional[DiscoveryStateManager] = None,
    ) -> bool:
        """
        Upload OpenAPI specification file to external API.

        Args:
            openapi_spec: OpenAPI specification as dictionary.
            metadata: Additional metadata to send (optional).

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            import tempfile
            import os
            from io import BytesIO

            # Get application name from spec title or metadata
            application_name = self._get_application_name(openapi_spec, metadata)
            
            # Create temporary file with OpenAPI spec
            spec_content = self._serialize_openapi_spec(openapi_spec)
            
            # Prepare multipart form data
            files = {
                'fileUpload': ('openapi-spec.yaml', BytesIO(spec_content.encode('utf-8')), 'application/x-yaml')
            }
            
            data = {
                'applicationName': application_name,
                'origin': 'CLI'
            }

            # Prepare headers (no Content-Type for multipart/form-data)
            headers = {}
            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"

            # Construct upload URL
            upload_url = f"{self.endpoint.rstrip('/')}/v1/applications/oas"

            # Send request
            print(f"Uploading OpenAPI specification to {upload_url}...")
            print(f"  Application: {application_name}")
            
            response = requests.post(
                upload_url,
                files=files,
                data=data,
                headers=headers,
                timeout=self.timeout,
            )

            # Check response
            response.raise_for_status()

            print(f"✓ Successfully uploaded OpenAPI specification")
            print(f"  Response: {response.status_code}")

            # Parse and log response
            if response.text:
                try:
                    response_data = response.json()
                    application_id = response_data.get('applicationId')
                    host_urls = response_data.get('hostUrls', [])
                    
                    print(f"  Application ID: {application_id}")
                    if host_urls:
                        print(f"  Host URLs: {', '.join(host_urls)}")
                    
                    # Make second API call to create instances
                    instance_id = None
                    if application_id and host_urls:
                        instance_id = self._create_application_instances(application_id, host_urls)
                        
                        # If instance ID not in response, try to get it by querying instances
                        if not instance_id and application_id:
                            instance_id = self._get_instance_id_from_app(application_id, host_urls[0] if host_urls else None)
                        
                        # Save state if state manager is provided
                        if state_manager and application_id and instance_id:
                            state_manager.save_state({
                                "applicationId": application_id,
                                "instanceId": instance_id,
                                "lastUpdatedAt": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                            })
                            print(f"✓ Saved state to {state_manager.state_file}")
                        elif state_manager and application_id and not instance_id:
                            print(f"  Warning: Could not get instance ID. State not saved.")
                            print(f"  Application ID: {application_id}")
                            print(f"  Note: State management requires instance ID for reload-spec endpoint")
                        
                        # Print application URL if both calls were successful
                        if instance_id:
                            application_url = f"https://<tenant-name>.apisecapps.com/application/{application_id}"
                            print(f"\n🎉 Application Created: {application_url}")
                    
                except Exception as e:
                    print(f"  Error parsing response: {e}")
                    print(f"  Response data: {response.text[:200]}")

                return True

        except requests.exceptions.Timeout:
            print(f"✗ Error: Request to {upload_url} timed out after {self.timeout}s")
            return False

        except requests.exceptions.ConnectionError:
            print(f"✗ Error: Could not connect to {upload_url}")
            return False

        except requests.exceptions.HTTPError as e:
            print(f"✗ HTTP Error: {e}")
            if hasattr(e.response, 'text'):
                print(f"  Response: {e.response.text[:200]}")
            return False

        except Exception as e:
            print(f"✗ Error uploading OpenAPI file: {e}")
            return False

    def _create_application_instances(
        self,
        application_id: str,
        host_urls: List[str],
    ) -> Optional[str]:
        """
        Create application instances using the application ID and host URLs.

        Args:
            application_id: The application ID from the previous API response.
            host_urls: List of host URLs from the previous API response.

        Returns:
            Instance ID if successful, None otherwise. Returns the first instance ID.
        """
        try:
            # Prepare headers
            headers = {
                "Content-Type": "application/json"
            }
            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"

            # Prepare payload
            payload = {
                "instanceRequestItems": [
                    {"hostUrl": host_url} for host_url in host_urls
                ]
            }

            # Construct instances URL
            instances_url = f"{self.endpoint.rstrip('/')}/v1/applications/{application_id}/instances/batch"

            # Send request
            print(f"Creating application instances...")
            print(f"  Instances URL: {instances_url}")
            print(f"  Host URLs: {', '.join(host_urls)}")
            
            response = requests.post(
                instances_url,
                json=payload,
                headers=headers,
                timeout=self.timeout,
            )

            # Check response
            response.raise_for_status()

            print(f"✓ Successfully created application instances")
            print(f"  Response: {response.status_code}")
            print(f"  Response headers: {dict(response.headers)}")

            # Parse and log response
            instance_id = None
            print(f"  Response text length: {len(response.text) if response.text else 0}")
            print(f"  Response text: {response.text[:500] if response.text else '(empty)'}")
            if response.text:
                try:
                    response_data = response.json()
                    print(f"  Instance creation response: {response_data}")
                    print(f"  Response type: {type(response_data)}")
                    
                    # Extract instance ID from response
                    # The response might contain instance IDs in different formats
                    # Try common patterns
                    if isinstance(response_data, list) and len(response_data) > 0:
                        # If response is a list, get first item
                        first_item = response_data[0]
                        print(f"  First item: {first_item}")
                        instance_id = first_item.get('instanceId') or first_item.get('id')
                    elif isinstance(response_data, dict):
                        # If response is a dict, look for instanceId or instances array
                        instance_id = response_data.get('instanceId')
                        if not instance_id and 'instances' in response_data:
                            instances = response_data['instances']
                            if isinstance(instances, list) and len(instances) > 0:
                                instance_id = instances[0].get('instanceId') or instances[0].get('id')
                        # Also check for 'id' field directly
                        if not instance_id:
                            instance_id = response_data.get('id')
                    
                    if instance_id:
                        print(f"  Instance ID: {instance_id}")
                    else:
                        print(f"  Warning: Could not extract instance ID from response")
                        print(f"  Response structure: {response_data}")
                        print(f"  Response keys: {list(response_data.keys()) if isinstance(response_data, dict) else 'N/A (not a dict)'}")
                        
                except Exception as e:
                    print(f"  Error parsing instance response: {e}")
                    print(f"  Response data: {response.text[:500]}")
            else:
                print(f"  Warning: Empty response from instance creation endpoint")

            return instance_id

        except requests.exceptions.Timeout:
            print(f"✗ Error: Request to {instances_url} timed out after {self.timeout}s")
            return None

        except requests.exceptions.ConnectionError:
            print(f"✗ Error: Could not connect to {instances_url}")
            return None

        except requests.exceptions.HTTPError as e:
            print(f"✗ HTTP Error: {e}")
            if hasattr(e.response, 'text'):
                print(f"  Response: {e.response.text[:200]}")
            return None

        except Exception as e:
            print(f"✗ Error creating application instances: {e}")
            return None

    def _get_application_name(
        self,
        openapi_spec: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Get application name from OpenAPI spec or metadata.

        Args:
            openapi_spec: OpenAPI specification as dictionary.
            metadata: Additional metadata to send (optional).

        Returns:
            str: Application name.
        """
        # Try to get from OpenAPI spec title first
        if 'info' in openapi_spec and 'title' in openapi_spec['info']:
            return openapi_spec['info']['title']
        
        # Try to get from metadata
        if metadata and 'repository_path' in metadata:
            import os
            return os.path.basename(metadata['repository_path'])
        
        # Default fallback
        return "discovered-api"

    def _reload_spec(
        self,
        openapi_spec: Dict[str, Any],
        application_id: str,
        instance_id: str,
        state_manager: Optional[DiscoveryStateManager] = None,
    ) -> bool:
        """
        Reload OpenAPI specification for an existing application instance.

        Args:
            openapi_spec: OpenAPI specification as dictionary.
            application_id: Existing application ID.
            instance_id: Existing instance ID.
            state_manager: State manager instance for updating timestamp.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            from io import BytesIO

            # Serialize OpenAPI spec to YAML
            spec_content = self._serialize_openapi_spec(openapi_spec)

            # Prepare multipart form data
            files = {
                'fileUpload': ('openapi-spec.yaml', BytesIO(spec_content.encode('utf-8')), 'application/x-yaml')
            }

            data = {
                'overwriteVal': 'false',
                'overwriteEndpointConfig': 'false',
                'deleteEndpoints': 'true'
            }

            # Prepare headers
            headers = {}
            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"

            # Construct reload URL
            reload_url = f"{self.endpoint.rstrip('/')}/v1/applications/{application_id}/instances/{instance_id}/reload-spec"

            # Send request
            print(f"Reloading OpenAPI specification...")
            print(f"  Application ID: {application_id}")
            print(f"  Instance ID: {instance_id}")
            print(f"  URL: {reload_url}")

            response = requests.post(
                reload_url,
                files=files,
                data=data,
                headers=headers,
                timeout=self.timeout,
            )

            # Check response
            response.raise_for_status()

            print(f"✓ Successfully reloaded OpenAPI specification")
            print(f"  Response: {response.status_code}")

            # Update state timestamp
            if state_manager:
                state_manager.update_timestamp()
                print(f"✓ Updated state timestamp")

            return True

        except requests.exceptions.Timeout:
            print(f"✗ Error: Request to {reload_url} timed out after {self.timeout}s")
            return False

        except requests.exceptions.ConnectionError:
            print(f"✗ Error: Could not connect to {reload_url}")
            return False

        except requests.exceptions.HTTPError as e:
            print(f"✗ HTTP Error: {e}")
            if hasattr(e.response, 'text'):
                print(f"  Response: {e.response.text[:200]}")
            return False

        except Exception as e:
            print(f"✗ Error reloading OpenAPI spec: {e}")
            return False

    def _get_instance_id_from_app(
        self,
        application_id: str,
        host_url: Optional[str] = None,
    ) -> Optional[str]:
        """
        Get instance ID by querying the application endpoint.
        
        The GET /v1/applications/{applicationId} endpoint returns application details
        including an instances array with instance IDs.
        
        Args:
            application_id: Application ID.
            host_url: Host URL to match (optional).
            
        Returns:
            Instance ID if found, None otherwise.
        """
        try:
            # Prepare headers
            headers = {
                "Content-Type": "application/json"
            }
            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"

            # Query application endpoint (returns application with instances array)
            app_url = f"{self.endpoint.rstrip('/')}/v1/applications/{application_id}"
            
            print(f"  Querying application {application_id} for instance ID...")
            response = requests.get(
                app_url,
                headers=headers,
                timeout=self.timeout,
            )

            response.raise_for_status()
            
            if response.text:
                app_data = response.json()
                print(f"  Application response: {app_data.get('applicationId')}, instances: {len(app_data.get('instances', []))}")
                
                # Extract instance ID from instances array
                instances = app_data.get('instances', [])
                
                if isinstance(instances, list) and len(instances) > 0:
                    # If host_url provided, try to match
                    if host_url:
                        for instance in instances:
                            if instance.get('hostUrl') == host_url:
                                instance_id = instance.get('instanceId')
                                if instance_id:
                                    print(f"  Found instance ID: {instance_id} (matched hostUrl: {host_url})")
                                    return instance_id
                    
                    # Otherwise, get first instance
                    first_instance = instances[0]
                    instance_id = first_instance.get('instanceId')
                    if instance_id:
                        print(f"  Found instance ID: {instance_id} (first instance)")
                        return instance_id
            
            print(f"  Warning: Could not find instance ID in application response")
            return None

        except Exception as e:
            print(f"  Error querying application: {e}")
            return None

    def _serialize_openapi_spec(self, openapi_spec: Dict[str, Any]) -> str:
        """
        Serialize OpenAPI spec to YAML string.

        Args:
            openapi_spec: OpenAPI specification as dictionary.

        Returns:
            str: YAML string representation of the spec.
        """
        import yaml
        return yaml.dump(openapi_spec, sort_keys=False, default_flow_style=False)

    def send_discovery_event(
        self,
        event_type: str,
        data: Dict[str, Any],
    ) -> bool:
        """
        Send a discovery event to external API.

        Args:
            event_type: Type of event (e.g., "api_discovered", "api_updated").
            data: Event data.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.endpoint:
            print("Warning: No external API endpoint configured. Skipping event.")
            return False

        try:
            payload = {
                "event_type": event_type,
                "data": data,
            }

            headers = {
                "Content-Type": "application/json",
            }

            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"

            response = requests.post(
                self.endpoint,
                json=payload,
                headers=headers,
                timeout=self.timeout,
            )

            response.raise_for_status()
            print(f"✓ Successfully sent {event_type} event to external API")
            return True

        except Exception as e:
            print(f"✗ Error sending event to external API: {e}")
            return False

    def health_check(self) -> bool:
        """
        Check if the external API is reachable.

        Returns:
            bool: True if API is healthy, False otherwise.
        """
        if not self.endpoint:
            return False

        try:
            # Try to send a HEAD or GET request to the endpoint
            response = requests.head(self.endpoint, timeout=5)
            return response.status_code < 500
        except:
            return False

    @classmethod
    def from_apisec_config(cls, service: str = "api-discovery", apisec_config: Optional[APISecConfig] = None) -> Optional['APIClient']:
        """
        Create APIClient instance from .apisec configuration.

        Args:
            service: Service name from .apisec file (default: 'api-discovery').
            apisec_config: APISecConfig instance (optional, will create new if not provided).

        Returns:
            APIClient instance or None if service not configured.
        """
        if apisec_config is None:
            apisec_config = APISecConfig()

        if not apisec_config.has_service(service):
            print(f"Warning: Service '{service}' not found in .apisec configuration")
            return None

        endpoint = apisec_config.get_endpoint(service)
        token = apisec_config.get_token(service)

        if not endpoint:
            print(f"Warning: No endpoint configured for service '{service}'")
            return None

        return cls(endpoint=endpoint, auth_token=token)

    @classmethod
    def create_for_all_services(cls, apisec_config: Optional[APISecConfig] = None) -> List['APIClient']:
        """
        Create APIClient instances for all services in .apisec configuration.

        Args:
            apisec_config: APISecConfig instance (optional, will create new if not provided).

        Returns:
            List of APIClient instances for configured services.
        """
        if apisec_config is None:
            apisec_config = APISecConfig()

        clients = []
        for service in apisec_config.list_services():
            client = cls.from_apisec_config(service, apisec_config)
            if client:
                clients.append(client)

        return clients

