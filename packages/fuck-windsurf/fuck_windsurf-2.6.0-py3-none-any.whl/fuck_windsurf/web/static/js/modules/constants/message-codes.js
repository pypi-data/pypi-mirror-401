/**
 * MCP Feedback Enhanced - 讯息代码常量
 * ====================================
 * 
 * 定义所有系统讯息的标准代码，用于国际化支援
 */

(function() {
    'use strict';

    // 确保命名空间存在
    window.MCPFeedback = window.MCPFeedback || {};
    window.MCPFeedback.Constants = window.MCPFeedback.Constants || {};

    /**
     * 讯息代码枚举
     * 所有系统讯息都应该使用这些代码，而非硬编码字串
     */
    const MessageCodes = {
        // 系统状态讯息
        SYSTEM: {
            CONNECTION_ESTABLISHED: 'system.connectionEstablished',
            CONNECTION_LOST: 'system.connectionLost',
            CONNECTION_RECONNECTING: 'system.connectionReconnecting',
            CONNECTION_RECONNECTED: 'system.connectionReconnected',
            CONNECTION_FAILED: 'system.connectionFailed',
            WEBSOCKET_ERROR: 'system.websocketError'
        },

        // 会话相关讯息
        SESSION: {
            NO_ACTIVE_SESSION: 'session.noActiveSession',
            SESSION_CREATED: 'session.created',
            SESSION_UPDATED: 'session.updated',
            SESSION_EXPIRED: 'session.expired',
            SESSION_TIMEOUT: 'session.timeout',
            SESSION_CLEANED: 'session.cleaned',
            FEEDBACK_SUBMITTED: 'session.feedbackSubmitted',
            USER_MESSAGE_RECORDED: 'session.userMessageRecorded',
            HISTORY_SAVED: 'session.historySaved',
            HISTORY_LOADED: 'session.historyLoaded',
            MANUAL_CLEANUP: 'session.manualCleanup',
            ERROR_CLEANUP: 'session.errorCleanup'
        },

        // 设定相关讯息
        SETTINGS: {
            SAVED: 'settings.saved',
            LOADED: 'settings.loaded',
            CLEARED: 'settings.cleared',
            SAVE_FAILED: 'settings.saveFailed',
            LOAD_FAILED: 'settings.loadFailed',
            CLEAR_FAILED: 'settings.clearFailed',
            INVALID_VALUE: 'settings.invalidValue',
            LOG_LEVEL_UPDATED: 'settings.logLevelUpdated',
            INVALID_LOG_LEVEL: 'settings.invalidLogLevel'
        },

        // 通知相关讯息
        NOTIFICATION: {
            AUTOPLAY_BLOCKED: 'notification.autoplayBlocked',
            PERMISSION_DENIED: 'notification.permissionDenied',
            PERMISSION_GRANTED: 'notification.permissionGranted',
            TEST_SENT: 'notification.testSent',
            SOUND_ENABLED: 'notification.soundEnabled',
            SOUND_DISABLED: 'notification.soundDisabled'
        },

        // 档案上传讯息
        FILE: {
            UPLOAD_SUCCESS: 'file.uploadSuccess',
            UPLOAD_FAILED: 'file.uploadFailed',
            SIZE_TOO_LARGE: 'file.sizeTooLarge',
            TYPE_NOT_SUPPORTED: 'file.typeNotSupported',
            PROCESSING: 'file.processing',
            REMOVED: 'file.removed'
        },

        // 提示词相关讯息
        PROMPT: {
            SAVED: 'prompt.saved',
            DELETED: 'prompt.deleted',
            APPLIED: 'prompt.applied',
            IMPORT_SUCCESS: 'prompt.importSuccess',
            IMPORT_FAILED: 'prompt.importFailed',
            EXPORT_SUCCESS: 'prompt.exportSuccess',
            VALIDATION_FAILED: 'prompt.validationFailed'
        },

        // 错误讯息
        ERROR: {
            GENERIC: 'error.generic',
            NETWORK: 'error.network',
            SERVER: 'error.server',
            TIMEOUT: 'error.timeout',
            INVALID_INPUT: 'error.invalidInput',
            OPERATION_FAILED: 'error.operationFailed'
        },

        // 命令执行讯息
        COMMAND: {
            EXECUTING: 'commandStatus.executing',
            COMPLETED: 'commandStatus.completed',
            FAILED: 'commandStatus.failed',
            OUTPUT_RECEIVED: 'commandStatus.outputReceived',
            INVALID_COMMAND: 'commandStatus.invalid',
            ERROR: 'commandStatus.error'
        }
    };

    /**
     * 讯息严重程度
     */
    const MessageSeverity = {
        INFO: 'info',
        SUCCESS: 'success',
        WARNING: 'warning',
        ERROR: 'error'
    };

    /**
     * 建立标准讯息物件
     * @param {string} code - 讯息代码
     * @param {Object} params - 动态参数
     * @param {string} severity - 严重程度
     * @returns {Object} 标准讯息物件
     */
    function createMessage(code, params = {}, severity = MessageSeverity.INFO) {
        return {
            type: 'notification',
            code: code,
            params: params,
            severity: severity,
            timestamp: Date.now()
        };
    }

    /**
     * 快捷方法：建立成功讯息
     */
    function createSuccessMessage(code, params = {}) {
        return createMessage(code, params, MessageSeverity.SUCCESS);
    }

    /**
     * 快捷方法：建立错误讯息
     */
    function createErrorMessage(code, params = {}) {
        return createMessage(code, params, MessageSeverity.ERROR);
    }

    /**
     * 快捷方法：建立警告讯息
     */
    function createWarningMessage(code, params = {}) {
        return createMessage(code, params, MessageSeverity.WARNING);
    }

    // 汇出到全域命名空间
    window.MCPFeedback.Constants.MessageCodes = MessageCodes;
    window.MCPFeedback.Constants.MessageSeverity = MessageSeverity;
    window.MCPFeedback.Constants.createMessage = createMessage;
    window.MCPFeedback.Constants.createSuccessMessage = createSuccessMessage;
    window.MCPFeedback.Constants.createErrorMessage = createErrorMessage;
    window.MCPFeedback.Constants.createWarningMessage = createWarningMessage;

    console.log('📋 讯息代码常量载入完成');
})();