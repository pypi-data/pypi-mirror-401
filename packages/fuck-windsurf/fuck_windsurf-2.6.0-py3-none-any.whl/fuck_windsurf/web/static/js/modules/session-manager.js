/**
 * MCP Feedback Enhanced - 会话管理模组（重构版）
 * =============================================
 *
 * 整合会话数据管理、UI 渲染和面板控制功能
 * 使用模组化架构提升可维护性
 */

(function() {
    'use strict';

    // 确保命名空间和依赖存在
    window.MCPFeedback = window.MCPFeedback || {};

    // 获取 DOMUtils 的安全方法
    function getDOMUtils() {
        return window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.DOM;
    }

    /**
     * 会话管理器建构函数（重构版）
     */
    function SessionManager(options) {
        options = options || {};

        // 子模组实例
        this.dataManager = null;
        this.uiRenderer = null;
        this.detailsModal = null;

        // UI 状态
        this.isLoading = false;

        // 设定管理器引用
        this.settingsManager = options.settingsManager || null;

        // 回调函数
        this.onSessionChange = options.onSessionChange || null;
        this.onSessionSelect = options.onSessionSelect || null;

        this.initializeModules(options);
        this.setupEventListeners();

        console.log('📋 SessionManager (重构版) 初始化完成');
    }

    /**
     * 初始化子模组
     */
    SessionManager.prototype.initializeModules = function(options) {
        const self = this;

        // 先初始化 UI 渲染器（避免数据管理器回调时 UI 组件尚未准备好）
        this.uiRenderer = new window.MCPFeedback.Session.UIRenderer({
            showFullSessionId: options.showFullSessionId || false,
            enableAnimations: options.enableAnimations !== false
        });

        // 初始化详情弹窗
        this.detailsModal = new window.MCPFeedback.Session.DetailsModal({
            enableEscapeClose: options.enableEscapeClose !== false,
            enableBackdropClose: options.enableBackdropClose !== false,
            showFullSessionId: options.showFullSessionId || false
        });

        // 初始化防抖处理器
        this.initDebounceHandlers();

        // 最后初始化数据管理器（确保 UI 组件已准备好接收回调）
        this.dataManager = new window.MCPFeedback.Session.DataManager({
            settingsManager: this.settingsManager,
            onSessionChange: function(sessionData) {
                self.handleSessionChange(sessionData);
            },
            onHistoryChange: function(history) {
                self.handleHistoryChange(history);
            },
            onStatsChange: function(stats) {
                self.handleStatsChange(stats);
            },
            onDataChanged: function() {
                self.handleDataChanged();
            }
        });
    };

    /**
     * 初始化防抖处理器
     */
    SessionManager.prototype.initDebounceHandlers = function() {
        // 为会话变更处理添加防抖
        this._debouncedHandleSessionChange = window.MCPFeedback.Utils.DOM.debounce(
            this._originalHandleSessionChange.bind(this),
            100,
            false
        );

        // 为历史记录变更处理添加防抖
        this._debouncedHandleHistoryChange = window.MCPFeedback.Utils.DOM.debounce(
            this._originalHandleHistoryChange.bind(this),
            150,
            false
        );

        // 为统计资讯变更处理添加防抖
        this._debouncedHandleStatsChange = window.MCPFeedback.Utils.DOM.debounce(
            this._originalHandleStatsChange.bind(this),
            100,
            false
        );

        // 为资料变更处理添加防抖
        this._debouncedHandleDataChanged = window.MCPFeedback.Utils.DOM.debounce(
            this._originalHandleDataChanged.bind(this),
            200,
            false
        );
    };

    /**
     * 处理会话变更（原始版本，供防抖使用）
     */
    SessionManager.prototype._originalHandleSessionChange = function(sessionData) {
        // 减少重复日志：只在会话 ID 变化时记录
        const sessionId = sessionData ? sessionData.session_id : null;
        if (!this._lastSessionId || this._lastSessionId !== sessionId) {
            console.log('📋 处理会话变更:', sessionData);
            this._lastSessionId = sessionId;
        }

        // 更新 UI 渲染
        this.uiRenderer.renderCurrentSession(sessionData);

        // 调用外部回调
        if (this.onSessionChange) {
            this.onSessionChange(sessionData);
        }
    };

    /**
     * 处理会话变更（防抖版本）
     */
    SessionManager.prototype.handleSessionChange = function(sessionData) {
        if (this._debouncedHandleSessionChange) {
            this._debouncedHandleSessionChange(sessionData);
        } else {
            // 回退到原始方法（防抖未初始化时）
            this._originalHandleSessionChange(sessionData);
        }
    };

    /**
     * 处理历史记录变更（原始版本，供防抖使用）
     */
    SessionManager.prototype._originalHandleHistoryChange = function(history) {
        // 减少重复日志：只在历史记录数量变化时记录
        if (!this._lastHistoryCount || this._lastHistoryCount !== history.length) {
            console.log('📋 处理历史记录变更:', history.length, '个会话');
            this._lastHistoryCount = history.length;
        }

        // 更新 UI 渲染
        this.uiRenderer.renderSessionHistory(history);
    };

    /**
     * 处理历史记录变更（防抖版本）
     */
    SessionManager.prototype.handleHistoryChange = function(history) {
        if (this._debouncedHandleHistoryChange) {
            this._debouncedHandleHistoryChange(history);
        } else {
            // 回退到原始方法（防抖未初始化时）
            this._originalHandleHistoryChange(history);
        }
    };

    /**
     * 处理统计资讯变更（原始版本，供防抖使用）
     */
    SessionManager.prototype._originalHandleStatsChange = function(stats) {
        // 减少重复日志：只在统计资讯有意义变化时记录
        const statsKey = stats ? JSON.stringify(stats) : null;
        if (!this._lastStatsKey || this._lastStatsKey !== statsKey) {
            console.log('📋 处理统计资讯变更:', stats);
            this._lastStatsKey = statsKey;
        }

        // 更新 UI 渲染
        this.uiRenderer.renderStats(stats);
    };

    /**
     * 处理统计资讯变更（防抖版本）
     */
    SessionManager.prototype.handleStatsChange = function(stats) {
        if (this._debouncedHandleStatsChange) {
            this._debouncedHandleStatsChange(stats);
        } else {
            // 回退到原始方法（防抖未初始化时）
            this._originalHandleStatsChange(stats);
        }
    };

    /**
     * 处理资料变更（原始版本，供防抖使用）
     */
    SessionManager.prototype._originalHandleDataChanged = function() {
        console.log('📋 处理资料变更，重新渲染所有内容');

        // 重新渲染所有内容
        const currentSession = this.dataManager.getCurrentSession();
        const history = this.dataManager.getSessionHistory();
        const stats = this.dataManager.getStats();

        this.uiRenderer.renderCurrentSession(currentSession);
        this.uiRenderer.renderSessionHistory(history);
        this.uiRenderer.renderStats(stats);
    };

    /**
     * 处理资料变更（防抖版本）
     */
    SessionManager.prototype.handleDataChanged = function() {
        if (this._debouncedHandleDataChanged) {
            this._debouncedHandleDataChanged();
        } else {
            // 回退到原始方法（防抖未初始化时）
            this._originalHandleDataChanged();
        }
    };

    /**
     * 设置事件监听器
     */
    SessionManager.prototype.setupEventListeners = function() {
        const self = this;
        const DOMUtils = getDOMUtils();



        // 刷新按钮
        const refreshButton = DOMUtils ?
            DOMUtils.safeQuerySelector('#refreshSessions') :
            document.querySelector('#refreshSessions');
        if (refreshButton) {
            refreshButton.addEventListener('click', function() {
                self.refreshSessionData();
            });
        }

        // 详细资讯按钮
        const detailsButton = DOMUtils ?
            DOMUtils.safeQuerySelector('#viewSessionDetails') :
            document.querySelector('#viewSessionDetails');
        if (detailsButton) {
            detailsButton.addEventListener('click', function() {
                self.showSessionDetails();
            });
        }

        // 复制当前会话内容按钮
        const copySessionButton = DOMUtils ?
            DOMUtils.safeQuerySelector('#copyCurrentSessionContent') :
            document.querySelector('#copyCurrentSessionContent');
        if (copySessionButton) {
            copySessionButton.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                self.copyCurrentSessionContent();
            });
        }

        // 复制当前用户内容按钮
        const copyUserButton = DOMUtils ?
            DOMUtils.safeQuerySelector('#copyCurrentUserContent') :
            document.querySelector('#copyCurrentUserContent');
        if (copyUserButton) {
            copyUserButton.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                self.copyCurrentUserContent();
            });
        }

        // 会话历史管理按钮 - 会话管理页签
        // 汇出全部按钮
        const sessionTabExportAllBtn = DOMUtils ?
            DOMUtils.safeQuerySelector('#sessionTabExportAllBtn') :
            document.querySelector('#sessionTabExportAllBtn');
        if (sessionTabExportAllBtn) {
            sessionTabExportAllBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                self.exportSessionHistory();
            });
        }

        // 清空讯息记录按钮
        const sessionTabClearMessagesBtn = DOMUtils ?
            DOMUtils.safeQuerySelector('#sessionTabClearMessagesBtn') :
            document.querySelector('#sessionTabClearMessagesBtn');
        if (sessionTabClearMessagesBtn) {
            sessionTabClearMessagesBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                self.clearUserMessages();
            });
        }

        // 清空所有会话按钮
        const sessionTabClearAllBtn = DOMUtils ?
            DOMUtils.safeQuerySelector('#sessionTabClearAllBtn') :
            document.querySelector('#sessionTabClearAllBtn');
        if (sessionTabClearAllBtn) {
            sessionTabClearAllBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                self.clearSessionHistory();
            });
        }
    };

    /**
     * 更新当前会话（委托给数据管理器）
     */
    SessionManager.prototype.updateCurrentSession = function(sessionData) {
        return this.dataManager.updateCurrentSession(sessionData);
    };

    /**
     * 更新状态资讯（委托给数据管理器）
     */
    SessionManager.prototype.updateStatusInfo = function(statusInfo) {
        return this.dataManager.updateStatusInfo(statusInfo);
    };












    /**
     * 刷新会话数据
     */
    SessionManager.prototype.refreshSessionData = function() {
        if (this.isLoading) return;

        console.log('📋 刷新会话数据');
        this.isLoading = true;

        const self = this;
        // 这里可以发送 WebSocket 请求获取最新数据
        setTimeout(function() {
            self.isLoading = false;
            console.log('📋 会话数据刷新完成');
        }, 1000);
    };

    /**
     * 显示当前会话详情
     */
    SessionManager.prototype.showSessionDetails = function() {
        const currentSession = this.dataManager.getCurrentSession();

        if (!currentSession) {
            const message = window.i18nManager ? 
                window.i18nManager.t('sessionHistory.noActiveSession', '目前没有活跃的会话数据') : 
                '目前没有活跃的会话数据';
            this.showMessage(message, 'warning');
            return;
        }

        this.detailsModal.showSessionDetails(currentSession);
    };



    /**
     * 查看会话详情（通过会话ID）
     */
    SessionManager.prototype.viewSessionDetails = function(sessionId) {
        console.log('📋 查看会话详情:', sessionId);

        const sessionData = this.dataManager.findSessionById(sessionId);

        if (sessionData) {
            this.detailsModal.showSessionDetails(sessionData);
        } else {
            const message = window.i18nManager ? 
                window.i18nManager.t('sessionHistory.sessionNotFound', '找不到会话资料') : 
                '找不到会话资料';
            this.showMessage(message, 'error');
        }
    };



    /**
     * 获取当前会话（便利方法）
     */
    SessionManager.prototype.getCurrentSession = function() {
        return this.dataManager.getCurrentSession();
    };

    /**
     * 获取会话历史（便利方法）
     */
    SessionManager.prototype.getSessionHistory = function() {
        return this.dataManager.getSessionHistory();
    };

    /**
     * 获取统计资讯（便利方法）
     */
    SessionManager.prototype.getStats = function() {
        return this.dataManager.getStats();
    };

    /**
     * 获取当前会话数据（相容性方法）
     */
    SessionManager.prototype.getCurrentSessionData = function() {
        console.log('📋 尝试获取当前会话数据...');

        const currentSession = this.dataManager.getCurrentSession();

        if (currentSession && currentSession.session_id) {
            console.log('📋 从 dataManager 获取数据:', currentSession.session_id);
            return currentSession;
        }

        // 尝试从 app 的 WebSocketManager 获取
        if (window.feedbackApp && window.feedbackApp.webSocketManager) {
            const wsManager = window.feedbackApp.webSocketManager;
            if (wsManager.sessionId) {
                console.log('📋 从 WebSocketManager 获取数据:', wsManager.sessionId);
                return {
                    session_id: wsManager.sessionId,
                    status: this.getCurrentSessionStatus(),
                    created_at: this.getSessionCreatedTime(),
                    project_directory: this.getProjectDirectory(),
                    summary: this.getAISummary()
                };
            }
        }

        // 尝试从 app 的 currentSessionId 获取
        if (window.feedbackApp && window.feedbackApp.currentSessionId) {
            console.log('📋 从 app.currentSessionId 获取数据:', window.feedbackApp.currentSessionId);
            return {
                session_id: window.feedbackApp.currentSessionId,
                status: this.getCurrentSessionStatus(),
                created_at: this.getSessionCreatedTime(),
                project_directory: this.getProjectDirectory(),
                summary: this.getAISummary()
            };
        }

        console.log('📋 无法获取会话数据');
        return null;
    };

    /**
     * 获取会话建立时间
     */
    SessionManager.prototype.getSessionCreatedTime = function() {
        // 尝试从 WebSocketManager 的连线开始时间获取
        if (window.feedbackApp && window.feedbackApp.webSocketManager) {
            const wsManager = window.feedbackApp.webSocketManager;
            if (wsManager.connectionStartTime) {
                return wsManager.connectionStartTime / 1000;
            }
        }

        // 尝试从最后收到的状态更新中获取
        if (this.dataManager && this.dataManager.lastStatusUpdate && this.dataManager.lastStatusUpdate.created_at) {
            return this.dataManager.lastStatusUpdate.created_at;
        }

        // 如果都没有，返回 null
        return null;
    };

    /**
     * 获取当前会话状态
     */
    SessionManager.prototype.getCurrentSessionStatus = function() {
        // 尝试从 UIManager 获取当前状态
        if (window.feedbackApp && window.feedbackApp.uiManager) {
            const currentState = window.feedbackApp.uiManager.getFeedbackState();
            if (currentState) {
                // 将内部状态转换为会话状态
                const stateMap = {
                    'waiting_for_feedback': 'waiting',
                    'processing': 'active',
                    'feedback_submitted': 'feedback_submitted'
                };
                return stateMap[currentState] || currentState;
            }
        }

        // 尝试从最后收到的状态更新中获取
        if (this.dataManager && this.dataManager.lastStatusUpdate && this.dataManager.lastStatusUpdate.status) {
            return this.dataManager.lastStatusUpdate.status;
        }

        // 预设状态
        return 'waiting';
    };

    /**
     * 获取专案目录
     */
    SessionManager.prototype.getProjectDirectory = function() {
        const projectElement = document.querySelector('.session-project');
        if (projectElement) {
            return projectElement.textContent.replace('专案: ', '');
        }

        // 从顶部状态列获取
        const topProjectInfo = document.querySelector('.project-info');
        if (topProjectInfo) {
            return topProjectInfo.textContent.replace('专案目录: ', '');
        }

        return '未知';
    };

    /**
     * 获取 AI 摘要
     */
    SessionManager.prototype.getAISummary = function() {
        const summaryElement = document.querySelector('.session-summary');
        if (summaryElement && summaryElement.textContent !== 'AI 摘要: 载入中...') {
            return summaryElement.textContent.replace('AI 摘要: ', '');
        }

        // 尝试从主要内容区域获取
        const mainSummary = document.querySelector('#combinedSummaryContent');
        if (mainSummary && mainSummary.textContent.trim()) {
            return mainSummary.textContent.trim();
        }

        return '暂无摘要';
    };





    /**
     * 更新显示
     */
    SessionManager.prototype.updateDisplay = function() {
        const currentSession = this.dataManager.getCurrentSession();
        const history = this.dataManager.getSessionHistory();
        const stats = this.dataManager.getStats();

        this.uiRenderer.renderCurrentSession(currentSession);
        this.uiRenderer.renderSessionHistory(history);
        this.uiRenderer.renderStats(stats);
    };

    /**
     * 显示讯息
     */
    SessionManager.prototype.showMessage = function(message, type) {
        if (window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.showMessage) {
            window.MCPFeedback.Utils.showMessage(message, type);
        } else {
            console.log('📋 ' + message);
        }
    };

    /**
     * 汇出会话历史
     */
    SessionManager.prototype.exportSessionHistory = function() {
        if (!this.dataManager) {
            console.error('📋 DataManager 未初始化');
            return;
        }

        try {
            const filename = this.dataManager.exportSessionHistory();

            // 显示成功讯息
            if (window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.showMessage) {
                const message = window.i18nManager ?
                    window.i18nManager.t('sessionHistory.management.exportSuccess') :
                    '会话历史已汇出';
                window.MCPFeedback.Utils.showMessage(message + ': ' + filename, 'success');
            }
        } catch (error) {
            console.error('📋 汇出会话历史失败:', error);
            if (window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.showMessage) {
                const message = window.i18nManager ?
                    window.i18nManager.t('sessionHistory.management.exportFailed', { error: error.message }) :
                    '汇出失败: ' + error.message;
                window.MCPFeedback.Utils.showMessage(message, 'error');
            }
        }
    };

    /**
     * 汇出单一会话
     */
    SessionManager.prototype.exportSingleSession = function(sessionId) {
        if (!this.dataManager) {
            console.error('📋 DataManager 未初始化');
            return;
        }

        try {
            const filename = this.dataManager.exportSingleSession(sessionId);
            if (filename) {
                // 显示成功讯息
                if (window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.showMessage) {
                    const message = window.i18nManager ?
                        window.i18nManager.t('sessionHistory.management.exportSuccess') :
                        '会话已汇出';
                    window.MCPFeedback.Utils.showMessage(message + ': ' + filename, 'success');
                }
            }
        } catch (error) {
            console.error('📋 汇出单一会话失败:', error);
            if (window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.showMessage) {
                const message = window.i18nManager ?
                    window.i18nManager.t('sessionHistory.management.exportFailed', { error: error.message }) :
                    '汇出失败: ' + error.message;
                window.MCPFeedback.Utils.showMessage(message, 'error');
            }
        }
    };

    /**
     * 清空会话历史
     */
    SessionManager.prototype.clearSessionHistory = function() {
        if (!this.dataManager) {
            console.error('📋 DataManager 未初始化');
            return;
        }

        // 确认对话框
        const confirmMessage = window.i18nManager ?
            window.i18nManager.t('sessionHistory.management.confirmClear') :
            '确定要清空所有会话历史吗？';

        if (!confirm(confirmMessage)) {
            return;
        }

        try {
            this.dataManager.clearHistory();

            // 显示成功讯息
            if (window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.showMessage) {
                const message = window.i18nManager ?
                    window.i18nManager.t('sessionHistory.management.clearSuccess') :
                    '会话历史已清空';
                window.MCPFeedback.Utils.showMessage(message, 'success');
            }
        } catch (error) {
            console.error('📋 清空会话历史失败:', error);
            if (window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.showMessage) {
                const errorMessage = window.i18nManager ?
                    window.i18nManager.t('sessionHistory.management.clearFailed', { error: error.message }) :
                    '清空失败: ' + error.message;
                window.MCPFeedback.Utils.showMessage(errorMessage, 'error');
            }
        }
    };

    /**
     * 清空用户讯息记录
     */
    SessionManager.prototype.clearUserMessages = function() {
        if (!this.dataManager) {
            console.error('📋 DataManager 未初始化');
            return;
        }

        const i18n = window.i18nManager;
        const confirmMessage = i18n ?
            i18n.t('sessionHistory.userMessages.confirmClearAll') :
            '确定要清空所有会话的用户讯息记录吗？此操作无法复原。';

        if (!confirm(confirmMessage)) {
            return;
        }

        try {
            const success = this.dataManager.clearAllUserMessages();
            if (success) {
                const successMessage = i18n ?
                    i18n.t('sessionHistory.userMessages.clearSuccess') :
                    '用户讯息记录已清空';
                this.showMessage(successMessage, 'success');
            } else {
                const errorMessage = window.i18nManager ?
                    window.i18nManager.t('sessionHistory.management.clearFailedGeneric', '清空失败') :
                    '清空失败';
                this.showMessage(errorMessage, 'error');
            }
        } catch (error) {
            console.error('📋 清空用户讯息记录失败:', error);
            const errorMessage = window.i18nManager ?
                window.i18nManager.t('sessionHistory.management.clearFailed', { error: error.message }) :
                '清空失败: ' + error.message;
            this.showMessage(errorMessage, 'error');
        }
    };

    /**
     * 清理资源
     */
    SessionManager.prototype.cleanup = function() {
        // 清理子模组
        if (this.dataManager) {
            this.dataManager.cleanup();
            this.dataManager = null;
        }

        if (this.uiRenderer) {
            this.uiRenderer.cleanup();
            this.uiRenderer = null;
        }

        if (this.detailsModal) {
            this.detailsModal.cleanup();
            this.detailsModal = null;
        }



        console.log('📋 SessionManager (重构版) 清理完成');
    };

    // 将 SessionManager 加入命名空间
    window.MCPFeedback.SessionManager = SessionManager;

    // 全域方法供 HTML 调用
    window.MCPFeedback.SessionManager.viewSessionDetails = function(sessionId) {
        console.log('📋 全域查看会话详情:', sessionId);

        // 找到当前的 SessionManager 实例
        if (window.MCPFeedback && window.MCPFeedback.app && window.MCPFeedback.app.sessionManager) {
            const sessionManager = window.MCPFeedback.app.sessionManager;
            sessionManager.viewSessionDetails(sessionId);
        } else {
            // 如果找不到实例，显示错误讯息
            console.warn('找不到 SessionManager 实例');
            if (window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.showMessage) {
                window.MCPFeedback.Utils.showMessage('会话管理器未初始化', 'error');
            }
        }
    };

    /**
     * 复制当前会话内容
     */
    SessionManager.prototype.copyCurrentSessionContent = function() {
        console.log('📋 复制当前会话内容...');

        try {
            const currentSession = this.dataManager.getCurrentSession();
            if (!currentSession) {
                const message = window.i18nManager ?
                    window.i18nManager.t('sessionHistory.currentSession.noData', '没有当前会话数据') :
                    '没有当前会话数据';
                this.showMessage(message, 'error');
                return;
            }

            const content = this.formatCurrentSessionContent(currentSession);
            const successMessage = window.i18nManager ?
                window.i18nManager.t('sessionHistory.currentSession.copySuccess', '当前会话内容已复制到剪贴板') :
                '当前会话内容已复制到剪贴板';
            this.copyToClipboard(content, successMessage);
        } catch (error) {
            console.error('复制当前会话内容失败:', error);
            const message = window.i18nManager ?
                window.i18nManager.t('sessionHistory.currentSession.copyFailed', '复制失败，请重试') :
                '复制失败，请重试';
            this.showMessage(message, 'error');
        }
    };

    /**
     * 复制当前用户发送的内容
     */
    SessionManager.prototype.copyCurrentUserContent = function() {
        console.log('📝 复制当前用户发送的内容...');
        console.log('📝 this.dataManager 存在吗?', !!this.dataManager);

        try {
            if (!this.dataManager) {
                console.log('📝 dataManager 不存在，尝试其他方式获取数据');
                const message = window.i18nManager ?
                    window.i18nManager.t('sessionHistory.currentSession.dataManagerNotInit', '数据管理器未初始化') :
                    '数据管理器未初始化';
                this.showMessage(message, 'error');
                return;
            }

            const currentSession = this.dataManager.getCurrentSession();
            console.log('📝 当前会话数据:', currentSession);

            if (!currentSession) {
                console.log('📝 没有当前会话数据');
                const message = window.i18nManager ?
                    window.i18nManager.t('sessionHistory.currentSession.noData', '当前会话没有数据') :
                    '当前会话没有数据';
                this.showMessage(message, 'warning');
                return;
            }

            console.log('📝 用户消息数组:', currentSession.user_messages);
            console.log('📝 用户消息数组长度:', currentSession.user_messages ? currentSession.user_messages.length : 'undefined');

            if (!currentSession.user_messages || currentSession.user_messages.length === 0) {
                console.log('📝 没有用户消息记录');
                const message = window.i18nManager ?
                    window.i18nManager.t('sessionHistory.currentSession.noUserMessages', '当前会话没有用户消息记录') :
                    '当前会话没有用户消息记录';
                this.showMessage(message, 'warning');
                return;
            }

            // 在这里也添加调试信息
            console.log('📝 准备格式化用户消息，数量:', currentSession.user_messages.length);
            console.log('📝 第一条消息内容:', currentSession.user_messages[0]);

            const content = this.formatCurrentUserContent(currentSession.user_messages);
            console.log('📝 格式化后的内容长度:', content.length);
            console.log('📝 格式化后的内容预览:', content.substring(0, 200));

            const successMessage = window.i18nManager ?
                window.i18nManager.t('sessionHistory.currentSession.userContentCopySuccess', '当前用户内容已复制到剪贴板') :
                '当前用户内容已复制到剪贴板';
            this.copyToClipboard(content, successMessage);
        } catch (error) {
            console.error('📝 复制当前用户内容失败:', error);
            console.error('📝 错误堆栈:', error.stack);
            const message = window.i18nManager ?
                window.i18nManager.t('sessionHistory.currentSession.copyFailed', '复制失败，请重试') :
                '复制失败，请重试';
            this.showMessage(message, 'error');
        }
    };

    /**
     * 格式化当前会话内容
     */
    SessionManager.prototype.formatCurrentSessionContent = function(sessionData) {
        const lines = [];
        lines.push('# MCP Feedback Enhanced - 当前会话内容');
        lines.push('');
        lines.push(`**会话ID**: ${sessionData.session_id || 'N/A'}`);
        lines.push(`**项目目录**: ${sessionData.project_directory || 'N/A'}`);
        lines.push(`**摘要**: ${sessionData.summary || 'N/A'}`);
        lines.push(`**状态**: ${sessionData.status || 'N/A'}`);
        lines.push(`**创建时间**: ${sessionData.created_at || 'N/A'}`);
        lines.push(`**更新时间**: ${sessionData.updated_at || 'N/A'}`);
        lines.push('');

        if (sessionData.user_messages && sessionData.user_messages.length > 0) {
            lines.push('## 用户消息');
            sessionData.user_messages.forEach((msg, index) => {
                lines.push(`### 消息 ${index + 1}`);
                lines.push(msg);
                lines.push('');
            });
        }

        if (sessionData.ai_responses && sessionData.ai_responses.length > 0) {
            lines.push('## AI 响应');
            sessionData.ai_responses.forEach((response, index) => {
                lines.push(`### 响应 ${index + 1}`);
                lines.push(response);
                lines.push('');
            });
        }

        return lines.join('\n');
    };

    /**
     * 格式化当前用户内容
     */
    SessionManager.prototype.formatCurrentUserContent = function(userMessages) {
        const lines = [];
        lines.push('# MCP Feedback Enhanced - 用户发送内容');
        lines.push('');

        userMessages.forEach((msg, index) => {
            lines.push(`## 消息 ${index + 1}`);

            // 调试：输出完整的消息对象
            console.log(`📝 消息 ${index + 1} 完整对象:`, msg);
            console.log(`📝 消息 ${index + 1} 所有属性:`, Object.keys(msg));

            // 添加时间戳信息 - 简化版本，直接使用当前时间
            let timeStr = '未知时间';

            // 检查是否有时间戳字段
            if (msg.timestamp) {
                // 如果时间戳看起来不正常（太小），直接使用当前时间
                if (msg.timestamp < 1000000000) { // 小于2001年的时间戳，可能是相对时间
                    timeStr = new Date().toLocaleString('zh-CN');
                    console.log('📝 时间戳异常，使用当前时间:', msg.timestamp);
                } else {
                    // 正常处理时间戳
                    let timestamp = msg.timestamp;
                    if (timestamp > 1e12) {
                        // 毫秒时间戳
                        timeStr = new Date(timestamp).toLocaleString('zh-CN');
                    } else {
                        // 秒时间戳
                        timeStr = new Date(timestamp * 1000).toLocaleString('zh-CN');
                    }
                }
            } else {
                // 没有时间戳，使用当前时间
                timeStr = new Date().toLocaleString('zh-CN');
                console.log('📝 没有时间戳字段，使用当前时间');
            }

            lines.push(`**时间**: ${timeStr}`);

            // 添加提交方式
            if (msg.submission_method) {
                const methodText = msg.submission_method === 'auto' ? '自动提交' : '手动提交';
                lines.push(`**提交方式**: ${methodText}`);
            }

            // 处理消息内容
            if (msg.content !== undefined) {
                // 完整记录模式 - 显示实际内容
                lines.push(`**内容**: ${msg.content}`);

                // 如果有图片，显示图片数量
                if (msg.images && msg.images.length > 0) {
                    lines.push(`**图片数量**: ${msg.images.length}`);
                }
            } else if (msg.content_length !== undefined) {
                // 基本统计模式 - 显示统计信息
                lines.push(`**内容长度**: ${msg.content_length} 字符`);
                lines.push(`**图片数量**: ${msg.image_count || 0}`);
                lines.push(`**有内容**: ${msg.has_content ? '是' : '否'}`);
            } else if (msg.privacy_note) {
                // 隐私保护模式
                lines.push(`**内容**: [内容记录已停用 - 隐私设置]`);
            } else {
                // 兜底情况 - 尝试显示对象的JSON格式
                lines.push(`**原始数据**: ${JSON.stringify(msg, null, 2)}`);
            }

            lines.push('');
        });

        return lines.join('\n');
    };

    /**
     * 复制到剪贴板
     */
    SessionManager.prototype.copyToClipboard = function(text, successMessage) {
        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(text).then(() => {
                this.showMessage(successMessage, 'success');
            }).catch(err => {
                console.error('复制到剪贴板失败:', err);
                this.fallbackCopyToClipboard(text, successMessage);
            });
        } else {
            this.fallbackCopyToClipboard(text, successMessage);
        }
    };

    /**
     * 降级复制方法
     */
    SessionManager.prototype.fallbackCopyToClipboard = function(text, successMessage) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        try {
            document.execCommand('copy');
            this.showMessage(successMessage, 'success');
        } catch (err) {
            console.error('降级复制失败:', err);
            const message = window.i18nManager ?
                window.i18nManager.t('sessionHistory.currentSession.copyFailedManual', '复制失败，请手动复制') :
                '复制失败，请手动复制';
            this.showMessage(message, 'error');
        } finally {
            document.body.removeChild(textArea);
        }
    };

    /**
     * 显示消息
     */
    SessionManager.prototype.showMessage = function(message, type) {
        if (window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.showMessage) {
            const messageType = type === 'success' ? window.MCPFeedback.Utils.CONSTANTS.MESSAGE_SUCCESS :
                               type === 'warning' ? window.MCPFeedback.Utils.CONSTANTS.MESSAGE_WARNING :
                               window.MCPFeedback.Utils.CONSTANTS.MESSAGE_ERROR;
            window.MCPFeedback.Utils.showMessage(message, messageType);
        } else {
            console.log(`[${type.toUpperCase()}] ${message}`);
        }
    };

    // 全域汇出会话历史方法
    window.MCPFeedback.SessionManager.exportSessionHistory = function() {
        if (window.MCPFeedback && window.MCPFeedback.app && window.MCPFeedback.app.sessionManager) {
            window.MCPFeedback.app.sessionManager.exportSessionHistory();
        } else {
            console.warn('找不到 SessionManager 实例');
        }
    };

    // 全域汇出单一会话方法
    window.MCPFeedback.SessionManager.exportSingleSession = function(sessionId) {
        if (window.MCPFeedback && window.MCPFeedback.app && window.MCPFeedback.app.sessionManager) {
            window.MCPFeedback.app.sessionManager.exportSingleSession(sessionId);
        } else {
            console.warn('找不到 SessionManager 实例');
        }
    };

    // 全域清空会话历史方法
    window.MCPFeedback.SessionManager.clearSessionHistory = function() {
        if (window.MCPFeedback && window.MCPFeedback.app && window.MCPFeedback.app.sessionManager) {
            window.MCPFeedback.app.sessionManager.clearSessionHistory();
        } else {
            console.warn('找不到 SessionManager 实例');
        }
    };

    console.log('✅ SessionManager (重构版) 模组载入完成');

})();
