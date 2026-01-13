/**
 * MCP Feedback Enhanced - 连线监控模组
 * ===================================
 * 
 * 处理 WebSocket 连线状态监控、品质检测和诊断功能
 */

(function() {
    'use strict';

    // 确保命名空间和依赖存在
    window.MCPFeedback = window.MCPFeedback || {};
    const Utils = window.MCPFeedback.Utils;

    /**
     * 连线监控器建构函数
     */
    function ConnectionMonitor(options) {
        options = options || {};
        
        // 监控状态
        this.isMonitoring = false;
        this.connectionStartTime = null;
        this.lastPingTime = null;
        this.latencyHistory = [];
        this.maxLatencyHistory = 20;
        this.reconnectCount = 0;
        this.messageCount = 0;
        
        // 连线品质指标
        this.currentLatency = 0;
        this.averageLatency = 0;
        this.connectionQuality = 'unknown'; // excellent, good, fair, poor, unknown
        
        // UI 元素
        this.statusIcon = null;
        this.statusText = null;
        this.latencyDisplay = null;
        this.connectionTimeDisplay = null;
        this.reconnectCountDisplay = null;
        this.messageCountDisplay = null;
        this.signalBars = null;
        
        // 回调函数
        this.onStatusChange = options.onStatusChange || null;
        this.onQualityChange = options.onQualityChange || null;
        
        this.initializeUI();
        
        console.log('🔍 ConnectionMonitor 初始化完成');
    }

    /**
     * 初始化 UI 元素
     */
    ConnectionMonitor.prototype.initializeUI = function() {
        // 获取 UI 元素引用
        this.statusIcon = Utils.safeQuerySelector('.status-icon');
        this.statusText = Utils.safeQuerySelector('.status-text');
        this.latencyDisplay = Utils.safeQuerySelector('.latency-indicator');
        this.connectionTimeDisplay = Utils.safeQuerySelector('.connection-time');
        this.reconnectCountDisplay = Utils.safeQuerySelector('.reconnect-count');
        this.messageCountDisplay = Utils.safeQuerySelector('#messageCount');
        this.latencyDisplayFooter = Utils.safeQuerySelector('#latencyDisplay');
        this.signalBars = document.querySelectorAll('.signal-bar');
        
        // 初始化显示
        this.updateDisplay();
    };

    /**
     * 开始监控
     */
    ConnectionMonitor.prototype.startMonitoring = function() {
        if (this.isMonitoring) return;
        
        this.isMonitoring = true;
        this.connectionStartTime = Date.now();
        this.reconnectCount = 0;
        this.messageCount = 0;
        this.latencyHistory = [];
        
        console.log('🔍 开始连线监控');
        this.updateDisplay();
    };

    /**
     * 停止监控
     */
    ConnectionMonitor.prototype.stopMonitoring = function() {
        this.isMonitoring = false;
        this.connectionStartTime = null;
        this.lastPingTime = null;
        
        console.log('🔍 停止连线监控');
        this.updateDisplay();
    };

    /**
     * 更新连线状态
     */
    ConnectionMonitor.prototype.updateConnectionStatus = function(status, message) {
        console.log('🔍 连线状态更新:', status, message);

        // 更新状态显示
        if (this.statusText) {
            // 使用 i18n 翻译或提供的讯息
            const displayText = message || (window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.Status ?
                window.MCPFeedback.Utils.Status.getConnectionStatusText(status) : status);
            this.statusText.textContent = displayText;
        }

        // 更新状态图示
        if (this.statusIcon) {
            this.statusIcon.className = 'status-icon';

            switch (status) {
                case 'connecting':
                case 'reconnecting':
                    this.statusIcon.classList.add('pulse');
                    break;
                case 'connected':
                    this.statusIcon.classList.remove('pulse');
                    break;
                default:
                    this.statusIcon.classList.remove('pulse');
            }
        }

        // 更新连线指示器样式
        const indicator = Utils.safeQuerySelector('.connection-indicator');
        if (indicator) {
            indicator.className = 'connection-indicator ' + status;
        }
        
        // 更新精简的顶部状态指示器（现在是紧凑版）
        const minimalIndicator = document.getElementById('connectionStatusMinimal');
        if (minimalIndicator) {
            minimalIndicator.className = 'connection-status-compact ' + status;
            const statusText = minimalIndicator.querySelector('.status-text');
            if (statusText) {
                let statusKey = '';
                switch (status) {
                    case 'connected':
                        statusKey = 'connectionMonitor.connected';
                        break;
                    case 'connecting':
                        statusKey = 'connectionMonitor.connecting';
                        break;
                    case 'disconnected':
                        statusKey = 'connectionMonitor.disconnected';
                        break;
                    case 'reconnecting':
                        statusKey = 'connectionMonitor.reconnecting';
                        break;
                    default:
                        statusKey = 'connectionMonitor.unknown';
                }
                statusText.setAttribute('data-i18n', statusKey);
                if (window.i18nManager) {
                    statusText.textContent = window.i18nManager.t(statusKey);
                }
            }
        }
        
        // 处理特殊状态
        switch (status) {
            case 'connected':
                if (!this.isMonitoring) {
                    this.startMonitoring();
                }
                break;
            case 'disconnected':
            case 'error':
                this.stopMonitoring();
                break;
            case 'reconnecting':
                this.reconnectCount++;
                break;
        }
        
        this.updateDisplay();
        
        // 调用回调
        if (this.onStatusChange) {
            this.onStatusChange(status, message);
        }
    };

    /**
     * 记录 ping 时间
     */
    ConnectionMonitor.prototype.recordPing = function() {
        this.lastPingTime = Date.now();
    };

    /**
     * 记录 pong 时间并计算延迟
     */
    ConnectionMonitor.prototype.recordPong = function() {
        if (!this.lastPingTime) return;
        
        const now = Date.now();
        const latency = now - this.lastPingTime;
        
        this.currentLatency = latency;
        this.latencyHistory.push(latency);
        
        // 保持历史记录在限制范围内
        if (this.latencyHistory.length > this.maxLatencyHistory) {
            this.latencyHistory.shift();
        }
        
        // 计算平均延迟
        this.averageLatency = this.latencyHistory.reduce((sum, lat) => sum + lat, 0) / this.latencyHistory.length;
        
        // 更新连线品质
        this.updateConnectionQuality();
        
        console.log('🔍 延迟测量:', latency + 'ms', '平均:', Math.round(this.averageLatency) + 'ms');
        
        this.updateDisplay();
    };

    /**
     * 记录讯息
     */
    ConnectionMonitor.prototype.recordMessage = function() {
        this.messageCount++;
        this.updateDisplay();
    };

    /**
     * 更新连线品质
     */
    ConnectionMonitor.prototype.updateConnectionQuality = function() {
        const avgLatency = this.averageLatency;
        let quality;
        
        if (avgLatency < 50) {
            quality = 'excellent';
        } else if (avgLatency < 100) {
            quality = 'good';
        } else if (avgLatency < 200) {
            quality = 'fair';
        } else {
            quality = 'poor';
        }
        
        if (quality !== this.connectionQuality) {
            this.connectionQuality = quality;
            this.updateSignalStrength();
            
            if (this.onQualityChange) {
                this.onQualityChange(quality, avgLatency);
            }
        }
    };

    /**
     * 更新信号强度显示
     */
    ConnectionMonitor.prototype.updateSignalStrength = function() {
        if (!this.signalBars || this.signalBars.length === 0) return;
        
        let activeBars = 0;
        
        switch (this.connectionQuality) {
            case 'excellent':
                activeBars = 3;
                break;
            case 'good':
                activeBars = 2;
                break;
            case 'fair':
                activeBars = 1;
                break;
            case 'poor':
            default:
                activeBars = 0;
                break;
        }
        
        this.signalBars.forEach(function(bar, index) {
            if (index < activeBars) {
                bar.classList.add('active');
            } else {
                bar.classList.remove('active');
            }
        });
    };

    /**
     * 更新显示
     */
    ConnectionMonitor.prototype.updateDisplay = function() {
        // 更新延迟显示
        if (this.latencyDisplay) {
            const latencyLabel = window.i18nManager ? window.i18nManager.t('connectionMonitor.latency') : '延迟';
            if (this.currentLatency > 0) {
                this.latencyDisplay.textContent = latencyLabel + ': ' + this.currentLatency + 'ms';
            } else {
                this.latencyDisplay.textContent = latencyLabel + ': --ms';
            }
        }
        
        if (this.latencyDisplayFooter) {
            if (this.currentLatency > 0) {
                this.latencyDisplayFooter.textContent = this.currentLatency + 'ms';
            } else {
                this.latencyDisplayFooter.textContent = '--ms';
            }
        }
        
        // 更新统计面板中的延迟显示
        const statsLatency = document.getElementById('statsLatency');
        if (statsLatency) {
            statsLatency.textContent = this.currentLatency > 0 ? this.currentLatency + 'ms' : '--ms';
        }
        
        // 更新连线时间
        let connectionTimeStr = '--:--';
        if (this.connectionStartTime) {
            const duration = Math.floor((Date.now() - this.connectionStartTime) / 1000);
            const minutes = Math.floor(duration / 60);
            const seconds = duration % 60;
            connectionTimeStr = String(minutes).padStart(2, '0') + ':' + String(seconds).padStart(2, '0');
        }
        
        if (this.connectionTimeDisplay) {
            const connectionTimeLabel = window.i18nManager ? window.i18nManager.t('connectionMonitor.connectionTime') : '连线时间';
            this.connectionTimeDisplay.textContent = connectionTimeLabel + ': ' + connectionTimeStr;
        }
        
        // 更新统计面板中的连线时间
        const statsConnectionTime = document.getElementById('statsConnectionTime');
        if (statsConnectionTime) {
            statsConnectionTime.textContent = connectionTimeStr;
        }
        
        // 更新重连次数
        if (this.reconnectCountDisplay) {
            const reconnectLabel = window.i18nManager ? window.i18nManager.t('connectionMonitor.reconnectCount') : '重连';
            const timesLabel = window.i18nManager ? window.i18nManager.t('connectionMonitor.times') : '次';
            this.reconnectCountDisplay.textContent = reconnectLabel + ': ' + this.reconnectCount + ' ' + timesLabel;
        }
        
        // 更新统计面板中的重连次数
        const statsReconnectCount = document.getElementById('statsReconnectCount');
        if (statsReconnectCount) {
            statsReconnectCount.textContent = this.reconnectCount.toString();
        }
        
        // 更新讯息计数
        if (this.messageCountDisplay) {
            this.messageCountDisplay.textContent = this.messageCount;
        }
        
        // 更新统计面板中的讯息计数
        const statsMessageCount = document.getElementById('statsMessageCount');
        if (statsMessageCount) {
            statsMessageCount.textContent = this.messageCount.toString();
        }
        
        // 更新统计面板中的会话数和状态
        const sessionCount = document.getElementById('sessionCount');
        const statsSessionCount = document.getElementById('statsSessionCount');
        if (sessionCount && statsSessionCount) {
            statsSessionCount.textContent = sessionCount.textContent;
        }
        
        const sessionStatusText = document.getElementById('sessionStatusText');
        const statsSessionStatus = document.getElementById('statsSessionStatus');
        if (sessionStatusText && statsSessionStatus) {
            statsSessionStatus.textContent = sessionStatusText.textContent;
        }
    };

    /**
     * 获取连线统计资讯
     */
    ConnectionMonitor.prototype.getConnectionStats = function() {
        return {
            isMonitoring: this.isMonitoring,
            connectionTime: this.connectionStartTime ? Date.now() - this.connectionStartTime : 0,
            currentLatency: this.currentLatency,
            averageLatency: Math.round(this.averageLatency),
            connectionQuality: this.connectionQuality,
            reconnectCount: this.reconnectCount,
            messageCount: this.messageCount,
            latencyHistory: this.latencyHistory.slice() // 复制阵列
        };
    };

    /**
     * 重置统计
     */
    ConnectionMonitor.prototype.resetStats = function() {
        this.reconnectCount = 0;
        this.messageCount = 0;
        this.latencyHistory = [];
        this.currentLatency = 0;
        this.averageLatency = 0;
        this.connectionQuality = 'unknown';
        
        this.updateDisplay();
        this.updateSignalStrength();
        
        console.log('🔍 连线统计已重置');
    };

    /**
     * 清理资源
     */
    ConnectionMonitor.prototype.cleanup = function() {
        this.stopMonitoring();
        
        // 清理 UI 引用
        this.statusIcon = null;
        this.statusText = null;
        this.latencyDisplay = null;
        this.connectionTimeDisplay = null;
        this.reconnectCountDisplay = null;
        this.messageCountDisplay = null;
        this.signalBars = null;
        
        console.log('🔍 ConnectionMonitor 清理完成');
    };

    // 将 ConnectionMonitor 加入命名空间
    window.MCPFeedback.ConnectionMonitor = ConnectionMonitor;

    console.log('✅ ConnectionMonitor 模组载入完成');

})();
