/**
 * 现代化档案上传管理器
 * 使用事件委托模式，避免重复事件监听器问题
 */

(function() {
    'use strict';

    // 确保命名空间存在
    if (!window.MCPFeedback) {
        window.MCPFeedback = {};
    }

    /**
     * 档案上传管理器建构函数
     */
    function FileUploadManager(options) {
        options = options || {};
        
        // 配置选项
        this.maxFileSize = options.maxFileSize || 0; // 0 表示无限制
        this.enableBase64Detail = options.enableBase64Detail || false;
        this.acceptedTypes = options.acceptedTypes || 'image/*';
        this.maxFiles = options.maxFiles || 10;
        
        // 状态管理
        this.files = [];
        this.isInitialized = false;
        this.debounceTimeout = null;
        this.lastClickTime = 0;
        this.isProcessingClick = false;
        this.lastClickTime = 0;
        
        // 事件回调
        this.onFileAdd = options.onFileAdd || null;
        this.onFileRemove = options.onFileRemove || null;
        this.onSettingsChange = options.onSettingsChange || null;
        
        // 绑定方法上下文
        this.handleDelegatedEvent = this.handleDelegatedEvent.bind(this);
        this.handleGlobalPaste = this.handleGlobalPaste.bind(this);
        
        console.log('📁 FileUploadManager 初始化完成');
    }

    /**
     * 初始化档案上传管理器
     */
    FileUploadManager.prototype.initialize = function() {
        if (this.isInitialized) {
            console.warn('⚠️ FileUploadManager 已经初始化过了');
            return;
        }

        this.setupEventDelegation();
        this.setupGlobalPasteHandler();
        this.isInitialized = true;
        
        console.log('✅ FileUploadManager 事件委托设置完成');
    };

    /**
     * 设置事件委托
     * 使用单一事件监听器处理所有档案上传相关事件
     */
    FileUploadManager.prototype.setupEventDelegation = function() {
        // 移除旧的事件监听器
        document.removeEventListener('click', this.handleDelegatedEvent);
        document.removeEventListener('dragover', this.handleDelegatedEvent);
        document.removeEventListener('dragleave', this.handleDelegatedEvent);
        document.removeEventListener('drop', this.handleDelegatedEvent);
        document.removeEventListener('change', this.handleDelegatedEvent);

        // 设置新的事件委托
        document.addEventListener('click', this.handleDelegatedEvent);
        document.addEventListener('dragover', this.handleDelegatedEvent);
        document.addEventListener('dragleave', this.handleDelegatedEvent);
        document.addEventListener('drop', this.handleDelegatedEvent);
        document.addEventListener('change', this.handleDelegatedEvent);
    };

    /**
     * 处理委托事件
     */
    FileUploadManager.prototype.handleDelegatedEvent = function(event) {
        const target = event.target;

        // 处理档案移除按钮点击
        const removeBtn = target.closest('.image-remove-btn');
        if (removeBtn) {
            event.preventDefault();
            event.stopPropagation();
            this.handleRemoveFile(removeBtn);
            return;
        }

        // 处理档案输入变更
        if (target.type === 'file' && event.type === 'change') {
            this.handleFileInputChange(target, event);
            return;
        }

        // 处理上传区域事件 - 只处理直接点击上传区域的情况
        const uploadArea = target.closest('.image-upload-area');
        if (uploadArea && event.type === 'click') {
            // 确保不是点击 input 元素本身
            if (target.type === 'file') {
                return;
            }

            // 确保不是点击预览图片或移除按钮
            if (target.closest('.image-preview-item') || target.closest('.image-remove-btn')) {
                return;
            }

            this.handleUploadAreaClick(uploadArea, event);
            return;
        }

        // 处理拖放事件
        if (uploadArea && (event.type === 'dragover' || event.type === 'dragleave' || event.type === 'drop')) {
            switch (event.type) {
                case 'dragover':
                    this.handleDragOver(uploadArea, event);
                    break;
                case 'dragleave':
                    this.handleDragLeave(uploadArea, event);
                    break;
                case 'drop':
                    this.handleDrop(uploadArea, event);
                    break;
            }
        }
    };

    /**
     * 处理上传区域点击（使用防抖机制）
     */
    FileUploadManager.prototype.handleUploadAreaClick = function(uploadArea, event) {
        event.preventDefault();
        event.stopPropagation();

        // 强力防抖机制 - 防止无限循环
        const now = Date.now();
        if (this.lastClickTime && (now - this.lastClickTime) < 500) {
            console.log('🚫 防抖：忽略重复点击，间隔:', now - this.lastClickTime, 'ms');
            return;
        }
        this.lastClickTime = now;

        // 如果已经有待处理的点击，忽略新的点击
        if (this.isProcessingClick) {
            console.log('🚫 正在处理点击，忽略新的点击');
            return;
        }

        this.isProcessingClick = true;

        const fileInput = uploadArea.querySelector('input[type="file"]');
        if (fileInput) {
            console.log('🖱️ 触发档案选择:', fileInput.id);

            // 重置 input 值以确保可以重复选择同一档案
            fileInput.value = '';

            // 使用 setTimeout 确保在下一个事件循环中执行，避免事件冒泡问题
            const self = this;
            setTimeout(function() {
                try {
                    fileInput.click();
                    console.log('✅ 档案选择对话框已触发');
                } catch (error) {
                    console.error('❌ 档案选择对话框触发失败:', error);
                } finally {
                    // 重置处理状态
                    setTimeout(function() {
                        self.isProcessingClick = false;
                    }, 100);
                }
            }, 50);
        } else {
            this.isProcessingClick = false;
        }
    };

    /**
     * 处理档案输入变更
     */
    FileUploadManager.prototype.handleFileInputChange = function(fileInput, event) {
        const files = event.target.files;
        if (files && files.length > 0) {
            console.log('📁 档案选择变更:', files.length, '个档案');
            this.processFiles(Array.from(files), fileInput);
        }
    };

    /**
     * 处理拖放事件
     */
    FileUploadManager.prototype.handleDragOver = function(uploadArea, event) {
        event.preventDefault();
        uploadArea.classList.add('dragover');
    };

    FileUploadManager.prototype.handleDragLeave = function(uploadArea, event) {
        event.preventDefault();
        // 只有当滑鼠真正离开上传区域时才移除样式
        if (!uploadArea.contains(event.relatedTarget)) {
            uploadArea.classList.remove('dragover');
        }
    };

    FileUploadManager.prototype.handleDrop = function(uploadArea, event) {
        event.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = event.dataTransfer.files;
        if (files && files.length > 0) {
            console.log('📁 拖放档案:', files.length, '个档案');
            this.processFiles(Array.from(files), uploadArea.querySelector('input[type="file"]'));
        }
    };

    /**
     * 处理档案移除
     */
    FileUploadManager.prototype.handleRemoveFile = function(removeBtn) {
        const index = parseInt(removeBtn.dataset.index);
        if (!isNaN(index) && index >= 0 && index < this.files.length) {
            const removedFile = this.files.splice(index, 1)[0];
            console.log('🗑️ 移除档案:', removedFile.name);
            
            this.updateAllPreviews();
            
            if (this.onFileRemove) {
                this.onFileRemove(removedFile, index);
            }
        }
    };

    /**
     * 设置全域剪贴板贴上处理
     */
    FileUploadManager.prototype.setupGlobalPasteHandler = function() {
        document.removeEventListener('paste', this.handleGlobalPaste);
        document.addEventListener('paste', this.handleGlobalPaste);
    };

    /**
     * 处理全域剪贴板贴上
     */
    FileUploadManager.prototype.handleGlobalPaste = function(event) {
        const items = event.clipboardData.items;
        const imageFiles = [];

        for (let i = 0; i < items.length; i++) {
            const item = items[i];
            if (item.type.indexOf('image') !== -1) {
                const file = item.getAsFile();
                if (file) {
                    imageFiles.push(file);
                }
            }
        }

        if (imageFiles.length > 0) {
            event.preventDefault();
            console.log('📋 剪贴板贴上图片:', imageFiles.length, '个档案');
            this.processFiles(imageFiles);
        }
    };

    /**
     * 处理档案
     */
    FileUploadManager.prototype.processFiles = function(files, sourceInput) {
        const validFiles = [];

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            
            // 检查档案类型
            if (!file.type.startsWith('image/')) {
                console.warn('⚠️ 跳过非图片档案:', file.name);
                continue;
            }

            // 检查档案大小
            if (this.maxFileSize > 0 && file.size > this.maxFileSize) {
                const sizeLimit = this.formatFileSize(this.maxFileSize);
                console.warn('⚠️ 档案过大:', file.name, '超过限制', sizeLimit);
                const message = window.i18nManager ?
                    window.i18nManager.t('fileUpload.fileSizeExceeded', {
                        limit: sizeLimit,
                        filename: file.name
                    }) :
                    '图片大小超过限制 (' + sizeLimit + '): ' + file.name;
                this.showMessage(message, 'warning');
                continue;
            }

            // 检查档案数量限制
            if (this.files.length + validFiles.length >= this.maxFiles) {
                console.warn('⚠️ 档案数量超过限制:', this.maxFiles);
                const message = window.i18nManager ?
                    window.i18nManager.t('fileUpload.maxFilesExceeded', { maxFiles: this.maxFiles }) :
                    '最多只能上传 ' + this.maxFiles + ' 个档案';
                this.showMessage(message, 'warning');
                break;
            }

            validFiles.push(file);
        }

        // 处理有效档案
        if (validFiles.length > 0) {
            this.addFiles(validFiles);
        }
    };

    /**
     * 添加档案到列表
     */
    FileUploadManager.prototype.addFiles = function(files) {
        const promises = files.map(file => this.fileToBase64(file));
        
        const self = this;
        Promise.all(promises)
            .then(function(base64Results) {
                base64Results.forEach(function(base64, index) {
                    const file = files[index];
                    const fileData = {
                        name: file.name,
                        size: file.size,
                        type: file.type,
                        data: base64,
                        timestamp: Date.now()
                    };
                    
                    self.files.push(fileData);
                    console.log('✅ 档案已添加:', file.name);
                    
                    if (self.onFileAdd) {
                        self.onFileAdd(fileData);
                    }
                });
                
                self.updateAllPreviews();
            })
            .catch(function(error) {
                console.error('❌ 档案处理失败:', error);
                const message = window.i18nManager ?
                    window.i18nManager.t('fileUpload.processingFailed', '档案处理失败，请重试') :
                    '档案处理失败，请重试';
                self.showMessage(message, 'error');
            });
    };

    /**
     * 将档案转换为 Base64
     */
    FileUploadManager.prototype.fileToBase64 = function(file) {
        return new Promise(function(resolve, reject) {
            const reader = new FileReader();
            reader.onload = function() {
                resolve(reader.result.split(',')[1]);
            };
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    };

    /**
     * 更新所有预览容器
     */
    FileUploadManager.prototype.updateAllPreviews = function() {
        const previewContainers = document.querySelectorAll('.image-preview-container');
        const self = this;

        previewContainers.forEach(function(container) {
            self.updatePreviewContainer(container);
        });

        this.updateFileCount();
        console.log('🖼️ 已更新', previewContainers.length, '个预览容器');
    };

    /**
     * 更新单个预览容器
     */
    FileUploadManager.prototype.updatePreviewContainer = function(container) {
        container.innerHTML = '';

        const self = this;
        this.files.forEach(function(file, index) {
            const previewElement = self.createPreviewElement(file, index);
            container.appendChild(previewElement);
        });
    };

    /**
     * 创建预览元素
     */
    FileUploadManager.prototype.createPreviewElement = function(file, index) {
        const preview = document.createElement('div');
        preview.className = 'image-preview-item';

        // 图片元素
        const img = document.createElement('img');
        img.src = 'data:' + file.type + ';base64,' + file.data;
        img.alt = file.name;
        img.title = file.name + ' (' + this.formatFileSize(file.size) + ')';

        // 档案资讯
        const info = document.createElement('div');
        info.className = 'image-info';

        const name = document.createElement('div');
        name.className = 'image-name';
        name.textContent = file.name;

        const size = document.createElement('div');
        size.className = 'image-size';
        size.textContent = this.formatFileSize(file.size);

        // 移除按钮
        const removeBtn = document.createElement('button');
        removeBtn.className = 'image-remove-btn';
        removeBtn.textContent = '×';
        removeBtn.title = '移除图片';
        removeBtn.dataset.index = index;
        removeBtn.setAttribute('aria-label', '移除图片 ' + file.name);

        // 组装元素
        info.appendChild(name);
        info.appendChild(size);
        preview.appendChild(img);
        preview.appendChild(info);
        preview.appendChild(removeBtn);

        return preview;
    };

    /**
     * 更新档案计数显示
     */
    FileUploadManager.prototype.updateFileCount = function() {
        const count = this.files.length;
        const countElements = document.querySelectorAll('.image-count');

        countElements.forEach(function(element) {
            element.textContent = count > 0 ? '(' + count + ')' : '';
        });

        // 更新上传区域状态
        const uploadAreas = document.querySelectorAll('.image-upload-area');
        uploadAreas.forEach(function(area) {
            if (count > 0) {
                area.classList.add('has-images');
            } else {
                area.classList.remove('has-images');
            }
        });
    };

    /**
     * 格式化档案大小
     */
    FileUploadManager.prototype.formatFileSize = function(bytes) {
        if (bytes === 0) return '0 Bytes';

        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));

        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    /**
     * 显示讯息
     */
    FileUploadManager.prototype.showMessage = function(message, type) {
        // 使用现有的 Utils.showMessage 如果可用
        if (window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.showMessage) {
            const messageType = type === 'warning' ? window.MCPFeedback.Utils.CONSTANTS.MESSAGE_WARNING :
                               type === 'error' ? window.MCPFeedback.Utils.CONSTANTS.MESSAGE_ERROR :
                               window.MCPFeedback.Utils.CONSTANTS.MESSAGE_INFO;
            window.MCPFeedback.Utils.showMessage(message, messageType);
        } else {
            // 后备方案
            console.log('[' + type.toUpperCase() + ']', message);
            alert(message);
        }
    };

    /**
     * 更新设定
     */
    FileUploadManager.prototype.updateSettings = function(settings) {
        this.maxFileSize = settings.imageSizeLimit || 0;
        this.enableBase64Detail = settings.enableBase64Detail || false;

        console.log('⚙️ FileUploadManager 设定已更新:', {
            maxFileSize: this.maxFileSize,
            enableBase64Detail: this.enableBase64Detail
        });
    };

    /**
     * 获取档案列表
     */
    FileUploadManager.prototype.getFiles = function() {
        return this.files.slice(); // 返回副本
    };

    /**
     * 清空所有档案
     */
    FileUploadManager.prototype.clearFiles = function() {
        this.files = [];
        this.updateAllPreviews();
        console.log('🗑️ 已清空所有档案');
    };

    /**
     * 清理资源
     */
    FileUploadManager.prototype.cleanup = function() {
        // 移除事件监听器
        document.removeEventListener('click', this.handleDelegatedEvent);
        document.removeEventListener('dragover', this.handleDelegatedEvent);
        document.removeEventListener('dragleave', this.handleDelegatedEvent);
        document.removeEventListener('drop', this.handleDelegatedEvent);
        document.removeEventListener('change', this.handleDelegatedEvent);
        document.removeEventListener('paste', this.handleGlobalPaste);

        // 清理防抖计时器
        if (this.debounceTimeout) {
            clearTimeout(this.debounceTimeout);
            this.debounceTimeout = null;
        }

        // 清空档案
        this.clearFiles();

        this.isInitialized = false;
        console.log('🧹 FileUploadManager 资源已清理');
    };

    // 将 FileUploadManager 加入命名空间
    window.MCPFeedback.FileUploadManager = FileUploadManager;

    console.log('✅ FileUploadManager 模组载入完成');

})();
