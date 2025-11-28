"""
ML Analyzer Service
===================
Analyzes URL metrics using Linear Regression and PCA for health scoring.
"""

import numpy as np
from typing import Dict, List, Tuple
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLHealthAnalyzer:
    """ML-based URL health analysis using Linear Regression and PCA."""
    
    def __init__(self):
        """Initialize the analyzer with trained models."""
        self.lr_weights = self._initialize_lr_weights()
        self.pca_components = self._initialize_pca_components()
        self.feature_importance = self._calculate_feature_importance()
        
    def _initialize_lr_weights(self) -> np.ndarray:
        """
        Initialize Linear Regression weights.
        In production, these would be loaded from trained model.
        """
        # Simulated weights - in production load from trained model
        # Weights favor: fast load time, SSL, mobile-friendly, good SEO
        weights = np.array([
            0.5,   # status_code (200 = good)
            -2.0,  # load_time (lower is better)
            -0.1,  # response_size (lower is better)
            -0.5,  # redirects (fewer is better)
            1.5,   # compression_enabled
            1.0,   # has_cache_headers
            2.0,   # ssl_enabled
            0.01,  # ssl_days_until_expiry
            1.5,   # ssl_valid
            -0.05, # images_count (too many is bad)
            -0.05, # scripts_count
            -0.05, # stylesheets_count
            0.01,  # links_count
            0.1,   # forms_count
            -0.3,  # iframes_count (usually bad)
            -0.2,  # external_scripts_count
            1.0,   # has_meta_description
            1.5,   # has_viewport_meta
            1.5,   # mobile_friendly
            1.0,   # has_title
            0.01,  # title_length
            0.8,   # has_schema_org
            0.8,   # has_open_graph
            0.0001, # text_content_length
            0.5,   # html_to_text_ratio
            1.2,   # has_content_security_policy
            1.0,   # has_x_frame_options
            1.2,   # has_strict_transport_security
            0.5,   # dns_resolved
            -1.0,  # dns_resolution_time
            # Padding weights
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        ])
        
        return weights[:41]
    
    def _initialize_pca_components(self) -> np.ndarray:
        """Initialize PCA components for anomaly detection."""
        # First 3 principal components (simulated)
        # In production, load from trained PCA model
        np.random.seed(42)
        return np.random.randn(3, 41) * 0.1
    
    def _calculate_feature_importance(self) -> Dict[str, float]:
        """Calculate and return feature importance scores."""
        feature_names = [
            'status_code', 'load_time', 'response_size', 'redirects',
            'compression', 'caching', 'ssl_enabled', 'ssl_expiry',
            'ssl_valid', 'images', 'scripts', 'stylesheets', 'links',
            'forms', 'iframes', 'external_scripts', 'meta_description',
            'viewport', 'mobile_friendly', 'has_title', 'title_length',
            'schema_org', 'open_graph', 'text_length', 'html_text_ratio',
            'csp', 'x_frame', 'hsts', 'dns_resolved', 'dns_time'
        ]
        
        importance = {}
        abs_weights = np.abs(self.lr_weights[:30])  # First 30 actual features
        normalized = abs_weights / abs_weights.sum()
        
        for name, score in zip(feature_names, normalized):
            importance[name] = float(score)
        
        return importance
    
    def analyze(self, features: List[float]) -> Dict:
        """
        Perform complete ML analysis on URL features.
        
        Args:
            features: List of 41 numerical features
            
        Returns:
            Dictionary with health score, predictions, and recommendations
        """
        logger.info("Starting ML analysis...")
        
        features_array = np.array(features).reshape(1, -1)
        
        # Calculate health score using Linear Regression
        health_score = self._calculate_health_score(features_array)
        
        # Detect anomalies using PCA
        anomalies = self._detect_anomalies(features_array)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(features, health_score)
        
        # Calculate grade
        grade = self._calculate_grade(health_score)
        
        result = {
            'health_score': round(health_score, 2),
            'grade': grade,
            'anomalies': anomalies,
            'recommendations': recommendations,
            'feature_analysis': self._analyze_features(features),
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Analysis complete. Health score: {health_score:.2f}")
        return result
    
    def _calculate_health_score(self, features: np.ndarray) -> float:
        """Calculate health score using Linear Regression."""
        raw_score = np.dot(features, self.lr_weights)[0]
        
        # Normalize to 0-100 scale
        # Add bias and apply sigmoid-like transformation
        normalized = 50 + (raw_score * 2)
        
        # Clamp to 0-100
        health_score = max(0, min(100, normalized))
        
        return health_score
    
    def _detect_anomalies(self, features: np.ndarray) -> List[str]:
        """Detect anomalies using PCA reconstruction error."""
        anomalies = []
        
        # Project to PCA space and reconstruct
        projected = np.dot(features, self.pca_components.T)
        reconstructed = np.dot(projected, self.pca_components)
        
        # Calculate reconstruction error
        error = np.mean((features - reconstructed) ** 2)
        
        # Check specific feature anomalies
        features_flat = features.flatten()
        
        if features_flat[1] > 5.0:  # load_time > 5s
            anomalies.append("⚠️ Extremely slow load time detected")
        
        if features_flat[2] > 5000:  # response_size > 5MB
            anomalies.append("⚠️ Very large page size detected")
        
        if features_flat[6] == 0:  # no SSL
            anomalies.append("🔒 Missing SSL certificate")
        
        if features_flat[7] < 30 and features_flat[7] > 0:  # SSL expiring soon
            anomalies.append("⏰ SSL certificate expiring soon")
        
        if features_flat[14] > 5:  # many iframes
            anomalies.append("⚠️ Excessive iframe usage detected")
        
        if error > 10:
            anomalies.append("⚠️ Unusual metric pattern detected (high reconstruction error)")
        
        return anomalies if anomalies else ["✅ No anomalies detected"]
    
    def _generate_recommendations(self, features: List[float], score: float) -> List[Dict]:
        """Generate actionable recommendations based on features."""
        recommendations = []
        
        # Performance recommendations
        if features[1] > 3.0:  # load_time
            recommendations.append({
                'category': 'Performance',
                'priority': 'high',
                'issue': 'Slow page load time',
                'current': f'{features[1]:.2f}s',
                'target': '< 2.0s',
                'action': 'Optimize images, minify CSS/JS, enable caching'
            })
        
        if features[2] > 1000:  # response_size_kb
            recommendations.append({
                'category': 'Performance',
                'priority': 'medium',
                'issue': 'Large page size',
                'current': f'{features[2]:.0f}KB',
                'target': '< 500KB',
                'action': 'Compress images, remove unused code, lazy load resources'
            })
        
        # Security recommendations
        if features[6] == 0:  # ssl_enabled
            recommendations.append({
                'category': 'Security',
                'priority': 'critical',
                'issue': 'No SSL/HTTPS',
                'current': 'HTTP only',
                'target': 'HTTPS enabled',
                'action': 'Install SSL certificate (Let\'s Encrypt is free)'
            })
        
        if features[25] == 0:  # has_content_security_policy
            recommendations.append({
                'category': 'Security',
                'priority': 'medium',
                'issue': 'Missing Content-Security-Policy header',
                'current': 'Not present',
                'target': 'CSP header configured',
                'action': 'Add CSP header to prevent XSS attacks'
            })
        
        # SEO recommendations
        if features[16] == 0:  # has_meta_description
            recommendations.append({
                'category': 'SEO',
                'priority': 'high',
                'issue': 'Missing meta description',
                'current': 'Not present',
                'target': 'Meta description added',
                'action': 'Add <meta name="description"> tag (150-160 chars)'
            })
        
        if features[18] == 0:  # mobile_friendly
            recommendations.append({
                'category': 'Mobile',
                'priority': 'high',
                'issue': 'Not mobile-friendly',
                'current': 'No viewport meta tag',
                'target': 'Mobile responsive',
                'action': 'Add viewport meta tag and responsive CSS'
            })
        
        if features[21] == 0:  # has_schema_org
            recommendations.append({
                'category': 'SEO',
                'priority': 'low',
                'issue': 'No structured data',
                'current': 'No Schema.org markup',
                'target': 'Structured data added',
                'action': 'Add Schema.org microdata for better search results'
            })
        
        # Caching recommendations
        if features[5] == 0:  # has_cache_headers
            recommendations.append({
                'category': 'Performance',
                'priority': 'medium',
                'issue': 'No cache headers',
                'current': 'No caching configured',
                'target': 'Cache headers set',
                'action': 'Add Cache-Control headers for static resources'
            })
        
        # Sort by priority
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        recommendations.sort(key=lambda x: priority_order[x['priority']])
        
        return recommendations
    
    def _analyze_features(self, features: List[float]) -> Dict:
        """Provide detailed analysis of key features."""
        return {
            'performance': {
                'load_time': {'value': features[1], 'unit': 'seconds', 'status': 'good' if features[1] < 2 else 'needs_improvement'},
                'page_size': {'value': features[2], 'unit': 'KB', 'status': 'good' if features[2] < 500 else 'needs_improvement'},
                'compression': {'enabled': bool(features[4]), 'status': 'good' if features[4] else 'warning'}
            },
            'security': {
                'ssl': {'enabled': bool(features[6]), 'status': 'good' if features[6] else 'critical'},
                'ssl_valid': {'valid': bool(features[8]), 'days_remaining': int(features[7])},
                'security_headers': {
                    'csp': bool(features[25]),
                    'x_frame_options': bool(features[26]),
                    'hsts': bool(features[27])
                }
            },
            'seo': {
                'meta_description': bool(features[16]),
                'mobile_friendly': bool(features[18]),
                'has_title': bool(features[19]),
                'structured_data': bool(features[21])
            },
            'content': {
                'images': int(features[9]),
                'scripts': int(features[10]),
                'links': int(features[12]),
                'text_length': int(features[23])
            }
        }
    
    def _calculate_grade(self, score: float) -> str:
        """Convert numerical score to letter grade."""
        if score >= 90:
            return 'A+'
        elif score >= 85:
            return 'A'
        elif score >= 80:
            return 'A-'
        elif score >= 75:
            return 'B+'
        elif score >= 70:
            return 'B'
        elif score >= 65:
            return 'B-'
        elif score >= 60:
            return 'C+'
        elif score >= 55:
            return 'C'
        elif score >= 50:
            return 'C-'
        elif score >= 45:
            return 'D'
        else:
            return 'F'


if __name__ == "__main__":
    # Test the analyzer
    analyzer = URLHealthAnalyzer()
    
    # Simulated features for a good website
    test_features = [
        200,  # status_code
        1.5,  # load_time
        350,  # response_size_kb
        0,    # redirects
        1,    # compression
        1,    # caching
        1,    # ssl_enabled
        90,   # ssl_days_until_expiry
        1,    # ssl_valid
        20,   # images
        5,    # scripts
        3,    # stylesheets
        50,   # links
        2,    # forms
        0,    # iframes
        2,    # external_scripts
        1,    # meta_description
        1,    # viewport
        1,    # mobile_friendly
        1,    # has_title
        45,   # title_length
        1,    # schema_org
        1,    # open_graph
        5000, # text_length
        0.25, # html_text_ratio
        1,    # csp
        1,    # x_frame
        1,    # hsts
        1,    # dns_resolved
        0.05, # dns_time
        # Padding
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ]
    
    result = analyzer.analyze(test_features)
    
    import json
    print(json.dumps(result, indent=2))
