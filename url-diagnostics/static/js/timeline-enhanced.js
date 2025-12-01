// ============================================================================
// TransparentML Enhanced Timeline - Rich Event Visualization
// ============================================================================

class EnhancedTimeline {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.events = [];
        this.filteredEvents = [];
        this.filters = {
            type: 'all',
            service: 'all',
            timeRange: 'all'
        };
        this.options = {
            maxEvents: options.maxEvents || 50,
            autoScroll: options.autoScroll !== false,
            showMetadata: options.showMetadata !== false,
            enableZoom: options.enableZoom !== false,
            ...options
        };
        
        this.init();
    }
    
    init() {
        if (!this.container) return;
        
        // Create enhanced timeline structure
        this.container.innerHTML = `
            <div class="enhanced-timeline">
                <!-- Timeline Controls -->
                <div class="timeline-controls">
                    <div class="timeline-filters">
                        <select id="timelineTypeFilter" class="timeline-filter">
                            <option value="all">All Types</option>
                            <option value="info">✅ Info</option>
                            <option value="warning">⚠️ Warning</option>
                            <option value="error">❌ Error</option>
                        </select>
                        
                        <select id="timelineServiceFilter" class="timeline-filter">
                            <option value="all">All Services</option>
                            <option value="url-diagnostics">🔍 URL Diagnostics</option>
                            <option value="linear-regression">📈 Linear Regression</option>
                            <option value="pca">🌈 PCA</option>
                            <option value="knn">🎯 KNN</option>
                            <option value="ollama">🤖 Ollama AI</option>
                        </select>
                        
                        <select id="timelineRangeFilter" class="timeline-filter">
                            <option value="all">All Time</option>
                            <option value="last-10">Last 10 events</option>
                            <option value="last-30">Last 30 events</option>
                            <option value="1h">Last hour</option>
                            <option value="24h">Last 24 hours</option>
                        </select>
                    </div>
                    
                    <div class="timeline-actions">
                        <button id="timelineClearBtn" class="timeline-btn" title="Clear timeline">
                            🗑️ Clear
                        </button>
                        <button id="timelineExportBtn" class="timeline-btn" title="Export timeline">
                            💾 Export
                        </button>
                        <span class="timeline-count" id="timelineCount">0 events</span>
                    </div>
                </div>
                
                <!-- Timeline View -->
                <div class="timeline-view" id="timelineView">
                    <div class="timeline-empty-state">
                        <div class="timeline-empty-icon">⏱️</div>
                        <div class="timeline-empty-text">No events yet</div>
                        <div class="timeline-empty-hint">Events will appear here as actions occur</div>
                    </div>
                </div>
                
                <!-- Timeline Summary -->
                <div class="timeline-summary" id="timelineSummary">
                    <div class="summary-stat">
                        <span class="summary-label">Total:</span>
                        <span class="summary-value" id="summaryTotal">0</span>
                    </div>
                    <div class="summary-stat info">
                        <span class="summary-label">✅ Info:</span>
                        <span class="summary-value" id="summaryInfo">0</span>
                    </div>
                    <div class="summary-stat warning">
                        <span class="summary-label">⚠️ Warning:</span>
                        <span class="summary-value" id="summaryWarning">0</span>
                    </div>
                    <div class="summary-stat error">
                        <span class="summary-label">❌ Error:</span>
                        <span class="summary-value" id="summaryError">0</span>
                    </div>
                </div>
            </div>
        `;
        
        this.attachEventListeners();
    }
    
    attachEventListeners() {
        // Filter listeners
        document.getElementById('timelineTypeFilter')?.addEventListener('change', (e) => {
            this.filters.type = e.target.value;
            this.applyFilters();
        });
        
        document.getElementById('timelineServiceFilter')?.addEventListener('change', (e) => {
            this.filters.service = e.target.value;
            this.applyFilters();
        });
        
        document.getElementById('timelineRangeFilter')?.addEventListener('change', (e) => {
            this.filters.timeRange = e.target.value;
            this.applyFilters();
        });
        
        // Action listeners
        document.getElementById('timelineClearBtn')?.addEventListener('click', () => {
            this.clear();
        });
        
        document.getElementById('timelineExportBtn')?.addEventListener('click', () => {
            this.export();
        });
    }
    
    addEvent(event) {
        // Validate event structure
        if (!event.time || !event.type || !event.message) {
            console.warn('Invalid event structure:', event);
            return;
        }
        
        // Enrich event with additional data
        const enrichedEvent = {
            id: `evt_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            time: event.time instanceof Date ? event.time : new Date(event.time || Date.now()),
            type: event.type || 'info',
            service: event.service || 'system',
            message: event.message,
            duration: event.duration || null,
            metadata: event.metadata || {},
            icon: this.getEventIcon(event.type, event.service)
        };
        
        this.events.unshift(enrichedEvent); // Add to beginning
        
        // Limit total events
        if (this.events.length > this.options.maxEvents) {
            this.events = this.events.slice(0, this.options.maxEvents);
        }
        
        this.applyFilters();
        this.updateSummary();
    }
    
    getEventIcon(type, service) {
        // Service icons
        const serviceIcons = {
            'url-diagnostics': '🔍',
            'linear-regression': '📈',
            'pca': '🌈',
            'knn': '🎯',
            'ollama': '🤖',
            'vector-memory': '💾',
            'system': '⚙️'
        };
        
        // Type indicators
        const typeIndicators = {
            'info': '✅',
            'warning': '⚠️',
            'error': '❌'
        };
        
        return `${serviceIcons[service] || '📌'} ${typeIndicators[type] || 'ℹ️'}`;
    }
    
    applyFilters() {
        let filtered = [...this.events];
        
        // Filter by type
        if (this.filters.type !== 'all') {
            filtered = filtered.filter(e => e.type === this.filters.type);
        }
        
        // Filter by service
        if (this.filters.service !== 'all') {
            filtered = filtered.filter(e => e.service === this.filters.service);
        }
        
        // Filter by time range
        if (this.filters.timeRange !== 'all') {
            const now = Date.now();
            switch (this.filters.timeRange) {
                case 'last-10':
                    filtered = filtered.slice(0, 10);
                    break;
                case 'last-30':
                    filtered = filtered.slice(0, 30);
                    break;
                case '1h':
                    filtered = filtered.filter(e => (now - e.time.getTime()) < 3600000);
                    break;
                case '24h':
                    filtered = filtered.filter(e => (now - e.time.getTime()) < 86400000);
                    break;
            }
        }
        
        this.filteredEvents = filtered;
        this.render();
    }
    
    render() {
        const view = document.getElementById('timelineView');
        if (!view) return;
        
        if (this.filteredEvents.length === 0) {
            view.innerHTML = `
                <div class="timeline-empty-state">
                    <div class="timeline-empty-icon">⏱️</div>
                    <div class="timeline-empty-text">No events match filters</div>
                    <div class="timeline-empty-hint">Try adjusting your filters</div>
                </div>
            `;
            return;
        }
        
        // Group events by time proximity (same minute)
        const groupedEvents = this.groupEventsByTime(this.filteredEvents);
        
        view.innerHTML = groupedEvents.map(group => this.renderEventGroup(group)).join('');
        
        // Auto-scroll to bottom if enabled
        if (this.options.autoScroll) {
            view.scrollTop = view.scrollHeight;
        }
        
        // Update count
        document.getElementById('timelineCount').textContent = 
            `${this.filteredEvents.length} event${this.filteredEvents.length !== 1 ? 's' : ''}`;
    }
    
    groupEventsByTime(events) {
        const groups = [];
        let currentGroup = null;
        
        events.forEach(event => {
            const timeKey = event.time.toLocaleTimeString('en-US', { 
                hour: '2-digit', 
                minute: '2-digit' 
            });
            
            if (!currentGroup || currentGroup.timeKey !== timeKey) {
                currentGroup = {
                    timeKey,
                    timestamp: event.time,
                    events: []
                };
                groups.push(currentGroup);
            }
            
            currentGroup.events.push(event);
        });
        
        return groups;
    }
    
    renderEventGroup(group) {
        const relativeTime = this.getRelativeTime(group.timestamp);
        
        return `
            <div class="timeline-group">
                <div class="timeline-group-header">
                    <span class="timeline-group-time">🕐 ${group.timeKey}</span>
                    <span class="timeline-group-relative">${relativeTime}</span>
                    <span class="timeline-group-count">${group.events.length} event${group.events.length !== 1 ? 's' : ''}</span>
                </div>
                <div class="timeline-group-events">
                    ${group.events.map(event => this.renderEvent(event)).join('')}
                </div>
            </div>
        `;
    }
    
    renderEvent(event) {
        const durationText = event.duration ? 
            `<span class="event-duration">⏱️ ${event.duration.toFixed(2)}s</span>` : '';
        
        const metadataHtml = this.options.showMetadata && Object.keys(event.metadata).length > 0 ?
            `<div class="event-metadata">
                ${Object.entries(event.metadata).map(([key, value]) => 
                    `<span class="metadata-item"><strong>${key}:</strong> ${value}</span>`
                ).join('')}
            </div>` : '';
        
        return `
            <div class="timeline-event timeline-event-${event.type}" data-event-id="${event.id}">
                <div class="event-indicator"></div>
                <div class="event-content">
                    <div class="event-header">
                        <span class="event-icon">${event.icon}</span>
                        <span class="event-service">${this.formatService(event.service)}</span>
                        ${durationText}
                    </div>
                    <div class="event-message">${event.message}</div>
                    ${metadataHtml}
                </div>
            </div>
        `;
    }
    
    formatService(service) {
        const names = {
            'url-diagnostics': 'URL Diagnostics',
            'linear-regression': 'Linear Regression',
            'pca': 'PCA',
            'knn': 'KNN',
            'ollama': 'Ollama AI',
            'vector-memory': 'Vector Memory',
            'system': 'System'
        };
        return names[service] || service;
    }
    
    getRelativeTime(date) {
        const seconds = Math.floor((Date.now() - date.getTime()) / 1000);
        
        if (seconds < 10) return 'just now';
        if (seconds < 60) return `${seconds}s ago`;
        
        const minutes = Math.floor(seconds / 60);
        if (minutes < 60) return `${minutes}m ago`;
        
        const hours = Math.floor(minutes / 60);
        if (hours < 24) return `${hours}h ago`;
        
        const days = Math.floor(hours / 24);
        return `${days}d ago`;
    }
    
    updateSummary() {
        const stats = {
            total: this.events.length,
            info: this.events.filter(e => e.type === 'info').length,
            warning: this.events.filter(e => e.type === 'warning').length,
            error: this.events.filter(e => e.type === 'error').length
        };
        
        document.getElementById('summaryTotal').textContent = stats.total;
        document.getElementById('summaryInfo').textContent = stats.info;
        document.getElementById('summaryWarning').textContent = stats.warning;
        document.getElementById('summaryError').textContent = stats.error;
    }
    
    clear() {
        if (confirm('Clear all timeline events?')) {
            this.events = [];
            this.filteredEvents = [];
            this.applyFilters();
            this.updateSummary();
        }
    }
    
    export() {
        const data = this.filteredEvents.map(event => ({
            time: event.time.toISOString(),
            type: event.type,
            service: event.service,
            message: event.message,
            duration: event.duration,
            metadata: event.metadata
        }));
        
        const json = JSON.stringify(data, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `timeline-export-${new Date().toISOString()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }
    
    // Public API for adding events with rich metadata
    logEvent(type, service, message, options = {}) {
        this.addEvent({
            type,
            service,
            message,
            duration: options.duration,
            metadata: options.metadata || {},
            time: options.time || new Date()
        });
    }
}

// Export for use in dashboard
if (typeof module !== 'undefined' && module.exports) {
    module.exports = EnhancedTimeline;
}
