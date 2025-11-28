"""
URL Scraper Service
===================
Extracts comprehensive metrics from URLs for ML analysis.
"""

import time
import ssl
import socket
import requests
from urllib.parse import urlparse
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLScraper:
    """Comprehensive URL analysis and metrics extraction."""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TransparentML-URLDiagnostics/1.0'
        })
    
    def analyze_url(self, url: str) -> Dict:
        """
        Perform comprehensive analysis of a URL.
        
        Args:
            url: Target URL to analyze
            
        Returns:
            Dictionary with all extracted metrics
        """
        logger.info(f"Starting analysis for: {url}")
        
        # Validate and normalize URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        metrics = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'error': None
        }
        
        try:
            # Basic HTTP metrics
            http_metrics = self._get_http_metrics(url)
            metrics.update(http_metrics)
            
            # SSL/TLS metrics
            if url.startswith('https://'):
                ssl_metrics = self._get_ssl_metrics(url)
                metrics.update(ssl_metrics)
            
            # Content metrics
            if metrics.get('status_code') == 200:
                content_metrics = self._get_content_metrics(
                    metrics.get('response_text', ''),
                    metrics.get('response_headers', {})
                )
                metrics.update(content_metrics)
            
            # DNS metrics
            dns_metrics = self._get_dns_metrics(url)
            metrics.update(dns_metrics)
            
            metrics['success'] = True
            logger.info(f"Analysis completed successfully for: {url}")
            
        except Exception as e:
            logger.error(f"Error analyzing {url}: {str(e)}")
            metrics['error'] = str(e)
        
        return metrics
    
    def _get_http_metrics(self, url: str) -> Dict:
        """Extract HTTP-related metrics."""
        logger.info("Extracting HTTP metrics...")
        
        start_time = time.time()
        response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
        load_time = time.time() - start_time
        
        metrics = {
            'status_code': response.status_code,
            'load_time_seconds': round(load_time, 3),
            'response_size_bytes': len(response.content),
            'response_size_kb': round(len(response.content) / 1024, 2),
            'redirects_count': len(response.history),
            'final_url': response.url,
            'response_headers': dict(response.headers),
            'response_text': response.text,
            'encoding': response.encoding or 'unknown'
        }
        
        # Check for compression
        metrics['compression_enabled'] = 'gzip' in response.headers.get('Content-Encoding', '').lower()
        
        # Check for caching headers
        metrics['cache_control'] = response.headers.get('Cache-Control', 'none')
        metrics['has_cache_headers'] = bool(
            response.headers.get('Cache-Control') or 
            response.headers.get('ETag') or 
            response.headers.get('Last-Modified')
        )
        
        return metrics
    
    def _get_ssl_metrics(self, url: str) -> Dict:
        """Extract SSL/TLS certificate metrics."""
        logger.info("Extracting SSL metrics...")
        
        parsed = urlparse(url)
        hostname = parsed.netloc
        port = parsed.port or 443
        
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Parse expiration date
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_expiry = (not_after - datetime.now()).days
                    
                    return {
                        'ssl_enabled': True,
                        'ssl_version': ssock.version(),
                        'ssl_cipher': ssock.cipher()[0],
                        'ssl_days_until_expiry': days_until_expiry,
                        'ssl_issuer': dict(x[0] for x in cert['issuer']),
                        'ssl_subject': dict(x[0] for x in cert['subject']),
                        'ssl_valid': days_until_expiry > 0
                    }
        except Exception as e:
            logger.warning(f"SSL analysis failed: {str(e)}")
            return {
                'ssl_enabled': False,
                'ssl_error': str(e)
            }
    
    def _get_content_metrics(self, html_content: str, headers: Dict) -> Dict:
        """Extract content-related metrics from HTML."""
        logger.info("Extracting content metrics...")
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Count various elements
        metrics = {
            'images_count': len(soup.find_all('img')),
            'scripts_count': len(soup.find_all('script')),
            'stylesheets_count': len(soup.find_all('link', rel='stylesheet')),
            'links_count': len(soup.find_all('a')),
            'forms_count': len(soup.find_all('form')),
            'iframes_count': len(soup.find_all('iframe'))
        }
        
        # External resources
        external_scripts = [s for s in soup.find_all('script', src=True) 
                          if s.get('src', '').startswith(('http://', 'https://', '//'))]
        metrics['external_scripts_count'] = len(external_scripts)
        
        # Meta tags
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_viewport = soup.find('meta', attrs={'name': 'viewport'})
        
        metrics['has_meta_description'] = meta_description is not None
        metrics['has_viewport_meta'] = meta_viewport is not None
        metrics['mobile_friendly'] = meta_viewport is not None
        
        # Title
        title_tag = soup.find('title')
        metrics['has_title'] = title_tag is not None
        metrics['title_length'] = len(title_tag.text) if title_tag else 0
        
        # Structured data
        metrics['has_schema_org'] = bool(soup.find_all(attrs={'itemtype': True}))
        metrics['has_open_graph'] = bool(soup.find_all('meta', property=lambda x: x and x.startswith('og:')))
        
        # Content size
        text_content = soup.get_text()
        metrics['text_content_length'] = len(text_content)
        metrics['html_to_text_ratio'] = round(len(text_content) / len(html_content), 3) if html_content else 0
        
        # Security headers
        metrics['has_content_security_policy'] = 'Content-Security-Policy' in headers
        metrics['has_x_frame_options'] = 'X-Frame-Options' in headers
        metrics['has_strict_transport_security'] = 'Strict-Transport-Security' in headers
        
        return metrics
    
    def _get_dns_metrics(self, url: str) -> Dict:
        """Extract DNS-related metrics."""
        logger.info("Extracting DNS metrics...")
        
        parsed = urlparse(url)
        hostname = parsed.netloc
        
        try:
            start_time = time.time()
            ip_address = socket.gethostbyname(hostname)
            dns_resolution_time = time.time() - start_time
            
            return {
                'dns_resolved': True,
                'ip_address': ip_address,
                'dns_resolution_time_seconds': round(dns_resolution_time, 3)
            }
        except Exception as e:
            logger.warning(f"DNS resolution failed: {str(e)}")
            return {
                'dns_resolved': False,
                'dns_error': str(e)
            }
    
    def extract_features_for_ml(self, metrics: Dict) -> List[float]:
        """
        Convert metrics to feature vector for ML models.
        
        Returns 41 features to match linear regression model.
        """
        features = [
            float(metrics.get('status_code', 0)),
            float(metrics.get('load_time_seconds', 0)),
            float(metrics.get('response_size_kb', 0)),
            float(metrics.get('redirects_count', 0)),
            float(metrics.get('compression_enabled', 0)),
            float(metrics.get('has_cache_headers', 0)),
            float(metrics.get('ssl_enabled', 0)),
            float(metrics.get('ssl_days_until_expiry', 0)),
            float(metrics.get('ssl_valid', 0)),
            float(metrics.get('images_count', 0)),
            float(metrics.get('scripts_count', 0)),
            float(metrics.get('stylesheets_count', 0)),
            float(metrics.get('links_count', 0)),
            float(metrics.get('forms_count', 0)),
            float(metrics.get('iframes_count', 0)),
            float(metrics.get('external_scripts_count', 0)),
            float(metrics.get('has_meta_description', 0)),
            float(metrics.get('has_viewport_meta', 0)),
            float(metrics.get('mobile_friendly', 0)),
            float(metrics.get('has_title', 0)),
            float(metrics.get('title_length', 0)),
            float(metrics.get('has_schema_org', 0)),
            float(metrics.get('has_open_graph', 0)),
            float(metrics.get('text_content_length', 0)),
            float(metrics.get('html_to_text_ratio', 0)),
            float(metrics.get('has_content_security_policy', 0)),
            float(metrics.get('has_x_frame_options', 0)),
            float(metrics.get('has_strict_transport_security', 0)),
            float(metrics.get('dns_resolved', 0)),
            float(metrics.get('dns_resolution_time_seconds', 0)),
            # Padding to reach 41 features
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        ]
        
        return features[:41]  # Ensure exactly 41 features


if __name__ == "__main__":
    # Test the scraper
    scraper = URLScraper()
    test_url = "https://www.google.com"
    
    print(f"Testing URL: {test_url}\n")
    results = scraper.analyze_url(test_url)
    
    print(json.dumps(results, indent=2, default=str))
    
    print("\n\nFeature vector for ML:")
    features = scraper.extract_features_for_ml(results)
    print(f"Features (length={len(features)}): {features}")
