/**
 * MCP Feedback Enhanced - 工具模组
 * ================================
 * 
 * 提供共用的工具函数和常数定义
 */

(function() {
    'use strict';

    // 确保命名空间存在
    window.MCPFeedback = window.MCPFeedback || {};
    window.MCPFeedback.Utils = window.MCPFeedback.Utils || {};

    /**
     * 工具函数模组 - 扩展现有的 Utils 物件
     */
    Object.assign(window.MCPFeedback.Utils, {
        
        /**
         * 格式化档案大小
         * @param {number} bytes - 位元组数
         * @returns {string} 格式化后的档案大小
         */
        formatFileSize: function(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        },

        /**
         * 生成唯一 ID
         * @param {string} prefix - ID 前缀
         * @returns {string} 唯一 ID
         */
        generateId: function(prefix) {
            prefix = prefix || 'id';
            return prefix + '_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        },

        /**
         * 深度复制物件
         * @param {Object} obj - 要复制的物件
         * @returns {Object} 复制后的物件
         */
        deepClone: function(obj) {
            if (obj === null || typeof obj !== 'object') return obj;
            if (obj instanceof Date) return new Date(obj.getTime());
            if (obj instanceof Array) return obj.map(item => this.deepClone(item));
            if (typeof obj === 'object') {
                const clonedObj = {};
                for (const key in obj) {
                    if (obj.hasOwnProperty(key)) {
                        clonedObj[key] = this.deepClone(obj[key]);
                    }
                }
                return clonedObj;
            }
        },

        /**
         * 防抖函数
         * @param {Function} func - 要防抖的函数
         * @param {number} wait - 等待时间（毫秒）
         * @returns {Function} 防抖后的函数
         */
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction() {
                const later = () => {
                    clearTimeout(timeout);
                    func.apply(this, arguments);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        /**
         * 节流函数
         * @param {Function} func - 要节流的函数
         * @param {number} limit - 限制时间（毫秒）
         * @returns {Function} 节流后的函数
         */
        throttle: function(func, limit) {
            let inThrottle;
            return function() {
                const args = arguments;
                const context = this;
                if (!inThrottle) {
                    func.apply(context, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        },

        /**
         * 安全的 JSON 解析
         * @param {string} jsonString - JSON 字串
         * @param {*} defaultValue - 预设值
         * @returns {*} 解析结果或预设值
         */
        safeJsonParse: function(jsonString, defaultValue) {
            try {
                return JSON.parse(jsonString);
            } catch (error) {
                console.warn('JSON 解析失败:', error);
                return defaultValue;
            }
        },

        /**
         * 检查元素是否存在
         * @param {string} selector - CSS 选择器
         * @returns {boolean} 元素是否存在
         */
        elementExists: function(selector) {
            return document.querySelector(selector) !== null;
        },

        /**
         * 从右侧截断路径，保留最后几个目录层级
         * @param {string} path - 完整路径
         * @param {number} maxLevels - 保留的最大目录层级数（默认2）
         * @param {number} maxLength - 最大显示长度（默认40）
         * @returns {object} 包含 truncated（截断后的路径）和 isTruncated（是否被截断）
         */
        truncatePathFromRight: function(path, maxLevels, maxLength) {
            maxLevels = maxLevels || 2;
            maxLength = maxLength || 40;

            if (!path || typeof path !== 'string') {
                return { truncated: path || '', isTruncated: false };
            }

            // 如果路径长度小于最大长度，直接返回
            if (path.length <= maxLength) {
                return { truncated: path, isTruncated: false };
            }

            // 统一路径分隔符为反斜线（Windows风格）
            const normalizedPath = path.replace(/\//g, '\\');

            // 分割路径
            const parts = normalizedPath.split('\\').filter(part => part.length > 0);

            if (parts.length <= maxLevels) {
                return { truncated: normalizedPath, isTruncated: false };
            }

            // 取最后几个层级
            const lastParts = parts.slice(-maxLevels);
            const truncatedPath = '...' + '\\' + lastParts.join('\\');

            return {
                truncated: truncatedPath,
                isTruncated: true
            };
        },

        /**
         * 复制文字到剪贴板（统一的复制功能）
         * @param {string} text - 要复制的文字
         * @param {string} successMessage - 成功提示讯息
         * @param {string} errorMessage - 错误提示讯息
         * @returns {Promise<boolean>} 复制是否成功
         */
        copyToClipboard: function(text, successMessage, errorMessage) {
            successMessage = successMessage || (window.i18nManager ? 
                window.i18nManager.t('utils.copySuccess', '已复制到剪贴板') : 
                '已复制到剪贴板');
            errorMessage = errorMessage || (window.i18nManager ? 
                window.i18nManager.t('utils.copyError', '复制失败') : 
                '复制失败');

            return new Promise(function(resolve) {
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    // 使用现代 Clipboard API
                    navigator.clipboard.writeText(text).then(function() {
                        if (window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.showMessage) {
                            window.MCPFeedback.Utils.showMessage(successMessage, window.MCPFeedback.Utils.CONSTANTS.MESSAGE_SUCCESS);
                        }
                        resolve(true);
                    }).catch(function(err) {
                        console.error('Clipboard API 复制失败:', err);
                        // 回退到旧方法
                        const success = window.MCPFeedback.Utils.fallbackCopyToClipboard(text);
                        if (success) {
                            if (window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.showMessage) {
                                window.MCPFeedback.Utils.showMessage(successMessage, window.MCPFeedback.Utils.CONSTANTS.MESSAGE_SUCCESS);
                            }
                            resolve(true);
                        } else {
                            if (window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.showMessage) {
                                window.MCPFeedback.Utils.showMessage(errorMessage, window.MCPFeedback.Utils.CONSTANTS.MESSAGE_ERROR);
                            }
                            resolve(false);
                        }
                    });
                } else {
                    // 直接使用回退方法
                    const success = window.MCPFeedback.Utils.fallbackCopyToClipboard(text);
                    if (success) {
                        if (window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.showMessage) {
                            window.MCPFeedback.Utils.showMessage(successMessage, window.MCPFeedback.Utils.CONSTANTS.MESSAGE_SUCCESS);
                        }
                        resolve(true);
                    } else {
                        if (window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.showMessage) {
                            window.MCPFeedback.Utils.showMessage(errorMessage, window.MCPFeedback.Utils.CONSTANTS.MESSAGE_ERROR);
                        }
                        resolve(false);
                    }
                }
            });
        },

        /**
         * 回退的复制到剪贴板方法
         * @param {string} text - 要复制的文字
         * @returns {boolean} 复制是否成功
         */
        fallbackCopyToClipboard: function(text) {
            try {
                const textArea = document.createElement('textarea');
                textArea.value = text;
                textArea.style.position = 'fixed';
                textArea.style.left = '-999999px';
                textArea.style.top = '-999999px';
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();

                const successful = document.execCommand('copy');
                document.body.removeChild(textArea);

                return successful;
            } catch (err) {
                console.error('回退复制方法失败:', err);
                return false;
            }
        },

        /**
         * 安全的元素查询
         * @param {string} selector - CSS 选择器
         * @param {Element} context - 查询上下文（可选）
         * @returns {Element|null} 找到的元素或 null
         */
        safeQuerySelector: function(selector, context) {
            try {
                const root = context || document;
                return root.querySelector(selector);
            } catch (error) {
                console.warn('元素查询失败:', selector, error);
                return null;
            }
        },

        /**
         * 显示讯息提示
         * @param {string} message - 讯息内容
         * @param {string} type - 讯息类型 (success, error, warning, info)
         * @param {number} duration - 显示时间（毫秒）
         */
        showMessage: function(messageOrCode, type, duration) {
            // 处理讯息代码物件
            let actualMessage = messageOrCode;
            let actualType = type || 'info';
            
            if (typeof messageOrCode === 'object' && messageOrCode.code) {
                // 使用 i18n 系统翻译讯息代码
                if (window.i18nManager) {
                    actualMessage = window.i18nManager.t(messageOrCode.code, messageOrCode.params);
                } else {
                    // 改善 fallback 机制：提供基本的英文讯息
                    actualMessage = this.getFallbackMessage(messageOrCode.code, messageOrCode.params);
                }
                // 使用讯息物件中的严重程度
                actualType = messageOrCode.severity || type || 'info';
            }
            
            // 呼叫内部显示方法
            return this._displayMessage(actualMessage, actualType, duration);
        },
        
        /**
         * 获取 fallback 讯息
         * 当 i18n 系统尚未载入时使用
         * @param {string} code - 讯息代码
         * @param {Object} params - 参数
         * @returns {string} fallback 讯息
         */
        getFallbackMessage: function(code, params) {
            // 基本的 fallback 讯息对照表
            const fallbackMessages = {
                // 系统相关
                'system.connectionEstablished': 'WebSocket connection established',
                'system.connectionLost': 'WebSocket connection lost',
                'system.connectionReconnecting': 'Reconnecting...',
                'system.connectionReconnected': 'Reconnected',
                'system.connectionFailed': 'Connection failed',
                'system.websocketError': 'WebSocket error',
                'system.websocketReady': 'WebSocket ready',
                'system.memoryPressure': 'Memory pressure cleanup',
                'system.shutdown': 'System shutdown',
                'system.processKilled': 'Process killed',
                'system.heartbeatStopped': 'Heartbeat stopped',
                
                // 会话相关
                'session.noActiveSession': 'No active session',
                'session.created': 'New session created',
                'session.updated': 'Session updated',
                'session.expired': 'Session expired',
                'session.timeout': 'Session timed out',
                'session.cleaned': 'Session cleaned',
                'session.feedbackSubmitted': 'Feedback submitted successfully',
                'session.userMessageRecorded': 'User message recorded',
                'session.historySaved': 'Session history saved',
                'session.historyLoaded': 'Session history loaded',
                
                // 设定相关
                'settings.saved': 'Settings saved',
                'settings.loaded': 'Settings loaded',
                'settings.cleared': 'Settings cleared',
                'settings.saveFailed': 'Save failed',
                'settings.loadFailed': 'Load failed',
                'settings.clearFailed': 'Clear failed',
                'settings.setFailed': 'Set failed',
                'settings.logLevelUpdated': 'Log level updated',
                'settings.invalidLogLevel': 'Invalid log level',
                
                // 错误相关
                'error.generic': 'An error occurred',
                'error.userMessageFailed': 'Failed to add user message',
                'error.getSessionsFailed': 'Failed to get sessions',
                'error.getLogLevelFailed': 'Failed to get log level',
                'error.command': 'Command execution error',
                'error.resourceCleanup': 'Resource cleanup error',
                'error.processing': 'Processing error',
                
                // 通知相关
                'notification.autoplayBlocked': 'Browser blocked autoplay, click page to enable sound',
                
                // 预设讯息
                'default': 'System message'
            };
            
            // 尝试获取对应的 fallback 讯息
            let message = fallbackMessages[code] || fallbackMessages['default'];
            
            // 处理参数替换（简单版本）
            if (params && typeof params === 'object') {
                for (const key in params) {
                    if (params.hasOwnProperty(key)) {
                        const placeholder = '{{' + key + '}}';
                        message = message.replace(placeholder, params[key]);
                    }
                }
            }
            
            // 在开发模式下显示警告
            if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
                console.warn('[i18n] Fallback message used for:', code, '→', message);
            }
            
            return message;
        },
        
        /**
         * 内部方法：实际显示讯息
         * @private
         */
        _displayMessage: function(message, type, duration) {
            type = type || 'info';
            duration = duration || 3000;

            // 创建讯息元素
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message message-' + type;
            messageDiv.style.cssText = `
                position: fixed;
                top: 80px;
                right: 20px;
                z-index: 1001;
                padding: 12px 20px;
                background: var(--${type === 'error' ? 'error' : type === 'warning' ? 'warning' : 'success'}-color, #4CAF50);
                color: white;
                border-radius: 6px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                max-width: 300px;
                word-wrap: break-word;
                transition: opacity 0.3s ease;
            `;
            messageDiv.textContent = message;

            document.body.appendChild(messageDiv);

            // 自动移除
            setTimeout(() => {
                if (messageDiv.parentNode) {
                    messageDiv.style.opacity = '0';
                    setTimeout(() => {
                        if (messageDiv.parentNode) {
                            messageDiv.parentNode.removeChild(messageDiv);
                        }
                    }, 300);
                }
            }, duration);
        },

        /**
         * 检查 WebSocket 是否可用
         * @returns {boolean} WebSocket 是否可用
         */
        isWebSocketSupported: function() {
            return 'WebSocket' in window;
        },



        /**
         * HTML 转义函数
         * @param {string} text - 要转义的文字
         * @returns {string} 转义后的文字
         */
        escapeHtml: function(text) {
            if (typeof text !== 'string') {
                return text;
            }

            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        },

        /**
         * 常数定义
         */
        CONSTANTS: {
            // WebSocket 状态
            WS_CONNECTING: 0,
            WS_OPEN: 1,
            WS_CLOSING: 2,
            WS_CLOSED: 3,

            // 回馈状态
            FEEDBACK_WAITING: 'waiting_for_feedback',
            FEEDBACK_SUBMITTED: 'feedback_submitted',
            FEEDBACK_PROCESSING: 'processing',

            // 预设设定（优化后的值）
            DEFAULT_HEARTBEAT_FREQUENCY: 60000,  // 从 30 秒调整为 60 秒，减少网路负载
            DEFAULT_TAB_HEARTBEAT_FREQUENCY: 10000,  // 从 5 秒调整为 10 秒，减少标签页检查频率
            DEFAULT_RECONNECT_DELAY: 1000,
            MAX_RECONNECT_ATTEMPTS: 5,
            TAB_EXPIRED_THRESHOLD: 60000,  // 从 30 秒调整为 60 秒，与心跳频率保持一致

            // 讯息类型
            MESSAGE_SUCCESS: 'success',
            MESSAGE_ERROR: 'error',
            MESSAGE_WARNING: 'warning',
            MESSAGE_INFO: 'info'
        }
    });

    console.log('✅ Utils 模组载入完成');

})();
