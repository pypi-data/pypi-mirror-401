/**
 * MCP Feedback Enhanced - 会话数据管理模组
 * ========================================
 * 
 * 负责会话数据的存储、更新和状态管理
 */

(function() {
    'use strict';

    // 确保命名空间存在
    window.MCPFeedback = window.MCPFeedback || {};
    window.MCPFeedback.Session = window.MCPFeedback.Session || {};

    const TimeUtils = window.MCPFeedback.Utils.Time;
    const StatusUtils = window.MCPFeedback.Utils.Status;

    /**
     * 会话数据管理器
     */
    function SessionDataManager(options) {
        options = options || {};

        // 会话数据
        this.currentSession = null;
        this.sessionHistory = [];
        this.lastStatusUpdate = null;

        // 统计数据
        this.sessionStats = {
            todayCount: 0,
            averageDuration: 0
        };

        // 设定管理器
        this.settingsManager = options.settingsManager || null;

        // 回调函数
        this.onSessionChange = options.onSessionChange || null;
        this.onHistoryChange = options.onHistoryChange || null;
        this.onStatsChange = options.onStatsChange || null;
        this.onDataChanged = options.onDataChanged || null;

        // 初始化：载入历史记录并清理过期资料
        // 注意：loadFromServer 是异步的，会在载入完成后自动触发更新
        this.loadFromServer();

        console.log('📊 SessionDataManager 初始化完成');
    }

    /**
     * 更新当前会话
     */
    SessionDataManager.prototype.updateCurrentSession = function(sessionData) {
        console.log('📊 更新当前会话:', sessionData);

        if (this.currentSession && this.currentSession.session_id === sessionData.session_id) {
            // 合并数据，保留重要资讯
            this.currentSession = this.mergeSessionData(this.currentSession, sessionData);
        } else {
            // 新会话或不同会话 ID - 需要处理旧会话
            if (this.currentSession && this.currentSession.session_id) {
                console.log('📊 检测到会话 ID 变更，处理旧会话:', this.currentSession.session_id, '->', sessionData.session_id);

                // 将旧会话加入历史记录，保持其原有状态
                const oldSession = Object.assign({}, this.currentSession);

                // 完全保持旧会话的原有状态，不做任何修改
                // 让服务器端负责状态转换，前端只负责显示
                console.log('📊 保持旧会话的原有状态:', oldSession.status);

                oldSession.completed_at = TimeUtils.getCurrentTimestamp();

                // 计算持续时间
                if (oldSession.created_at && !oldSession.duration) {
                    oldSession.duration = oldSession.completed_at - oldSession.created_at;
                }

                console.log('📊 将旧会话加入历史记录:', oldSession);
                this.addSessionToHistory(oldSession);
            }

            // 设置新会话
            this.currentSession = this.normalizeSessionData(sessionData);
        }

        // 触发回调
        if (this.onSessionChange) {
            this.onSessionChange(this.currentSession);
        }

        return this.currentSession;
    };

    /**
     * 合并会话数据
     */
    SessionDataManager.prototype.mergeSessionData = function(existingData, newData) {
        const merged = Object.assign({}, existingData, newData);

        // 确保重要栏位不会被覆盖为空值
        if (!merged.created_at && existingData.created_at) {
            merged.created_at = existingData.created_at;
        }

        if (!merged.status && existingData.status) {
            merged.status = existingData.status;
        }

        return merged;
    };

    /**
     * 标准化会话数据
     */
    SessionDataManager.prototype.normalizeSessionData = function(sessionData) {
        const normalized = Object.assign({}, sessionData);

        // 补充缺失的时间戳
        if (!normalized.created_at) {
            if (this.lastStatusUpdate && this.lastStatusUpdate.created_at) {
                normalized.created_at = this.lastStatusUpdate.created_at;
            } else {
                normalized.created_at = TimeUtils.getCurrentTimestamp();
            }
        }

        // 补充缺失的状态
        if (!normalized.status) {
            normalized.status = 'waiting';
        }

        // 标准化时间戳
        if (normalized.created_at) {
            normalized.created_at = TimeUtils.normalizeTimestamp(normalized.created_at);
        }

        return normalized;
    };

    /**
     * 更新状态资讯
     */
    SessionDataManager.prototype.updateStatusInfo = function(statusInfo) {
        console.log('📊 更新状态资讯:', statusInfo);

        this.lastStatusUpdate = statusInfo;

        if (statusInfo.session_id || statusInfo.created_at) {
            const sessionData = {
                session_id: statusInfo.session_id || (this.currentSession && this.currentSession.session_id),
                status: statusInfo.status,
                created_at: statusInfo.created_at,
                project_directory: statusInfo.project_directory || this.getProjectDirectory(),
                summary: statusInfo.summary || this.getAISummary()
            };

            // 检查会话是否完成
            if (StatusUtils.isCompletedStatus(statusInfo.status)) {
                this.handleSessionCompleted(sessionData);
            } else {
                this.updateCurrentSession(sessionData);
            }
        }
    };

    /**
     * 处理会话完成
     */
    SessionDataManager.prototype.handleSessionCompleted = function(sessionData) {
        console.log('📊 处理会话完成:', sessionData);

        // 优先使用用户最后互动时间作为完成时间
        if (this.currentSession &&
            this.currentSession.session_id === sessionData.session_id &&
            this.currentSession.last_user_interaction) {
            sessionData.completed_at = this.currentSession.last_user_interaction;
            console.log('📊 使用用户最后互动时间作为完成时间:', sessionData.completed_at);
        } else if (!sessionData.completed_at) {
            sessionData.completed_at = TimeUtils.getCurrentTimestamp();
            console.log('📊 使用当前时间作为完成时间:', sessionData.completed_at);
        }

        // 计算持续时间
        if (sessionData.created_at && !sessionData.duration) {
            sessionData.duration = sessionData.completed_at - sessionData.created_at;
        }

        // 确保包含用户讯息（如果当前会话有的话）
        if (this.currentSession &&
            this.currentSession.session_id === sessionData.session_id &&
            this.currentSession.user_messages) {
            sessionData.user_messages = this.currentSession.user_messages;
            console.log('📊 会话完成时包含', sessionData.user_messages.length, '条用户讯息');
        }

        // 将完成的会话加入历史记录
        this.addSessionToHistory(sessionData);

        // 如果是当前会话完成，保持引用但标记为完成
        if (this.currentSession && this.currentSession.session_id === sessionData.session_id) {
            this.currentSession = Object.assign(this.currentSession, sessionData);
            if (this.onSessionChange) {
                this.onSessionChange(this.currentSession);
            }
        }
    };

    /**
     * 新增会话到历史记录
     */
    SessionDataManager.prototype.addSessionToHistory = function(sessionData) {
        console.log('📊 新增会话到历史记录:', sessionData);

        // 只有已完成的会话才加入历史记录
        if (!StatusUtils.isCompletedStatus(sessionData.status)) {
            console.log('📊 跳过未完成的会话:', sessionData.session_id);
            return false;
        }

        // 新增储存时间戳记
        sessionData.saved_at = TimeUtils.getCurrentTimestamp();

        // 确保 user_messages 阵列存在（向后相容）
        if (!sessionData.user_messages) {
            sessionData.user_messages = [];
        }

        // 避免重复新增
        const existingIndex = this.sessionHistory.findIndex(s => s.session_id === sessionData.session_id);
        if (existingIndex !== -1) {
            // 合并用户讯息记录
            const existingSession = this.sessionHistory[existingIndex];
            if (existingSession.user_messages && sessionData.user_messages) {
                sessionData.user_messages = this.mergeUserMessages(existingSession.user_messages, sessionData.user_messages);
            }
            this.sessionHistory[existingIndex] = sessionData;
        } else {
            this.sessionHistory.unshift(sessionData);
        }

        // 限制历史记录数量
        if (this.sessionHistory.length > 10) {
            this.sessionHistory = this.sessionHistory.slice(0, 10);
        }

        // 保存到伺服器端
        this.saveToServer();

        this.updateStats();

        // 触发回调
        if (this.onHistoryChange) {
            this.onHistoryChange(this.sessionHistory);
        }

        return true;
    };

    /**
     * 合并用户讯息记录
     */
    SessionDataManager.prototype.mergeUserMessages = function(existingMessages, newMessages) {
        const merged = existingMessages.slice(); // 复制现有讯息

        // 新增不重复的讯息（基于时间戳记去重）
        newMessages.forEach(function(newMsg) {
            const exists = merged.some(function(existingMsg) {
                return existingMsg.timestamp === newMsg.timestamp;
            });
            if (!exists) {
                merged.push(newMsg);
            }
        });

        // 按时间戳记排序
        merged.sort(function(a, b) {
            return a.timestamp - b.timestamp;
        });

        return merged;
    };

    /**
     * 新增用户讯息到当前会话
     */
    SessionDataManager.prototype.addUserMessage = function(messageData) {
        console.log('📊 新增用户讯息:', messageData);

        // 检查隐私设定
        if (!this.isUserMessageRecordingEnabled()) {
            console.log('📊 用户讯息记录已停用，跳过记录');
            return false;
        }

        // 检查是否有当前会话
        if (!this.currentSession || !this.currentSession.session_id) {
            console.warn('📊 没有当前会话，无法记录用户讯息');
            return false;
        }

        // 确保当前会话有 user_messages 阵列
        if (!this.currentSession.user_messages) {
            this.currentSession.user_messages = [];
        }

        // 建立用户讯息记录
        const userMessage = this.createUserMessageRecord(messageData);

        // 新增到当前会话
        this.currentSession.user_messages.push(userMessage);

        // 记录用户最后互动时间
        this.currentSession.last_user_interaction = TimeUtils.getCurrentTimestamp();

        // 发送用户消息到服务器端
        this.sendUserMessageToServer(userMessage);

        // 立即保存当前会话到伺服器
        this.saveCurrentSessionToServer();

        console.log('📊 用户讯息已记录到当前会话:', this.currentSession.session_id);
        return true;
    };

    /**
     * 发送用户消息到服务器端
     */
    SessionDataManager.prototype.sendUserMessageToServer = function(userMessage) {
        const lang = window.i18nManager ? window.i18nManager.getCurrentLanguage() : 'zh-TW';
        fetch('/api/add-user-message?lang=' + lang, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userMessage)
        })
        .then(function(response) {
            if (response.ok) {
                console.log('📊 用户消息已发送到服务器端');
            } else {
                console.warn('📊 发送用户消息到服务器端失败:', response.status);
            }
        })
        .catch(function(error) {
            console.warn('📊 发送用户消息到服务器端出错:', error);
        });
    };

    /**
     * 建立用户讯息记录
     */
    SessionDataManager.prototype.createUserMessageRecord = function(messageData) {
        const timestamp = TimeUtils.getCurrentTimestamp();
        const privacyLevel = this.getUserMessagePrivacyLevel();

        const record = {
            timestamp: timestamp,
            submission_method: messageData.submission_method || 'manual',
            type: 'feedback'
        };

        // 根据隐私等级决定记录内容
        if (privacyLevel === 'full') {
            record.content = messageData.content || '';
            record.images = this.processImageDataForRecord(messageData.images || []);
        } else if (privacyLevel === 'basic') {
            record.content_length = (messageData.content || '').length;
            record.image_count = (messageData.images || []).length;
            record.has_content = !!(messageData.content && messageData.content.trim());
        } else if (privacyLevel === 'disabled') {
            // 停用记录时，只记录最基本的时间戳记和提交方式
            record.privacy_note = 'Content recording disabled by user privacy settings';
        }

        return record;
    };

    /**
     * 处理图片资料用于记录
     */
    SessionDataManager.prototype.processImageDataForRecord = function(images) {
        if (!Array.isArray(images)) {
            return [];
        }

        return images.map(function(img) {
            return {
                name: img.name || 'unknown',
                size: img.size || 0,
                type: img.type || 'unknown'
            };
        });
    };

    /**
     * 检查是否启用用户讯息记录
     */
    SessionDataManager.prototype.isUserMessageRecordingEnabled = function() {
        if (!this.settingsManager) {
            return true; // 预设启用
        }

        // 检查总开关
        const recordingEnabled = this.settingsManager.get('userMessageRecordingEnabled', true);
        if (!recordingEnabled) {
            return false;
        }

        // 检查隐私等级（disabled 等级视为停用记录）
        const privacyLevel = this.settingsManager.get('userMessagePrivacyLevel', 'full');
        return privacyLevel !== 'disabled';
    };

    /**
     * 获取用户讯息隐私等级
     */
    SessionDataManager.prototype.getUserMessagePrivacyLevel = function() {
        if (!this.settingsManager) {
            return 'full'; // 预设完整记录
        }
        return this.settingsManager.get('userMessagePrivacyLevel', 'full');
    };

    /**
     * 清空所有会话的用户讯息记录
     */
    SessionDataManager.prototype.clearAllUserMessages = function() {
        console.log('📊 清空所有会话的用户讯息记录...');

        // 清空当前会话的用户讯息
        if (this.currentSession && this.currentSession.user_messages) {
            this.currentSession.user_messages = [];
        }

        // 清空历史会话的用户讯息
        this.sessionHistory.forEach(function(session) {
            if (session.user_messages) {
                session.user_messages = [];
            }
        });

        // 保存到伺服器端
        this.saveToServer();

        console.log('📊 所有用户讯息记录已清空');
        return true;
    };

    /**
     * 清空指定会话的用户讯息记录
     */
    SessionDataManager.prototype.clearSessionUserMessages = function(sessionId) {
        console.log('📊 清空会话用户讯息记录:', sessionId);

        // 查找并清空指定会话的用户讯息
        const session = this.sessionHistory.find(function(s) {
            return s.session_id === sessionId;
        });

        if (session && session.user_messages) {
            session.user_messages = [];
            this.saveToServer();
            console.log('📊 会话用户讯息记录已清空:', sessionId);
            return true;
        }

        console.warn('📊 找不到指定会话或该会话没有用户讯息记录:', sessionId);
        return false;
    };

    /**
     * 获取当前会话
     */
    SessionDataManager.prototype.getCurrentSession = function() {
        return this.currentSession;
    };

    /**
     * 获取会话历史
     */
    SessionDataManager.prototype.getSessionHistory = function() {
        return this.sessionHistory.slice(); // 返回副本
    };

    /**
     * 根据 ID 查找会话（包含完整的用户消息数据）
     */
    SessionDataManager.prototype.findSessionById = function(sessionId) {
        // 先检查当前会话
        if (this.currentSession && this.currentSession.session_id === sessionId) {
            console.log('📊 从当前会话获取数据:', sessionId, '用户消息数量:', this.currentSession.user_messages ? this.currentSession.user_messages.length : 0);
            return this.currentSession;
        }

        // 再检查历史记录
        const historySession = this.sessionHistory.find(s => s.session_id === sessionId);
        if (historySession) {
            console.log('📊 从历史记录获取数据:', sessionId, '用户消息数量:', historySession.user_messages ? historySession.user_messages.length : 0);
            return historySession;
        }

        console.warn('📊 找不到会话:', sessionId);
        return null;
    };

    /**
     * 更新统计资讯
     */
    SessionDataManager.prototype.updateStats = function() {
        // 计算今日会话数
        const todayStart = TimeUtils.getTodayStartTimestamp();
        const todaySessions = this.sessionHistory.filter(function(session) {
            return session.created_at && session.created_at >= todayStart;
        });
        this.sessionStats.todayCount = todaySessions.length;

        // 计算今日平均持续时间
        const todayCompletedSessions = todaySessions.filter(function(s) {
            // 过滤有效的持续时间：大于 0 且小于 24 小时（86400 秒）
            return s.duration && s.duration > 0 && s.duration < 86400;
        });

        if (todayCompletedSessions.length > 0) {
            const totalDuration = todayCompletedSessions.reduce(function(sum, s) {
                // 确保持续时间是合理的数值
                const duration = Math.min(s.duration, 86400); // 最大 24 小时
                return sum + duration;
            }, 0);
            this.sessionStats.averageDuration = Math.round(totalDuration / todayCompletedSessions.length);
        } else {
            this.sessionStats.averageDuration = 0;
        }

        // 触发回调
        if (this.onStatsChange) {
            this.onStatsChange(this.sessionStats);
        }
    };

    /**
     * 获取统计资讯
     */
    SessionDataManager.prototype.getStats = function() {
        return Object.assign({}, this.sessionStats);
    };

    /**
     * 清空会话数据
     */
    SessionDataManager.prototype.clearCurrentSession = function() {
        this.currentSession = null;
        if (this.onSessionChange) {
            this.onSessionChange(null);
        }
    };

    /**
     * 清空历史记录
     */
    SessionDataManager.prototype.clearHistory = function() {
        this.sessionHistory = [];

        // 清空伺服器端资料
        this.clearServerData();

        this.updateStats();
        if (this.onHistoryChange) {
            this.onHistoryChange(this.sessionHistory);
        }
    };

    /**
     * 获取专案目录（辅助方法）
     */
    SessionDataManager.prototype.getProjectDirectory = function() {
        // 尝试从多个来源获取专案目录
        const sources = [
            () => document.querySelector('.session-project')?.textContent?.replace('专案: ', ''),
            () => document.querySelector('.project-info')?.textContent?.replace('专案目录: ', ''),
            () => this.currentSession?.project_directory
        ];

        for (const source of sources) {
            try {
                const result = source();
                if (result && result !== '未知') {
                    return result;
                }
            } catch (error) {
                // 忽略错误，继续尝试下一个来源
            }
        }

        return '未知';
    };

    /**
     * 获取 AI 摘要（辅助方法）
     */
    SessionDataManager.prototype.getAISummary = function() {
        // 尝试从多个来源获取 AI 摘要
        const sources = [
            () => {
                const element = document.querySelector('.session-summary');
                const text = element?.textContent;
                return text && text !== 'AI 摘要: 载入中...' ? text.replace('AI 摘要: ', '') : null;
            },
            () => {
                const element = document.querySelector('#combinedSummaryContent');
                return element?.textContent?.trim();
            },
            () => this.currentSession?.summary
        ];

        for (const source of sources) {
            try {
                const result = source();
                if (result && result !== '暂无摘要') {
                    return result;
                }
            } catch (error) {
                // 忽略错误，继续尝试下一个来源
            }
        }

        return '暂无摘要';
    };

    /**
     * 从伺服器载入会话历史（包含实时状态）
     */
    SessionDataManager.prototype.loadFromServer = function() {
        const self = this;

        // 首先尝试获取实时会话状态
        const lang = window.i18nManager ? window.i18nManager.getCurrentLanguage() : 'zh-TW';
        fetch('/api/all-sessions?lang=' + lang)
            .then(function(response) {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('获取实时会话状态失败: ' + response.status);
                }
            })
            .then(function(data) {
                if (data && Array.isArray(data.sessions)) {
                    // 使用实时会话状态
                    self.sessionHistory = data.sessions;
                    console.log('📊 从伺服器载入', self.sessionHistory.length, '个实时会话状态');

                    // 载入完成后进行清理和统计更新
                    self.cleanupExpiredSessions();
                    self.updateStats();

                    // 触发历史记录变更回调
                    if (self.onHistoryChange) {
                        self.onHistoryChange(self.sessionHistory);
                    }

                    // 触发资料变更回调
                    if (self.onDataChanged) {
                        self.onDataChanged();
                    }
                } else {
                    console.warn('📊 实时会话状态回应格式错误，回退到历史文件');
                    self.loadFromHistoryFile();
                }
            })
            .catch(function(error) {
                console.warn('📊 获取实时会话状态失败，回退到历史文件:', error);
                self.loadFromHistoryFile();
            });
    };

    /**
     * 从历史文件载入会话数据（备用方案）
     */
    SessionDataManager.prototype.loadFromHistoryFile = function() {
        const self = this;

        const lang = window.i18nManager ? window.i18nManager.getCurrentLanguage() : 'zh-TW';
        fetch('/api/load-session-history?lang=' + lang)
            .then(function(response) {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('伺服器回应错误: ' + response.status);
                }
            })
            .then(function(data) {
                if (data && Array.isArray(data.sessions)) {
                    self.sessionHistory = data.sessions;
                    console.log('📊 从历史文件载入', self.sessionHistory.length, '个会话');

                    // 载入完成后进行清理和统计更新
                    self.cleanupExpiredSessions();
                    self.updateStats();

                    // 触发历史记录变更回调
                    if (self.onHistoryChange) {
                        self.onHistoryChange(self.sessionHistory);
                    }

                    // 触发资料变更回调
                    if (self.onDataChanged) {
                        self.onDataChanged();
                    }
                } else {
                    console.warn('📊 历史文件回应格式错误:', data);
                    self.sessionHistory = [];
                    self.updateStats();

                    if (self.onHistoryChange) {
                        self.onHistoryChange(self.sessionHistory);
                    }

                    if (self.onDataChanged) {
                        self.onDataChanged();
                    }
                }
            })
            .catch(function(error) {
                console.warn('📊 从历史文件载入失败:', error);
                self.sessionHistory = [];
                self.updateStats();

                if (self.onHistoryChange) {
                    self.onHistoryChange(self.sessionHistory);
                }

                if (self.onDataChanged) {
                    self.onDataChanged();
                }
            });
    };

    /**
     * 立即保存当前会话到伺服器
     */
    SessionDataManager.prototype.saveCurrentSessionToServer = function() {
        if (!this.currentSession) {
            console.log('📊 没有当前会话，跳过即时保存');
            return;
        }

        console.log('📊 立即保存当前会话到伺服器:', this.currentSession.session_id);

        // 建立当前会话的快照（包含用户讯息）
        const sessionSnapshot = Object.assign({}, this.currentSession);

        // 确保快照包含在历史记录中（用于即时保存）
        const updatedHistory = this.sessionHistory.slice();
        const existingIndex = updatedHistory.findIndex(s => s.session_id === sessionSnapshot.session_id);

        if (existingIndex !== -1) {
            // 更新现有会话，保留用户讯息
            const existingSession = updatedHistory[existingIndex];
            if (existingSession.user_messages && sessionSnapshot.user_messages) {
                sessionSnapshot.user_messages = this.mergeUserMessages(existingSession.user_messages, sessionSnapshot.user_messages);
            }
            updatedHistory[existingIndex] = sessionSnapshot;
        } else {
            // 新增会话快照到历史记录开头
            updatedHistory.unshift(sessionSnapshot);
        }

        // 保存包含当前会话的历史记录
        this.saveSessionSnapshot(updatedHistory);
    };

    /**
     * 保存会话快照到伺服器
     */
    SessionDataManager.prototype.saveSessionSnapshot = function(sessions) {
        const data = {
            sessions: sessions,
            lastCleanup: TimeUtils.getCurrentTimestamp()
        };

        const lang = window.i18nManager ? window.i18nManager.getCurrentLanguage() : 'zh-TW';
        fetch('/api/save-session-history?lang=' + lang, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(function(response) {
            if (response.ok) {
                console.log('📊 已保存会话快照到伺服器，包含', data.sessions.length, '个会话');
                return response.json();
            } else {
                throw new Error('伺服器回应错误: ' + response.status);
            }
        })
        .then(function(result) {
            if (result.messageCode && window.i18nManager) {
                const message = window.i18nManager.t(result.messageCode, result.params);
                console.log('📊 会话快照保存回应:', message);
            } else {
                console.log('📊 会话快照保存回应:', result.message);
            }
        })
        .catch(function(error) {
            console.error('📊 保存会话快照到伺服器失败:', error);
        });
    };

    /**
     * 保存会话历史到伺服器
     */
    SessionDataManager.prototype.saveToServer = function() {
        const data = {
            sessions: this.sessionHistory,
            lastCleanup: TimeUtils.getCurrentTimestamp()
        };

        const lang = window.i18nManager ? window.i18nManager.getCurrentLanguage() : 'zh-TW';
        fetch('/api/save-session-history?lang=' + lang, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(function(response) {
            if (response.ok) {
                console.log('📊 已保存', data.sessions.length, '个会话到伺服器');
                return response.json();
            } else {
                throw new Error('伺服器回应错误: ' + response.status);
            }
        })
        .then(function(result) {
            if (result.messageCode && window.i18nManager) {
                const message = window.i18nManager.t(result.messageCode, result.params);
                console.log('📊 伺服器保存回应:', message);
            } else {
                console.log('📊 伺服器保存回应:', result.message);
            }
        })
        .catch(function(error) {
            console.error('📊 保存会话历史到伺服器失败:', error);
        });
    };

    /**
     * 清空伺服器端的会话历史
     */
    SessionDataManager.prototype.clearServerData = function() {
        const emptyData = {
            sessions: [],
            lastCleanup: TimeUtils.getCurrentTimestamp()
        };

        fetch('/api/save-session-history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(emptyData)
        })
        .then(function(response) {
            if (response.ok) {
                console.log('📊 已清空伺服器端的会话历史');
            } else {
                throw new Error('伺服器回应错误: ' + response.status);
            }
        })
        .catch(function(error) {
            console.error('📊 清空伺服器端会话历史失败:', error);
        });
    };



    /**
     * 清理过期的会话
     */
    SessionDataManager.prototype.cleanupExpiredSessions = function() {
        if (!this.settingsManager) {
            return;
        }

        const retentionHours = this.settingsManager.get('sessionHistoryRetentionHours', 72);
        const retentionMs = retentionHours * 60 * 60 * 1000;
        const now = TimeUtils.getCurrentTimestamp();

        const originalCount = this.sessionHistory.length;
        this.sessionHistory = this.sessionHistory.filter(function(session) {
            const sessionAge = now - (session.saved_at || session.completed_at || session.created_at || 0);
            return sessionAge < retentionMs;
        });

        const cleanedCount = originalCount - this.sessionHistory.length;
        if (cleanedCount > 0) {
            console.log('📊 清理了', cleanedCount, '个过期会话');
            this.saveToServer();
        }
    };

    /**
     * 检查会话是否过期
     */
    SessionDataManager.prototype.isSessionExpired = function(session) {
        if (!this.settingsManager) {
            return false;
        }

        const retentionHours = this.settingsManager.get('sessionHistoryRetentionHours', 72);
        const retentionMs = retentionHours * 60 * 60 * 1000;
        const now = TimeUtils.getCurrentTimestamp();
        const sessionTime = session.saved_at || session.completed_at || session.created_at || 0;

        return (now - sessionTime) > retentionMs;
    };

    /**
     * 汇出会话历史
     */
    SessionDataManager.prototype.exportSessionHistory = function() {
        const self = this;
        const exportData = {
            exportedAt: new Date().toISOString(),
            sessionCount: this.sessionHistory.length,
            sessions: this.sessionHistory.map(function(session) {
                const sessionData = {
                    session_id: session.session_id,
                    created_at: session.created_at,
                    completed_at: session.completed_at,
                    duration: session.duration,
                    status: session.status,
                    project_directory: session.project_directory,
                    ai_summary: session.summary || session.ai_summary,
                    saved_at: session.saved_at
                };

                // 包含用户讯息记录（如果存在且允许汇出）
                if (session.user_messages && self.isUserMessageRecordingEnabled()) {
                    sessionData.user_messages = session.user_messages;
                    sessionData.user_message_count = session.user_messages.length;
                }

                return sessionData;
            })
        };

        const filename = 'session-history-' + new Date().toISOString().split('T')[0] + '.json';
        this.downloadJSON(exportData, filename);

        console.log('📊 汇出了', this.sessionHistory.length, '个会话');
        return filename;
    };

    /**
     * 汇出单一会话
     */
    SessionDataManager.prototype.exportSingleSession = function(sessionId) {
        const session = this.sessionHistory.find(function(s) {
            return s.session_id === sessionId;
        });

        if (!session) {
            console.error('📊 找不到会话:', sessionId);
            return null;
        }

        const sessionData = {
            session_id: session.session_id,
            created_at: session.created_at,
            completed_at: session.completed_at,
            duration: session.duration,
            status: session.status,
            project_directory: session.project_directory,
            ai_summary: session.summary || session.ai_summary,
            saved_at: session.saved_at
        };

        // 包含用户讯息记录（如果存在且允许汇出）
        if (session.user_messages && this.isUserMessageRecordingEnabled()) {
            sessionData.user_messages = session.user_messages;
            sessionData.user_message_count = session.user_messages.length;
        }

        const exportData = {
            exportedAt: new Date().toISOString(),
            session: sessionData
        };

        const shortId = sessionId.substring(0, 8);
        const filename = 'session-' + shortId + '-' + new Date().toISOString().split('T')[0] + '.json';
        this.downloadJSON(exportData, filename);

        console.log('📊 汇出会话:', sessionId);
        return filename;
    };

    /**
     * 下载 JSON 档案
     */
    SessionDataManager.prototype.downloadJSON = function(data, filename) {
        try {
            const jsonString = JSON.stringify(data, null, 2);
            const blob = new Blob([jsonString], { type: 'application/json' });
            const url = URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } catch (error) {
            console.error('📊 下载档案失败:', error);
        }
    };

    /**
     * 清理资源
     */
    SessionDataManager.prototype.cleanup = function() {
        this.currentSession = null;
        this.sessionHistory = [];
        this.lastStatusUpdate = null;
        this.sessionStats = {
            todayCount: 0,
            averageDuration: 0
        };

        console.log('📊 SessionDataManager 清理完成');
    };

    // 将 SessionDataManager 加入命名空间
    window.MCPFeedback.Session.DataManager = SessionDataManager;

    console.log('✅ SessionDataManager 模组载入完成');

})();
