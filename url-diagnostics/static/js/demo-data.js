// ============================================================================
// TransparentML Demo Data - Pre-loaded samples for professional UI
// ============================================================================

const DEMO_DATA = {
    // Sample KPIs for system header
    systemKPIs: {
        uptime: '99.2%',
        totalRuns: 1247,
        avgAccuracy: '94.3%',
        activeModels: 4,
        lastUpdate: new Date().toLocaleTimeString()
    },
    
    // Sample URL Diagnostics Result
    urlDiagnostics: {
        url: 'https://example.com',
        health_score: 87.5,
        grade: 'A',
        metrics: {
            load_time: 1.23,
            status_code: 200,
            ssl_enabled: true,
            response_size_kb: 245.7,
            ttfb: 0.45
        },
        recommendations: [
            {
                category: 'Performance',
                priority: 'MEDIUM',
                issue: 'Page load time could be optimized',
                action: 'Consider implementing caching strategies'
            },
            {
                category: 'Security',
                priority: 'LOW',
                issue: 'Security headers are properly configured',
                action: 'No action needed'
            }
        ]
    },
    
    // Sample Linear Regression Result
    linearRegression: {
        algorithm: 'Linear Regression',
        metrics: {
            r2_score: 0.9234,
            mse: 12.45,
            mae: 3.21,
            n_samples: 1000,
            n_features: 41
        },
        coefficients: [0.45, -0.23, 0.67, 0.12],
        intercept: 5.23
    },
    
    // Sample PCA Result
    pca: {
        algorithm: 'PCA',
        metrics: {
            n_components: 2,
            explained_variance_ratio: [0.729, 0.228],
            total_variance: 0.957,
            n_samples: 150,
            n_features: 4
        }
    },
    
    // Sample KNN Result
    knn: {
        algorithm: 'KNN',
        metrics: {
            accuracy: 0.967,
            n_neighbors: 5,
            n_classes: 3,
            n_features: 4,
            n_train_samples: 120,
            n_test_samples: 30
        },
        class_metrics: [
            { class: 0, accuracy: 0.97, precision: 0.95, recall: 0.98 },
            { class: 1, accuracy: 0.93, precision: 0.92, recall: 0.94 },
            { class: 2, accuracy: 0.99, precision: 0.98, recall: 1.0 }
        ]
    },
    
    // Sample timeline events
    timelineEvents: [
        {
            timestamp: new Date(Date.now() - 3000),
            type: 'success',
            icon: '✅',
            model: 'URL Diagnostics',
            message: 'Analysis completed successfully',
            duration: '1.23s'
        },
        {
            timestamp: new Date(Date.now() - 8000),
            type: 'info',
            icon: '🔄',
            model: 'KNN',
            message: 'Model training started',
            duration: '--'
        },
        {
            timestamp: new Date(Date.now() - 15000),
            type: 'success',
            icon: '📊',
            model: 'Linear Regression',
            message: 'Training completed with R²=0.923',
            duration: '2.45s'
        },
        {
            timestamp: new Date(Date.now() - 22000),
            type: 'info',
            icon: '🧠',
            model: 'AI Analyst',
            message: 'Deep analysis generated',
            duration: '5.67s'
        },
        {
            timestamp: new Date(Date.now() - 35000),
            type: 'warning',
            icon: '⚠️',
            model: 'PCA',
            message: 'Low variance ratio detected',
            duration: '1.89s'
        }
    ],
    
    // Model cards metadata
    modelCards: [
        {
            id: 'url-diagnostics',
            name: 'URL Health Diagnostics',
            icon: '🔍',
            description: 'Comprehensive health analysis for web URLs with SSL, performance, and security checks',
            status: 'ready',
            avgLatency: '1.2s',
            lastRun: new Date(Date.now() - 3000),
            totalRuns: 342,
            avgAccuracy: 'N/A',
            endpoint: 'http://localhost:8003'
        },
        {
            id: 'linear-regression',
            name: 'Linear Regression',
            icon: '📈',
            description: 'Supervised learning for continuous target prediction using least squares optimization',
            status: 'ready',
            avgLatency: '2.4s',
            lastRun: new Date(Date.now() - 15000),
            totalRuns: 456,
            avgAccuracy: '92.3%',
            endpoint: 'http://localhost:8001'
        },
        {
            id: 'pca',
            name: 'PCA Analysis',
            icon: '🌈',
            description: 'Dimensionality reduction using Principal Component Analysis for feature extraction',
            status: 'ready',
            avgLatency: '1.8s',
            lastRun: new Date(Date.now() - 35000),
            totalRuns: 234,
            avgAccuracy: 'N/A',
            endpoint: 'http://localhost:8002'
        },
        {
            id: 'knn',
            name: 'K-Nearest Neighbors',
            icon: '🎯',
            description: 'Instance-based learning for classification using distance-based similarity metrics',
            status: 'ready',
            avgLatency: '0.9s',
            lastRun: new Date(Date.now() - 8000),
            totalRuns: 215,
            avgAccuracy: '96.7%',
            endpoint: 'http://localhost:8004'
        }
    ],
    
    // Empty state messages
    emptyStates: {
        results: {
            icon: '📊',
            title: 'No Results Yet',
            message: 'Run an analysis to see results here',
            cta: 'Start Analysis',
            ctaAction: 'showQuickStart'
        },
        timeline: {
            icon: '⏱️',
            title: 'No Activity',
            message: 'Your analysis timeline will appear here',
            hint: 'Events are tracked in real-time as you run models'
        },
        recommendations: {
            icon: '💡',
            title: 'No Recommendations',
            message: 'Complete an analysis to get AI-powered recommendations',
            hint: 'Our AI will analyze your results and suggest improvements'
        }
    }
};

// Export for use in dashboard
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DEMO_DATA;
}
