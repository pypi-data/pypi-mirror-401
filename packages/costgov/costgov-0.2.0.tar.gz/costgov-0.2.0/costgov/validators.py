"""Input validation and sanitization utilities for CostGov SDK"""

import re
import json
from typing import Optional, Dict, Any
from urllib.parse import urlparse
import ipaddress


def validate_api_url(url: str, is_production: Optional[bool] = None) -> str:
    """
    Validates and sanitizes API URL to prevent SSRF attacks
    
    Args:
        url: The API URL to validate
        is_production: Whether running in production (defaults to checking env)
    
    Returns:
        Validated URL string
        
    Raises:
        ValueError: If URL is invalid or potentially malicious
    """
    import os
    
    if is_production is None:
        is_production = os.getenv('NODE_ENV') == 'production'
    
    try:
        parsed = urlparse(url)
        
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("URL must include scheme and hostname")
        
        # Only allow HTTPS in production
        if is_production and parsed.scheme != 'https':
            raise ValueError("Only HTTPS is allowed in production environments")
        
        # Whitelist allowed hosts in production
        if is_production:
            allowed_hosts = ['costgov.com', 'api.costgov.com', 'ingest.costgov.com']
            hostname = parsed.hostname or ''
            is_allowed = any(hostname == h or hostname.endswith('.' + h) for h in allowed_hosts)
            
            if not is_allowed:
                raise ValueError("API URL must be a costgov.com domain in production")
        else:
            # In development, still block obvious SSRF targets
            if is_private_ip(parsed.hostname or ''):
                # Allow localhost/127.0.0.1 in development only
                is_localhost = parsed.hostname in ['localhost', '127.0.0.1', '::1']
                if not is_localhost:
                    raise ValueError("Private IP addresses are not allowed")
        
        return url
    except Exception as e:
        raise ValueError(f"Invalid API URL: {str(e)}")


def is_private_ip(hostname: str) -> bool:
    """
    Checks if a hostname is a private IP address
    Blocks RFC1918, loopback (except localhost in dev), link-local, cloud metadata
    """
    # Cloud metadata endpoints
    if hostname in ['169.254.169.254', 'metadata.google.internal']:
        return True
    
    # Localhost
    if hostname in ['localhost', '127.0.0.1', '::1'] or hostname.startswith('127.'):
        return True
    
    # Try to parse as IP address
    try:
        ip = ipaddress.ip_address(hostname)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not an IP address, check IPv4 patterns
        ipv4_private_patterns = [
            r'^10\.',
            r'^172\.(1[6-9]|2[0-9]|3[0-1])\.',
            r'^192\.168\.',
            r'^169\.254\.',
        ]
        
        for pattern in ipv4_private_patterns:
            if re.match(pattern, hostname):
                return True
    
    return False


def validate_metric_name(metric: str) -> None:
    """
    Validates metric name to prevent injection and DoS
    
    Args:
        metric: The metric name to validate
        
    Raises:
        ValueError: If metric name is invalid
    """
    if not metric or not isinstance(metric, str):
        raise ValueError("Metric name must be a non-empty string")
    
    if len(metric) > 256:
        raise ValueError("Metric name must not exceed 256 characters")
    
    # Only allow safe characters: alphanumeric, dots, hyphens, underscores
    if not re.match(r'^[a-zA-Z0-9._\-]+$', metric):
        raise ValueError(
            "Metric name contains invalid characters. "
            "Only alphanumeric, dots (.), hyphens (-), and underscores (_) are allowed"
        )


def validate_units(units: float) -> None:
    """
    Validates units value to prevent resource exhaustion
    
    Args:
        units: The units value to validate
        
    Raises:
        ValueError: If units value is invalid
    """
    if not isinstance(units, (int, float)):
        raise ValueError("Units must be a number")
    
    if not (units > 0 and units != float('inf') and units == units):  # Check for positive, not inf, not nan
        raise ValueError("Units must be a positive finite number")
    
    # Prevent extremely large values that could cause issues
    if units > 1e12:
        raise ValueError("Units must not exceed 1 trillion")


def validate_metadata(metadata: Optional[Dict[str, Any]]) -> None:
    """
    Validates metadata to prevent JSON bombs and DoS
    
    Args:
        metadata: The metadata dictionary to validate
        
    Raises:
        ValueError: If metadata is invalid or too large
    """
    if metadata is None:
        return
    
    if not isinstance(metadata, dict):
        raise ValueError("Metadata must be a dictionary")
    
    # Serialize to check size
    try:
        serialized = json.dumps(metadata)
        if len(serialized) > 10000:  # 10KB limit
            raise ValueError("Metadata exceeds maximum size of 10KB")
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid metadata: {str(e)}")


def sanitize_error(error: Any) -> str:
    """
    Sanitizes error messages to prevent API key leakage
    
    Args:
        error: The error object or string to sanitize
        
    Returns:
        Sanitized error message safe for logging
    """
    error_str = str(error)
    
    # Redact API keys (common patterns)
    error_str = re.sub(r'cg_[a-z]+_[a-zA-Z0-9]+', 'cg_***_REDACTED', error_str)
    error_str = re.sub(r'sk_[a-z]+_[a-zA-Z0-9]+', 'sk_***_REDACTED', error_str)
    error_str = re.sub(r'Bearer [a-zA-Z0-9\-_]+', 'Bearer ***_REDACTED', error_str)
    error_str = re.sub(r'api[_-]?key["\s:=]+[a-zA-Z0-9\-_]+', 'api_key=***_REDACTED', error_str, flags=re.IGNORECASE)
    error_str = re.sub(r'authorization["\s:=]+[a-zA-Z0-9\-_\s]+', 'authorization=***_REDACTED', error_str, flags=re.IGNORECASE)
    
    return error_str
