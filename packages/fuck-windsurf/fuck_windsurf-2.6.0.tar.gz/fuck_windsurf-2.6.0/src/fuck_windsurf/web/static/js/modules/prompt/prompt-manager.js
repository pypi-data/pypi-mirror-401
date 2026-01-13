/**
 * MCP Feedback Enhanced - 提示词管理模组
 * =====================================
 * 
 * 处理常用提示词的储存、管理和操作
 */

(function() {
    'use strict';

    // 确保命名空间和依赖存在
    window.MCPFeedback = window.MCPFeedback || {};
    window.MCPFeedback.Prompt = window.MCPFeedback.Prompt || {};
    const Utils = window.MCPFeedback.Utils;

    /**
     * 提示词管理器建构函数
     */
    function PromptManager(options) {
        options = options || {};
        
        // 设定管理器引用
        this.settingsManager = options.settingsManager || null;
        
        // 预设提示词设定
        this.defaultPromptSettings = {
            prompts: [],
            lastUsedPromptId: null,
            promptCounter: 0
        };
        
        // 当前提示词设定
        this.currentPromptSettings = Utils.deepClone(this.defaultPromptSettings);
        
        // 回调函数列表
        this.onPromptsChangeCallbacks = [];
        this.onLastUsedChangeCallbacks = [];

        // 向后相容的单一回调
        if (options.onPromptsChange) {
            this.onPromptsChangeCallbacks.push(options.onPromptsChange);
        }
        if (options.onLastUsedChange) {
            this.onLastUsedChangeCallbacks.push(options.onLastUsedChange);
        }
        
        console.log('✅ PromptManager 初始化完成');
    }

    /**
     * 初始化提示词管理器
     */
    PromptManager.prototype.init = function() {
        if (this.settingsManager) {
            // 从设定管理器载入提示词资料
            this.loadFromSettings();
        }

        console.log('📋 PromptManager 初始化完成，提示词数量:', this.currentPromptSettings.prompts.length);
        return this;
    };

    /**
     * 添加提示词变更回调
     */
    PromptManager.prototype.addPromptsChangeCallback = function(callback) {
        if (typeof callback === 'function') {
            this.onPromptsChangeCallbacks.push(callback);
        }
    };

    /**
     * 添加最近使用变更回调
     */
    PromptManager.prototype.addLastUsedChangeCallback = function(callback) {
        if (typeof callback === 'function') {
            this.onLastUsedChangeCallbacks.push(callback);
        }
    };

    /**
     * 触发提示词变更回调
     */
    PromptManager.prototype.triggerPromptsChangeCallbacks = function() {
        const prompts = this.currentPromptSettings.prompts;
        this.onPromptsChangeCallbacks.forEach(function(callback) {
            try {
                callback(prompts);
            } catch (error) {
                console.error('❌ 提示词变更回调执行失败:', error);
            }
        });
    };

    /**
     * 触发最近使用变更回调
     */
    PromptManager.prototype.triggerLastUsedChangeCallbacks = function(prompt) {
        this.onLastUsedChangeCallbacks.forEach(function(callback) {
            try {
                callback(prompt);
            } catch (error) {
                console.error('❌ 最近使用变更回调执行失败:', error);
            }
        });
    };

    /**
     * 从设定管理器载入提示词资料
     */
    PromptManager.prototype.loadFromSettings = function() {
        if (!this.settingsManager) {
            console.warn('⚠️ SettingsManager 未设定，无法载入提示词资料');
            return;
        }

        const promptSettings = this.settingsManager.get('promptSettings');
        if (promptSettings) {
            this.currentPromptSettings = this.mergePromptSettings(this.defaultPromptSettings, promptSettings);
            console.log('📥 从设定载入提示词资料:', this.currentPromptSettings.prompts.length, '个提示词');
        }
    };

    /**
     * 储存提示词资料到设定管理器
     */
    PromptManager.prototype.saveToSettings = function() {
        if (!this.settingsManager) {
            console.warn('⚠️ SettingsManager 未设定，无法储存提示词资料');
            return false;
        }

        try {
            this.settingsManager.set('promptSettings', this.currentPromptSettings);
            console.log('💾 提示词资料已储存');
            return true;
        } catch (error) {
            console.error('❌ 储存提示词资料失败:', error);
            return false;
        }
    };

    /**
     * 合并提示词设定
     */
    PromptManager.prototype.mergePromptSettings = function(defaultSettings, userSettings) {
        const merged = Utils.deepClone(defaultSettings);
        
        if (userSettings.prompts && Array.isArray(userSettings.prompts)) {
            merged.prompts = userSettings.prompts;
        }
        
        if (userSettings.lastUsedPromptId) {
            merged.lastUsedPromptId = userSettings.lastUsedPromptId;
        }
        
        if (typeof userSettings.promptCounter === 'number') {
            merged.promptCounter = userSettings.promptCounter;
        }
        
        return merged;
    };

    /**
     * 新增提示词
     */
    PromptManager.prototype.addPrompt = function(name, content) {
        if (!name || !content) {
            throw new Error('提示词名称和内容不能为空');
        }

        // 检查名称是否重复
        if (this.getPromptByName(name)) {
            throw new Error('提示词名称已存在');
        }

        const prompt = {
            id: this.generatePromptId(),
            name: name.trim(),
            content: content.trim(),
            createdAt: new Date().toISOString(),
            lastUsedAt: null,
            isAutoSubmit: false  // 新增：自动提交标记
        };

        this.currentPromptSettings.prompts.push(prompt);
        this.saveToSettings();

        // 触发回调
        this.triggerPromptsChangeCallbacks();

        console.log('➕ 新增提示词:', prompt.name);
        return prompt;
    };

    /**
     * 更新提示词
     */
    PromptManager.prototype.updatePrompt = function(id, name, content) {
        if (!name || !content) {
            throw new Error('提示词名称和内容不能为空');
        }

        const prompt = this.getPromptById(id);
        if (!prompt) {
            throw new Error('找不到指定的提示词');
        }

        // 检查名称是否与其他提示词重复
        const existingPrompt = this.getPromptByName(name);
        if (existingPrompt && existingPrompt.id !== id) {
            throw new Error('提示词名称已存在');
        }

        prompt.name = name.trim();
        prompt.content = content.trim();

        this.saveToSettings();

        // 触发回调
        this.triggerPromptsChangeCallbacks();

        console.log('✏️ 更新提示词:', prompt.name);
        return prompt;
    };

    /**
     * 删除提示词
     */
    PromptManager.prototype.deletePrompt = function(id) {
        const index = this.currentPromptSettings.prompts.findIndex(p => p.id === id);
        if (index === -1) {
            throw new Error('找不到指定的提示词');
        }

        const prompt = this.currentPromptSettings.prompts[index];
        this.currentPromptSettings.prompts.splice(index, 1);

        // 如果删除的是最近使用的提示词，清除记录
        if (this.currentPromptSettings.lastUsedPromptId === id) {
            this.currentPromptSettings.lastUsedPromptId = null;
        }

        this.saveToSettings();

        // 触发回调
        this.triggerPromptsChangeCallbacks();

        console.log('🗑️ 删除提示词:', prompt.name);
        return prompt;
    };

    /**
     * 使用提示词（更新最近使用记录）
     */
    PromptManager.prototype.usePrompt = function(id) {
        const prompt = this.getPromptById(id);
        if (!prompt) {
            throw new Error('找不到指定的提示词');
        }

        prompt.lastUsedAt = new Date().toISOString();
        this.currentPromptSettings.lastUsedPromptId = id;

        this.saveToSettings();

        // 触发回调
        this.triggerLastUsedChangeCallbacks(prompt);

        console.log('🎯 使用提示词:', prompt.name);
        return prompt;
    };

    /**
     * 获取所有提示词
     */
    PromptManager.prototype.getAllPrompts = function() {
        return [...this.currentPromptSettings.prompts];
    };

    /**
     * 根据 ID 获取提示词
     */
    PromptManager.prototype.getPromptById = function(id) {
        return this.currentPromptSettings.prompts.find(p => p.id === id) || null;
    };

    /**
     * 根据名称获取提示词
     */
    PromptManager.prototype.getPromptByName = function(name) {
        return this.currentPromptSettings.prompts.find(p => p.name === name) || null;
    };

    /**
     * 获取最近使用的提示词
     */
    PromptManager.prototype.getLastUsedPrompt = function() {
        if (!this.currentPromptSettings.lastUsedPromptId) {
            return null;
        }
        return this.getPromptById(this.currentPromptSettings.lastUsedPromptId);
    };

    /**
     * 获取按使用时间排序的提示词列表（自动提交提示词排在最前面）
     */
    PromptManager.prototype.getPromptsSortedByUsage = function() {
        const prompts = [...this.currentPromptSettings.prompts];
        return prompts.sort((a, b) => {
            // 自动提交提示词优先排序
            if (a.isAutoSubmit && !b.isAutoSubmit) return -1;
            if (!a.isAutoSubmit && b.isAutoSubmit) return 1;

            // 其次按最近使用时间排序
            if (!a.lastUsedAt && !b.lastUsedAt) {
                return new Date(b.createdAt) - new Date(a.createdAt);
            }
            if (!a.lastUsedAt) return 1;
            if (!b.lastUsedAt) return -1;
            return new Date(b.lastUsedAt) - new Date(a.lastUsedAt);
        });
    };

    /**
     * 设定提示词为自动提交
     */
    PromptManager.prototype.setAutoSubmitPrompt = function(id) {
        // 先清除所有提示词的自动提交标记
        this.currentPromptSettings.prompts.forEach(prompt => {
            prompt.isAutoSubmit = false;
        });

        // 设定指定提示词为自动提交
        const prompt = this.getPromptById(id);
        if (!prompt) {
            throw new Error('找不到指定的提示词');
        }

        prompt.isAutoSubmit = true;
        this.saveToSettings();

        // 触发回调
        this.triggerPromptsChangeCallbacks();

        console.log('✅ 设定自动提交提示词:', prompt.name);
        return prompt;
    };

    /**
     * 清除自动提交提示词
     */
    PromptManager.prototype.clearAutoSubmitPrompt = function() {
        this.currentPromptSettings.prompts.forEach(prompt => {
            prompt.isAutoSubmit = false;
        });

        this.saveToSettings();

        // 触发回调
        this.triggerPromptsChangeCallbacks();

        console.log('🔄 已清除自动提交提示词');
    };

    /**
     * 获取自动提交提示词
     */
    PromptManager.prototype.getAutoSubmitPrompt = function() {
        return this.currentPromptSettings.prompts.find(prompt => prompt.isAutoSubmit) || null;
    };

    /**
     * 生成提示词 ID
     */
    PromptManager.prototype.generatePromptId = function() {
        this.currentPromptSettings.promptCounter++;
        return 'prompt_' + this.currentPromptSettings.promptCounter + '_' + Date.now();
    };

    /**
     * 重置所有提示词资料
     */
    PromptManager.prototype.resetAllPrompts = function() {
        this.currentPromptSettings = Utils.deepClone(this.defaultPromptSettings);
        this.saveToSettings();

        // 触发回调
        this.triggerPromptsChangeCallbacks();

        console.log('🔄 重置所有提示词资料');
    };

    /**
     * 获取提示词统计资讯
     */
    PromptManager.prototype.getStatistics = function() {
        const prompts = this.currentPromptSettings.prompts;
        const usedPrompts = prompts.filter(p => p.lastUsedAt);
        
        return {
            total: prompts.length,
            used: usedPrompts.length,
            unused: prompts.length - usedPrompts.length,
            lastUsed: this.getLastUsedPrompt()
        };
    };

    // 将 PromptManager 加入命名空间
    window.MCPFeedback.Prompt.PromptManager = PromptManager;

    console.log('✅ PromptManager 模组载入完成');

})();
