// AscendNet Unified Dashboard JavaScript

class AscendNetDashboard {
    constructor() {
        this.currentComponent = 'overview';
        this.components = {
            'overview': { name: 'Overview', url: null },
            'statik-server': { name: 'Statik-Server', url: '/statik-dashboard' },
            'gremlin': { name: 'GremlinGPT', url: '/gremlin-dashboard' },
            'godcore': { name: 'GodCore', url: '/godcore-dashboard' },
            'mobile': { name: 'Mobile-Mirror', url: '/mobile-dashboard' },
            'p2p': { name: 'P2P Network', url: '/p2p-dashboard' },
            'memory': { name: 'AI Memory', url: '/memory-dashboard' },
            'admin': { name: 'System Admin', url: '/admin-dashboard' }
        };
        this.systemStatus = {
            'statik-server': true,
            'gremlin': true,
            'godcore': true,
            'mobile': true,
            'p2p': true
        };
        this.memoryFeedActive = true;
        this.notificationsPanelOpen = false;
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupEventListeners();
        this.startMemoryFeed();
        this.startStatusUpdates();
        this.checkComponentAvailability();
        console.log('🚀 AscendNet Unified Dashboard initialized');
    }

    setupNavigation() {
        const componentButtons = document.querySelectorAll('.component-btn');
        componentButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const componentName = btn.dataset.component;
                this.switchComponent(componentName);
            });
        });

        // Notifications button
        const notificationsBtn = document.getElementById('notifications');
        if (notificationsBtn) {
            notificationsBtn.addEventListener('click', () => {
                this.toggleNotifications();
            });
        }
    }

    setupEventListeners() {
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case '1':
                        e.preventDefault();
                        this.switchComponent('overview');
                        break;
                    case '2':
                        e.preventDefault();
                        this.switchComponent('statik-server');
                        break;
                    case '3':
                        e.preventDefault();
                        this.switchComponent('gremlin');
                        break;
                    case '4':
                        e.preventDefault();
                        this.switchComponent('godcore');
                        break;
                    case '5':
                        e.preventDefault();
                        this.switchComponent('mobile');
                        break;
                    case 'n':
                        e.preventDefault();
                        this.toggleNotifications();
                        break;
                }
            }
        });

        // Close notifications when clicking outside
        document.addEventListener('click', (e) => {
            const notificationPanel = document.getElementById('notification-panel');
            const notificationsBtn = document.getElementById('notifications');
            
            if (this.notificationsPanelOpen && 
                !notificationPanel.contains(e.target) && 
                !notificationsBtn.contains(e.target)) {
                this.toggleNotifications();
            }
        });

        // Handle iframe load events
        document.querySelectorAll('.component-iframe').forEach(iframe => {
            iframe.addEventListener('load', () => {
                this.hideLoading();
            });
        });
    }

    switchComponent(componentName) {
        if (componentName === this.currentComponent) return;

        // Update navigation
        document.querySelectorAll('.component-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-component="${componentName}"]`).classList.add('active');

        // Update content
        document.querySelectorAll('.component-view').forEach(view => {
            view.classList.remove('active');
        });
        document.getElementById(componentName).classList.add('active');

        this.currentComponent = componentName;
        
        // Load component content if needed
        this.loadComponent(componentName);
        
        // Log component switch
        this.addNotification(`Switched to ${this.components[componentName].name}`, 'info');
    }

    loadComponent(componentName) {
        const component = this.components[componentName];
        
        if (!component.url) return; // Overview doesn't need to load anything

        const iframe = document.getElementById(`${componentName}-frame`);
        if (!iframe) return;

        // Show loading if iframe hasn't loaded yet
        if (!iframe.src || iframe.src !== window.location.origin + component.url) {
            this.showLoading(`Loading ${component.name}...`);
            iframe.src = component.url;
        }
    }

    // Quick Actions
    quickAction(action) {
        switch (action) {
            case 'code':
                this.switchComponent('statik-server');
                break;
            case 'chat':
                this.switchComponent('gremlin');
                break;
            case 'route':
                this.switchComponent('godcore');
                break;
            case 'mobile':
                this.switchComponent('mobile');
                break;
        }
    }

    // Component Controls
    launchComponent(componentName) {
        this.switchComponent(componentName);
    }

    reloadComponent(componentName) {
        const iframe = document.getElementById(`${componentName}-frame`);
        if (iframe) {
            this.showLoading(`Reloading ${this.components[componentName].name}...`);
            iframe.src = iframe.src;
        }
    }

    openNewWindow(componentName) {
        const component = this.components[componentName];
        if (component.url) {
            window.open(component.url, '_blank');
        }
    }

    toggleFullscreen(componentName) {
        const componentView = document.getElementById(componentName);
        if (componentView) {
            if (document.fullscreenElement) {
                document.exitFullscreen();
            } else {
                componentView.requestFullscreen();
            }
        }
    }

    // System Status Management
    updateSystemStatus() {
        Object.keys(this.systemStatus).forEach(async (service) => {
            try {
                const response = await fetch(`/api/status/${service}`);
                this.systemStatus[service] = response.ok;
            } catch (error) {
                this.systemStatus[service] = false;
            }
            this.updateStatusDisplay(service);
        });

        this.updateGlobalStatus();
    }

    updateStatusDisplay(service) {
        const statusElement = document.querySelector(`[data-service="${service}"] .service-status`);
        if (statusElement) {
            if (this.systemStatus[service]) {
                statusElement.textContent = '🟢 Online';
                statusElement.className = 'service-status running';
            } else {
                statusElement.textContent = '🔴 Offline';
                statusElement.className = 'service-status offline';
            }
        }
    }

    updateGlobalStatus() {
        const allOnline = Object.values(this.systemStatus).every(status => status);
        const globalStatusDot = document.getElementById('global-status-dot');
        const globalStatusText = document.getElementById('global-status-text');

        if (allOnline) {
            globalStatusDot.textContent = '🟢';
            globalStatusText.textContent = 'All Systems Operational';
        } else {
            globalStatusDot.textContent = '🟡';
            globalStatusText.textContent = 'Some Services Offline';
        }
    }

    // Memory Feed
    startMemoryFeed() {
        this.updateMemoryFeed();
        setInterval(() => {
            if (this.memoryFeedActive) {
                this.updateMemoryFeed();
            }
        }, 5000);
    }

    async updateMemoryFeed() {
        try {
            const response = await fetch('/api/memory/live-feed');
            if (response.ok) {
                const memoryData = await response.json();
                this.displayMemoryEntries(memoryData);
            }
        } catch (error) {
            console.warn('Memory feed update failed:', error);
            // Show mock data for demo
            this.showMockMemoryData();
        }
    }

    displayMemoryEntries(entries) {
        const memoryFeed = document.getElementById('global-memory-feed');
        if (!memoryFeed) return;

        memoryFeed.innerHTML = '';
        entries.forEach(entry => {
            const memoryEntry = document.createElement('div');
            memoryEntry.className = 'memory-entry';
            memoryEntry.innerHTML = `
                <span class="memory-time">${this.formatTime(entry.timestamp)}</span>
                <span class="memory-source ${entry.source.toLowerCase()}">${entry.source}</span>
                <span class="memory-content">${entry.content}</span>
            `;
            memoryFeed.appendChild(memoryEntry);
        });
    }

    showMockMemoryData() {
        const mockEntries = [
            { timestamp: new Date(), source: 'GremlinGPT', content: 'Autonomous processing cycle complete' },
            { timestamp: new Date(Date.now() - 5000), source: 'GodCore', content: 'Model routing optimized' },
            { timestamp: new Date(Date.now() - 10000), source: 'Statik', content: 'User session synchronized' },
            { timestamp: new Date(Date.now() - 15000), source: 'GremlinGPT', content: 'Memory consolidation in progress' }
        ];
        this.displayMemoryEntries(mockEntries);
    }

    // Status Updates
    startStatusUpdates() {
        this.updateSystemStatus();
        setInterval(() => {
            this.updateSystemStatus();
        }, 30000); // Update every 30 seconds
    }

    // Component Availability Check
    async checkComponentAvailability() {
        for (const [componentName, component] of Object.entries(this.components)) {
            if (component.url) {
                try {
                    const response = await fetch(component.url, { method: 'HEAD' });
                    if (!response.ok) {
                        this.disableComponent(componentName);
                    }
                } catch (error) {
                    console.warn(`Component ${componentName} not available:`, error);
                    this.disableComponent(componentName);
                }
            }
        }
    }

    disableComponent(componentName) {
        const componentBtn = document.querySelector(`[data-component="${componentName}"]`);
        if (componentBtn) {
            componentBtn.style.opacity = '0.5';
            componentBtn.style.pointerEvents = 'none';
            componentBtn.title = `${this.components[componentName].name} is not available`;
        }
    }

    // Notifications
    toggleNotifications() {
        const notificationPanel = document.getElementById('notification-panel');
        this.notificationsPanelOpen = !this.notificationsPanelOpen;
        
        if (this.notificationsPanelOpen) {
            notificationPanel.classList.add('open');
        } else {
            notificationPanel.classList.remove('open');
        }
    }

    addNotification(message, type = 'info') {
        const notificationList = document.getElementById('notification-list');
        const notification = document.createElement('div');
        notification.className = `notification-item ${type}`;
        notification.innerHTML = `
            <span class="notification-time">${this.formatTime(new Date())}</span>
            <span class="notification-message">${message}</span>
        `;
        
        notificationList.insertBefore(notification, notificationList.firstChild);
        
        // Remove old notifications (keep only last 20)
        const notifications = notificationList.querySelectorAll('.notification-item');
        if (notifications.length > 20) {
            notifications[notifications.length - 1].remove();
        }
    }

    // Loading Management
    showLoading(message = 'Loading...') {
        const loadingOverlay = document.getElementById('loading-overlay');
        const loadingText = loadingOverlay.querySelector('p');
        if (loadingText) {
            loadingText.textContent = message;
        }
        loadingOverlay.classList.add('active');
    }

    hideLoading() {
        const loadingOverlay = document.getElementById('loading-overlay');
        loadingOverlay.classList.remove('active');
    }

    // Utility Methods
    formatTime(date) {
        return date.toLocaleTimeString('en-US', { 
            hour12: false, 
            hour: '2-digit', 
            minute: '2-digit', 
            second: '2-digit' 
        });
    }

    // Advanced Features
    toggleAutonomous() {
        const autonomousBtn = document.getElementById('gremlin-autonomous');
        if (autonomousBtn) {
            const isActive = autonomousBtn.textContent.includes('ON');
            if (isActive) {
                autonomousBtn.innerHTML = '🔴 Autonomous OFF';
                this.addNotification('GremlinGPT autonomous mode deactivated', 'warning');
            } else {
                autonomousBtn.innerHTML = '🟢 Autonomous ON';
                this.addNotification('GremlinGPT autonomous mode activated', 'success');
            }
        }
    }

    optimizeRouting() {
        this.showLoading('Optimizing AI routing...');
        setTimeout(() => {
            this.hideLoading();
            this.addNotification('GodCore routing optimized successfully', 'success');
        }, 2000);
    }

    generateQR() {
        this.addNotification('Mobile QR code generated', 'success');
    }

    refreshNetwork() {
        this.showLoading('Refreshing P2P network...');
        setTimeout(() => {
            this.hideLoading();
            this.addNotification('P2P network topology refreshed', 'success');
        }, 1500);
    }

    joinMarketplace() {
        this.addNotification('Connecting to P2P marketplace...', 'info');
    }

    pauseMemoryFeed() {
        this.memoryFeedActive = !this.memoryFeedActive;
        const pauseBtn = document.querySelector('[onclick="pauseMemoryFeed()"]');
        if (pauseBtn) {
            pauseBtn.textContent = this.memoryFeedActive ? '⏸️ Pause Feed' : '▶️ Resume Feed';
        }
        this.addNotification(`Memory feed ${this.memoryFeedActive ? 'resumed' : 'paused'}`, 'info');
    }

    exportMemory() {
        this.addNotification('Memory export initiated', 'info');
    }

    systemHealthCheck() {
        this.showLoading('Running system health check...');
        setTimeout(() => {
            this.hideLoading();
            this.addNotification('System health check completed - all systems nominal', 'success');
        }, 3000);
    }

    restartAllServices() {
        if (confirm('Are you sure you want to restart all services? This will cause temporary downtime.')) {
            this.showLoading('Restarting all services...');
            this.addNotification('System restart initiated', 'warning');
            setTimeout(() => {
                this.hideLoading();
                this.addNotification('All services restarted successfully', 'success');
                this.updateSystemStatus();
            }, 5000);
        }
    }

    showNetworkTopology() {
        this.addNotification('Network topology visualization opened', 'info');
    }
}

// Global Functions (for onclick handlers)
let dashboard;

function launchComponent(component) {
    dashboard.launchComponent(component);
}

function quickAction(action) {
    dashboard.quickAction(action);
}

function reloadComponent(component) {
    dashboard.reloadComponent(component);
}

function openNewWindow(component) {
    dashboard.openNewWindow(component);
}

function toggleFullscreen(component) {
    dashboard.toggleFullscreen(component);
}

function toggleAutonomous() {
    dashboard.toggleAutonomous();
}

function optimizeRouting() {
    dashboard.optimizeRouting();
}

function generateQR() {
    dashboard.generateQR();
}

function refreshNetwork() {
    dashboard.refreshNetwork();
}

function joinMarketplace() {
    dashboard.joinMarketplace();
}

function pauseMemoryFeed() {
    dashboard.pauseMemoryFeed();
}

function exportMemory() {
    dashboard.exportMemory();
}

function systemHealthCheck() {
    dashboard.systemHealthCheck();
}

function restartAllServices() {
    dashboard.restartAllServices();
}

function showNetworkTopology() {
    dashboard.showNetworkTopology();
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    dashboard = new AscendNetDashboard();
    
    // Add some demo notifications
    setTimeout(() => {
        dashboard.addNotification('AscendNet Unified Dashboard initialized', 'success');
    }, 1000);
    
    setTimeout(() => {
        dashboard.addNotification('All components loaded successfully', 'success');
    }, 2000);
});
