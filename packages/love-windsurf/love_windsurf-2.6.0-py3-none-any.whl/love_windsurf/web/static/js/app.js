/**
 * MCP Feedback Enhanced - 主应用程式
 * =================================
 *
 * 模组化重构版本，整合所有功能模组
 * 依赖模组载入顺序：utils -> tab-manager -> websocket-manager -> connection-monitor ->
 *                  session-manager -> image-handler -> settings-manager -> ui-manager ->
 *                  auto-refresh-manager -> app
 */

(function() {
    'use strict';

    // 确保命名空间存在
    window.MCPFeedback = window.MCPFeedback || {};
    const Utils = window.MCPFeedback.Utils;

    /**
     * 主应用程式建构函数
     */
    function FeedbackApp(sessionId) {
        // 会话信息
        this.sessionId = sessionId;
        this.currentSessionId = null;

        // 模组管理器
        this.tabManager = null;
        this.webSocketManager = null;
        this.connectionMonitor = null;
        this.sessionManager = null;
        this.imageHandler = null;
        this.settingsManager = null;
        this.uiManager = null;

        // 提示词管理器
        this.promptManager = null;
        this.promptModal = null;
        this.promptSettingsUI = null;
        this.promptInputButtons = null;

        // 音效管理器
        this.audioManager = null;
        this.audioSettingsUI = null;

        // 通知管理器
        this.notificationManager = null;
        this.notificationSettings = null;

        // 自动提交管理器
        this.autoSubmitManager = null;

        // 应用程式状态
        this.isInitialized = false;
        this.pendingSubmission = null;

        // 初始化防抖函数
        this.initDebounceHandlers();

        console.log('🚀 FeedbackApp 建构函数初始化完成');
    }

    /**
     * 初始化防抖处理器
     */
    FeedbackApp.prototype.initDebounceHandlers = function() {
        // 为自动提交检查添加防抖
        this._debouncedCheckAndStartAutoSubmit = window.MCPFeedback.Utils.DOM.debounce(
            this._originalCheckAndStartAutoSubmit.bind(this),
            200,
            false
        );

        // 为 WebSocket 讯息处理添加防抖
        this._debouncedHandleWebSocketMessage = window.MCPFeedback.Utils.DOM.debounce(
            this._originalHandleWebSocketMessage.bind(this),
            50,
            false
        );

        // 为会话更新处理添加防抖
        this._debouncedHandleSessionUpdated = window.MCPFeedback.Utils.DOM.debounce(
            this._originalHandleSessionUpdated.bind(this),
            100,
            false
        );

        // 为状态更新处理添加防抖
        this._debouncedHandleStatusUpdate = window.MCPFeedback.Utils.DOM.debounce(
            this._originalHandleStatusUpdate.bind(this),
            100,
            false
        );
    };

    /**
     * 初始化应用程式
     */
    FeedbackApp.prototype.init = function() {
        const self = this;

        console.log('🚀 初始化 MCP Feedback Enhanced 应用程式');

        return new Promise(function(resolve, reject) {
            try {
                // 等待国际化系统
                self.waitForI18n()
                    .then(function() {
                        return self.initializeManagers();
                    })
                    .then(function() {
                        return self.setupEventListeners();
                    })
                    .then(function() {
                        return self.setupCleanupHandlers();
                    })
                    .then(function() {
                        self.isInitialized = true;
                        console.log('✅ MCP Feedback Enhanced 应用程式初始化完成');
                        resolve();
                    })
                    .catch(function(error) {
                        console.error('❌ 应用程式初始化失败:', error);
                        reject(error);
                    });
            } catch (error) {
                console.error('❌ 应用程式初始化异常:', error);
                reject(error);
            }
        });
    };

    /**
     * 等待国际化系统载入
     */
    FeedbackApp.prototype.waitForI18n = function() {
        return new Promise(function(resolve) {
            if (window.i18nManager) {
                window.i18nManager.init().then(resolve).catch(resolve);
            } else {
                resolve();
            }
        });
    };

    /**
     * 初始化所有管理器
     */
    FeedbackApp.prototype.initializeManagers = function() {
        const self = this;

        return new Promise(function(resolve, reject) {
            try {
                console.log('🔧 初始化管理器...');

                // 1. 初始化设定管理器
                self.settingsManager = new window.MCPFeedback.SettingsManager({
                    onSettingsChange: function(settings) {
                        self.handleSettingsChange(settings);
                    },
                    onLanguageChange: function(language) {
                        self.handleLanguageChange(language);
                    },
                    onAutoSubmitStateChange: function(enabled, settings) {
                        self.handleAutoSubmitStateChange(enabled, settings);
                    }
                });

                // 2. 载入设定
                self.settingsManager.loadSettings()
                    .then(function(settings) {
                        console.log('📋 设定载入完成:', settings);

                        // 3. 初始化 UI 管理器
                        self.uiManager = new window.MCPFeedback.UIManager({
                            // 移除 activeTab - 页签切换无需持久化
                            layoutMode: settings.layoutMode,
                            onTabChange: function(tabName) {
                                self.handleTabChange(tabName);
                            },
                            onLayoutModeChange: function(layoutMode) {
                                self.handleLayoutModeChange(layoutMode);
                            }
                        });



                        // 5. 初始化连线监控器
                        self.connectionMonitor = new window.MCPFeedback.ConnectionMonitor({
                            onStatusChange: function(status, message) {
                                console.log('🔍 连线状态变更:', status, message);
                            },
                            onQualityChange: function(quality, latency) {
                                console.log('🔍 连线品质变更:', quality, latency + 'ms');
                            }
                        });

                        // 6. 初始化会话管理器
                        self.sessionManager = new window.MCPFeedback.SessionManager({
                            settingsManager: self.settingsManager,
                            onSessionChange: function(sessionData) {
                                console.log('📋 会话变更:', sessionData);
                            },
                            onSessionSelect: function(sessionId) {
                                console.log('📋 会话选择:', sessionId);
                            }
                        });

                        // 7. 初始化 WebSocket 管理器
                        self.webSocketManager = new window.MCPFeedback.WebSocketManager({
                            tabManager: self.tabManager,
                            connectionMonitor: self.connectionMonitor,
                            onOpen: function() {
                                self.handleWebSocketOpen();
                            },
                            onMessage: function(data) {
                                self.handleWebSocketMessage(data);
                            },
                            onClose: function(event) {
                                self.handleWebSocketClose(event);
                            },
                            onConnectionStatusChange: function(status, text) {
                                self.uiManager.updateConnectionStatus(status, text);
                                // 同时更新连线监控器
                                if (self.connectionMonitor) {
                                    self.connectionMonitor.updateConnectionStatus(status, text);
                                }
                            }
                        });

                        // 8. 初始化图片处理器
                        self.imageHandler = new window.MCPFeedback.ImageHandler({
                            imageSizeLimit: settings.imageSizeLimit,
                            enableBase64Detail: settings.enableBase64Detail,
                            layoutMode: settings.layoutMode,
                            onSettingsChange: function() {
                                self.saveImageSettings();
                            }
                        });

                        // 9. 初始化提示词管理器
                        self.initializePromptManagers();

                        // 10. 初始化音效管理器
                        self.initializeAudioManagers();

                        // 11. 初始化通知管理器
                        self.initializeNotificationManager();

                        // 12. 初始化自动提交管理器
                        self.initializeAutoSubmitManager();

                        // 13. 初始化 Textarea 高度管理器
                        self.initializeTextareaHeightManager();

                        // 14. 应用设定到 UI
                        self.settingsManager.applyToUI();

                        // 15. 初始化各个管理器
                        self.uiManager.initTabs();
                        self.imageHandler.init();

                        // 16. 检查并启动自动提交（如果条件满足）
                        setTimeout(function() {
                            self.checkAndStartAutoSubmit();
                        }, 500); // 延迟 500ms 确保所有初始化完成

                        // 17. 播放启动音效（如果音效已启用）
                        setTimeout(function() {
                            if (self.audioManager) {
                                self.audioManager.playStartupNotification();
                            }
                        }, 800); // 延迟 800ms 确保所有初始化完成且避免与其他音效冲突

                        // 17. 初始化会话超时设定
                        if (self.settingsManager.get('sessionTimeoutEnabled')) {
                            const timeoutSettings = {
                                enabled: self.settingsManager.get('sessionTimeoutEnabled'),
                                seconds: self.settingsManager.get('sessionTimeoutSeconds')
                            };
                            self.webSocketManager.updateSessionTimeoutSettings(timeoutSettings);
                        }

                        // 18. 建立 WebSocket 连接
                        self.webSocketManager.connect();

                        resolve();
                    })
                    .catch(reject);
            } catch (error) {
                reject(error);
            }
        });
    };

    /**
     * 设置事件监听器
     */
    FeedbackApp.prototype.setupEventListeners = function() {
        const self = this;

        return new Promise(function(resolve) {
            // 提交按钮事件
            const submitButtons = [
                window.MCPFeedback.Utils.safeQuerySelector('#submitBtn')
            ].filter(function(btn) { return btn !== null; });

            submitButtons.forEach(function(button) {
                button.addEventListener('click', function() {
                    self.submitFeedback();
                });
            });

            // 取消按钮事件 - 已移除取消按钮，保留 ESC 快捷键功能

            // 命令执行事件
            const runCommandBtn = window.MCPFeedback.Utils.safeQuerySelector('#runCommandBtn');
            if (runCommandBtn) {
                runCommandBtn.addEventListener('click', function() {
                    self.runCommand();
                });
            }

            const commandInput = window.MCPFeedback.Utils.safeQuerySelector('#commandInput');
            if (commandInput) {
                commandInput.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter') {
                        e.preventDefault();
                        self.runCommand();
                    }
                });
            }

            // 复制用户内容按钮
            const copyUserFeedback = window.MCPFeedback.Utils.safeQuerySelector('#copyUserFeedback');
            if (copyUserFeedback) {
                copyUserFeedback.addEventListener('click', function(e) {
                    e.preventDefault();
                    self.copyUserFeedback();
                });
            }

            // 快捷键
            document.addEventListener('keydown', function(e) {
                // Ctrl+Enter 提交回馈
                if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                    e.preventDefault();
                    self.submitFeedback();
                }

                // Ctrl+I 聚焦输入框
                if ((e.ctrlKey || e.metaKey) && e.key === 'i') {
                    e.preventDefault();
                    self.focusInput();
                }

                // ESC 键功能已移除 - 避免意外清空用户输入的文字
            });

            // 倒数计时器暂停/恢复按钮
            const countdownPauseBtn = window.MCPFeedback.Utils.safeQuerySelector('#countdownPauseBtn');
            if (countdownPauseBtn) {
                countdownPauseBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    if (self.autoSubmitManager) {
                        self.autoSubmitManager.togglePause();
                    }
                });
            }

            
            // 自动命令设定相关事件
            self.setupAutoCommandEvents();

            // 设置设定管理器的事件监听器
            self.settingsManager.setupEventListeners();

            // 设置用户活动监听（用于重置会话超时）
            self.setupUserActivityListeners();

            console.log('✅ 事件监听器设置完成');
            resolve();
        });
    };

    /**
     * 设置清理处理器
     */
    FeedbackApp.prototype.setupCleanupHandlers = function() {
        const self = this;

        return new Promise(function(resolve) {
            window.addEventListener('beforeunload', function() {
                self.cleanup();
            });

            console.log('✅ 清理处理器设置完成');
            resolve();
        });
    };

    /**
     * 处理设定变更
     */
    FeedbackApp.prototype.handleSettingsChange = function(settings) {
        console.log('🔧 处理设定变更:', settings);

        // 更新图片处理器设定
        if (this.imageHandler) {
            this.imageHandler.updateSettings(settings);
        }



        // 更新 UI 管理器布局模式
        if (this.uiManager && settings.layoutMode) {
            this.uiManager.applyLayoutMode(settings.layoutMode);
        }
    };

    /**
     * 处理语言变更
     */
    FeedbackApp.prototype.handleLanguageChange = function(language) {
        console.log('🌐 处理语言变更:', language);

        // 更新 UI 显示
        if (this.uiManager) {
            this.uiManager.updateStatusIndicator();
        }


    };

    /**
     * 处理页签变更
     */
    FeedbackApp.prototype.handleTabChange = function(tabName) {
        console.log('📋 处理页签变更:', tabName);

        // 重新初始化图片处理器（确保使用正确的布局模式元素）
        if (this.imageHandler) {
            const layoutMode = this.settingsManager.get('layoutMode');
            this.imageHandler.reinitialize(layoutMode);
        }

        // 移除页签状态保存 - 页签切换无需持久化
        // this.settingsManager.set('activeTab', tabName);
    };

    /**
     * 处理布局模式变更
     */
    FeedbackApp.prototype.handleLayoutModeChange = function(layoutMode) {
        console.log('🎨 处理布局模式变更:', layoutMode);

        // 重新初始化图片处理器
        if (this.imageHandler) {
            this.imageHandler.reinitialize(layoutMode);
        }
    };

    /**
     * 保存图片设定
     */
    FeedbackApp.prototype.saveImageSettings = function() {
        if (this.imageHandler && this.settingsManager) {
            this.settingsManager.setMultiple({
                imageSizeLimit: this.imageHandler.imageSizeLimit,
                enableBase64Detail: this.imageHandler.enableBase64Detail
            });
        }
    };

    /**
     * 初始化提示词管理器
     */
    FeedbackApp.prototype.initializePromptManagers = function() {
        console.log('📝 初始化提示词管理器...');

        try {
            // 检查提示词模组是否已载入
            if (!window.MCPFeedback.Prompt) {
                console.warn('⚠️ 提示词模组未载入，跳过初始化');
                return;
            }

            // 1. 初始化提示词管理器
            this.promptManager = new window.MCPFeedback.Prompt.PromptManager({
                settingsManager: this.settingsManager
            });
            this.promptManager.init();

            // 2. 初始化提示词弹窗
            this.promptModal = new window.MCPFeedback.Prompt.PromptModal();

            // 3. 初始化设定页签 UI
            this.promptSettingsUI = new window.MCPFeedback.Prompt.PromptSettingsUI({
                promptManager: this.promptManager,
                promptModal: this.promptModal,
                settingsManager: this.settingsManager
            });
            this.promptSettingsUI.init('#promptManagementContainer');

            // 4. 初始化输入按钮
            this.promptInputButtons = new window.MCPFeedback.Prompt.PromptInputButtons({
                promptManager: this.promptManager,
                promptModal: this.promptModal
            });

            // 初始化输入按钮到回馈输入区域
            const inputContainers = [
                '#combinedFeedbackText'    // 工作区分页的 textarea
            ];
            this.promptInputButtons.init(inputContainers);

            console.log('✅ 提示词管理器初始化完成');

        } catch (error) {
            console.error('❌ 提示词管理器初始化失败:', error);
        }
    };

    /**
     * 初始化音效管理器
     */
    FeedbackApp.prototype.initializeAudioManagers = function() {
        console.log('🔊 初始化音效管理器...');

        try {
            // 检查音效模组是否已载入
            if (!window.MCPFeedback.AudioManager) {
                console.warn('⚠️ 音效模组未载入，跳过初始化');
                return;
            }

            // 1. 初始化音效管理器
            this.audioManager = new window.MCPFeedback.AudioManager({
                settingsManager: this.settingsManager,
                onSettingsChange: function(settings) {
                    console.log('🔊 音效设定已变更:', settings);
                }
            });
            this.audioManager.initialize();

            // 2. 初始化音效设定 UI
            this.audioSettingsUI = new window.MCPFeedback.AudioSettingsUI({
                container: document.querySelector('#audioManagementContainer'),
                audioManager: this.audioManager,
                t: window.i18nManager ? window.i18nManager.t.bind(window.i18nManager) : function(key, defaultValue) { return defaultValue || key; }
            });
            this.audioSettingsUI.initialize();

            console.log('✅ 音效管理器初始化完成');

        } catch (error) {
            console.error('❌ 音效管理器初始化失败:', error);
        }
    };

    /**
     * 初始化通知管理器
     */
    FeedbackApp.prototype.initializeNotificationManager = function() {
        console.log('🔔 初始化通知管理器...');

        try {
            // 检查通知模组是否已载入
            if (!window.MCPFeedback.NotificationManager) {
                console.warn('⚠️ 通知模组未载入，跳过初始化');
                return;
            }

            // 1. 初始化通知管理器
            this.notificationManager = new window.MCPFeedback.NotificationManager({
                t: window.i18nManager ? window.i18nManager.t.bind(window.i18nManager) : function(key, defaultValue) { return defaultValue || key; }
            });
            this.notificationManager.initialize();

            // 2. 初始化通知设定 UI
            if (window.MCPFeedback.NotificationSettings) {
                const notificationContainer = document.querySelector('#notificationSettingsContainer');
                console.log('🔍 通知设定容器:', notificationContainer);
                
                if (notificationContainer) {
                    this.notificationSettings = new window.MCPFeedback.NotificationSettings({
                        container: notificationContainer,
                        notificationManager: this.notificationManager,
                        t: window.i18nManager ? window.i18nManager.t.bind(window.i18nManager) : function(key, defaultValue) { return defaultValue || key; }
                    });
                    this.notificationSettings.initialize();
                    console.log('✅ 通知设定 UI 初始化完成');
                } else {
                    console.error('❌ 找不到通知设定容器元素 notificationSettingsContainer');
                }
            } else {
                console.warn('⚠️ NotificationSettings 模组未载入');
            }

            console.log('✅ 通知管理器初始化完成');

        } catch (error) {
            console.error('❌ 通知管理器初始化失败:', error);
        }
    };

    /**
     * 初始化 Textarea 高度管理器
     */
    FeedbackApp.prototype.initializeTextareaHeightManager = function() {
        console.log('📏 初始化 Textarea 高度管理器...');

        try {
            // 检查 TextareaHeightManager 模组是否已载入
            if (!window.MCPFeedback.TextareaHeightManager) {
                console.warn('⚠️ TextareaHeightManager 模组未载入，跳过初始化');
                return;
            }

            // 建立 TextareaHeightManager 实例
            this.textareaHeightManager = new window.MCPFeedback.TextareaHeightManager({
                settingsManager: this.settingsManager,
                debounceDelay: 500 // 500ms 防抖延迟
            });

            // 初始化管理器
            this.textareaHeightManager.initialize();

            // 注册 combinedFeedbackText textarea
            const success = this.textareaHeightManager.registerTextarea(
                'combinedFeedbackText',
                'combinedFeedbackTextHeight'
            );

            if (success) {
                console.log('✅ combinedFeedbackText 高度管理已启用');
            } else {
                console.warn('⚠️ combinedFeedbackText 注册失败');
            }

            console.log('✅ Textarea 高度管理器初始化完成');

        } catch (error) {
            console.error('❌ Textarea 高度管理器初始化失败:', error);
        }
    };

    /**
     * 处理 WebSocket 开启
     */
    FeedbackApp.prototype.handleWebSocketOpen = function() {
        console.log('🔗 WebSocket 连接已开启');

        // 如果有待处理的提交，处理它
        if (this.pendingSubmission) {
            console.log('🔄 处理待提交的回馈');
            this.submitFeedbackInternal(this.pendingSubmission);
            this.pendingSubmission = null;
        }
    };

    /**
     * 处理 WebSocket 讯息（原始版本，供防抖使用）
     */
    FeedbackApp.prototype._originalHandleWebSocketMessage = function(data) {
        console.log('📨 处理 WebSocket 讯息:', data);

        switch (data.type) {
            case 'command_output':
                this.appendCommandOutput(data.output);
                break;
            case 'command_complete':
                this.appendCommandOutput('\n[命令完成，退出码: ' + data.exit_code + ']\n');
                this.enableCommandInput();
                break;
            case 'command_error':
                this.appendCommandOutput('\n[错误: ' + data.error + ']\n');
                this.enableCommandInput();
                break;
            case 'feedback_received':
                console.log('回馈已收到');
                this.handleFeedbackReceived(data);
                break;
            case 'status_update':
                console.log('状态更新:', data.status_info);
                this._originalHandleStatusUpdate(data.status_info);
                break;
            case 'session_updated':
                console.log('🔄 收到会话更新讯息:', data.session_info);
                // 处理讯息代码
                if (data.messageCode && window.i18nManager) {
                    const message = window.i18nManager.t(data.messageCode);
                    window.MCPFeedback.Utils.showMessage(message, window.MCPFeedback.Utils.CONSTANTS.MESSAGE_SUCCESS);
                }
                this._originalHandleSessionUpdated(data);
                break;
            case 'desktop_close_request':
                console.log('🖥️ 收到桌面关闭请求');
                this.handleDesktopCloseRequest(data);
                break;
            case 'notification':
                console.log('📢 收到通知:', data);
                // 处理 FEEDBACK_SUBMITTED 通知
                if (data.code === 'session.feedbackSubmitted' || data.code === 'FEEDBACK_SUBMITTED' || data.code === 201) {
                    console.log('✅ 回馈提交成功通知');
                    this.handleFeedbackReceived(data);
                }
                break;
        }
    };

    /**
     * 处理 WebSocket 讯息（防抖版本）
     */
    FeedbackApp.prototype.handleWebSocketMessage = function(data) {
        // 命令输出相关的讯息不应该使用防抖，需要立即处理
        if (data.type === 'command_output' || data.type === 'command_complete' || data.type === 'command_error') {
            this._originalHandleWebSocketMessage(data);
        } else if (this._debouncedHandleWebSocketMessage) {
            // 其他讯息类型使用防抖
            this._debouncedHandleWebSocketMessage(data);
        } else {
            // 回退到原始方法（防抖未初始化时）
            this._originalHandleWebSocketMessage(data);
        }
    };

    /**
     * 处理 WebSocket 关闭
     */
    FeedbackApp.prototype.handleWebSocketClose = function(event) {
        console.log('🔗 WebSocket 连接已关闭');

        // 重置回馈状态，避免卡在处理状态
        if (this.uiManager && this.uiManager.getFeedbackState() === window.MCPFeedback.Utils.CONSTANTS.FEEDBACK_PROCESSING) {
            console.log('🔄 WebSocket 断开，重置处理状态');
            this.uiManager.setFeedbackState(window.MCPFeedback.Utils.CONSTANTS.FEEDBACK_WAITING);
        }
    };

    /**
     * 处理回馈接收
     */
    FeedbackApp.prototype.handleFeedbackReceived = function(data) {
        // 使用 UI 管理器设置状态
        this.uiManager.setFeedbackState(window.MCPFeedback.Utils.CONSTANTS.FEEDBACK_SUBMITTED);
        this.uiManager.setLastSubmissionTime(Date.now());

        // 停止自动提交计时器（如果正在运行）
        if (this.autoSubmitManager && this.autoSubmitManager.isEnabled) {
            console.log('⏸️ 反馈已成功提交，停止自动提交倒数计时器');
            this.autoSubmitManager.stop();
        }

        // 显示成功讯息
        if (data.messageCode && window.i18nManager) {
            const message = window.i18nManager.t(data.messageCode, data.params);
            window.MCPFeedback.Utils.showMessage(message, window.MCPFeedback.Utils.CONSTANTS.MESSAGE_SUCCESS);
        } else {
            const successMessage = window.i18nManager ? window.i18nManager.t('feedback.submitSuccess') : '回馈提交成功！';
            window.MCPFeedback.Utils.showMessage(data.message || successMessage, window.MCPFeedback.Utils.CONSTANTS.MESSAGE_SUCCESS);
        }

        // 更新 AI 摘要区域显示「已送出反馈」状态
        const submittedMessage = window.i18nManager ? window.i18nManager.t('feedback.submittedWaiting') : '已送出反馈，等待下次 MCP 调用...';
        this.updateSummaryStatus(submittedMessage);
        
        // 执行提交回馈后的自动命令
        this.executeAutoCommandOnFeedbackSubmit();

        // 刷新会话列表以显示最新状态
        this.refreshSessionList();

        console.log('反馈已提交，页面保持开启状态');
    };

    /**
     * 刷新会话列表以显示最新状态
     */
    FeedbackApp.prototype.refreshSessionList = function() {
        // 如果有会话管理器，触发数据刷新
        if (this.sessionManager && this.sessionManager.dataManager) {
            console.log('🔄 刷新会话列表以显示最新状态');
            this.sessionManager.dataManager.loadFromServer();
        } else {
            console.log('⚠️ 会话管理器未初始化，跳过会话列表刷新');
        }
    };

    /**
     * 处理桌面关闭请求
     */
    FeedbackApp.prototype.handleDesktopCloseRequest = function(data) {
        console.log('🖥️ 处理桌面关闭请求:', data.message);

        // 显示关闭讯息
        const closeMessage = data.message || '正在关闭桌面应用程式...';
        window.MCPFeedback.Utils.showMessage(closeMessage, window.MCPFeedback.Utils.CONSTANTS.MESSAGE_INFO);

        // 检查是否在 Tauri 环境中
        if (window.__TAURI__) {
            console.log('🖥️ 检测到 Tauri 环境，关闭桌面视窗');
            try {
                // 使用 Tauri API 关闭视窗
                window.__TAURI__.window.getCurrent().close();
            } catch (error) {
                console.error('关闭 Tauri 视窗失败:', error);
                // 备用方案：关闭浏览器视窗
                window.close();
            }
        } else {
            console.log('🖥️ 非 Tauri 环境，尝试关闭浏览器视窗');
            // 在浏览器环境中尝试关闭视窗
            window.close();
        }
    };

    /**
     * 处理会话更新（原始版本，供防抖使用）
     */
    FeedbackApp.prototype._originalHandleSessionUpdated = function(data) {
        console.log('🔄 处理会话更新:', data);
        console.log('🔍 检查 action 字段:', data.action);
        console.log('🔍 检查 type 字段:', data.type);

        // 检查是否是新会话创建的通知
        if (data.action === 'new_session_created' || data.type === 'new_session_created') {
            console.log('🆕 检测到新会话创建，局部更新页面内容');

            // 播放音效通知
            if (this.audioManager) {
                this.audioManager.playNotification();
            }
            
            // 执行新会话自动命令
            this.executeAutoCommandOnNewSession();

            // 发送浏览器通知
            if (this.notificationManager && data.session_info) {
                this.notificationManager.notifyNewSession(
                    data.session_info.session_id,
                    data.session_info.project_directory || data.project_directory || '未知专案'
                );
            }

            // 显示新会话通知
            const defaultMessage = window.i18nManager ? 
                window.i18nManager.t('session.created') : 
                'New MCP session created, page will refresh automatically';
            window.MCPFeedback.Utils.showMessage(
                data.message || defaultMessage,
                window.MCPFeedback.Utils.CONSTANTS.MESSAGE_SUCCESS
            );

            // 局部更新页面内容而非开启新视窗
            const self = this;
            setTimeout(function() {
                console.log('🔄 执行局部更新页面内容');

                // 1. 更新会话资讯
                if (data.session_info) {
                    self.currentSessionId = data.session_info.session_id;
                    console.log('📋 新会话 ID:', self.currentSessionId);
                }

                // 2. 刷新页面内容（AI 摘要、表单等）
                self.refreshPageContent();

                // 3. 重置表单状态
                self.clearFeedback();

                // 4. 重置回馈状态为等待中
                if (self.uiManager) {
                    self.uiManager.setFeedbackState(window.MCPFeedback.Utils.CONSTANTS.FEEDBACK_WAITING, self.currentSessionId);
                }
                
                // 5. 重新启动会话超时计时器（如果已启用）
                if (self.settingsManager && self.settingsManager.get('sessionTimeoutEnabled')) {
                    console.log('🔄 新会话创建，重新启动会话超时计时器');
                    const timeoutSettings = {
                        enabled: self.settingsManager.get('sessionTimeoutEnabled'),
                        seconds: self.settingsManager.get('sessionTimeoutSeconds')
                    };
                    self.webSocketManager.updateSessionTimeoutSettings(timeoutSettings);
                }

                // 6. 检查并启动自动提交
                self.checkAndStartAutoSubmit();

                console.log('✅ 局部更新完成，页面已准备好接收新的回馈');
            }, 500);

            return; // 提前返回，不执行后续的局部更新逻辑
        }

        // 播放音效通知
        if (this.audioManager) {
            this.audioManager.playNotification();
        }

        // 显示更新通知
        window.MCPFeedback.Utils.showMessage(data.message || '会话已更新，正在局部更新内容...', window.MCPFeedback.Utils.CONSTANTS.MESSAGE_SUCCESS);

        // 更新会话信息
        if (data.session_info) {
            const newSessionId = data.session_info.session_id;
            console.log('📋 会话 ID 更新: ' + this.currentSessionId + ' -> ' + newSessionId);

            // 保存旧会话到历史记录（在更新当前会话之前）
            if (this.currentSessionId && this.sessionManager && this.currentSessionId !== newSessionId) {
                console.log('📋 尝试获取当前会话数据...');
                // 从 SessionManager 获取当前会话的完整数据
                const currentSessionData = this.sessionManager.getCurrentSessionData();
                console.log('📋 从 currentSession 获取数据:', this.currentSessionId);

                if (currentSessionData) {
                    // 计算实际持续时间
                    const now = Date.now() / 1000;
                    let duration = 300; // 预设 5 分钟

                    if (currentSessionData.created_at) {
                        let createdAt = currentSessionData.created_at;
                        // 处理时间戳格式
                        if (createdAt > 1e12) {
                            createdAt = createdAt / 1000;
                        }
                        duration = Math.max(1, Math.round(now - createdAt));
                    }

                    const oldSessionData = {
                        session_id: this.currentSessionId,
                        status: 'completed',
                        created_at: currentSessionData.created_at || (now - duration),
                        completed_at: now,
                        duration: duration,
                        project_directory: currentSessionData.project_directory,
                        summary: currentSessionData.summary
                    };

                    console.log('📋 准备将旧会话加入历史记录:', oldSessionData);

                    // 先更新当前会话 ID，再调用 addSessionToHistory
                    this.currentSessionId = newSessionId;

                    // 更新会话管理器的当前会话（这样 addSessionToHistory 检查时就不会认为是当前活跃会话）
                    if (this.sessionManager) {
                        this.sessionManager.updateCurrentSession(data.session_info);
                    }

                    // 现在可以安全地将旧会话加入历史记录
                    this.sessionManager.dataManager.addSessionToHistory(oldSessionData);
                } else {
                    console.log('⚠️ 无法获取当前会话数据，跳过历史记录保存');
                    // 仍然需要更新当前会话 ID
                    this.currentSessionId = newSessionId;
                    // 更新会话管理器
                    if (this.sessionManager) {
                        this.sessionManager.updateCurrentSession(data.session_info);
                    }
                }
            } else {
                // 没有旧会话或会话 ID 相同，直接更新
                this.currentSessionId = newSessionId;
                // 更新会话管理器
                if (this.sessionManager) {
                    this.sessionManager.updateCurrentSession(data.session_info);
                }
            }

            // 检查当前状态，只有在非已提交状态时才重置
            const currentState = this.uiManager.getFeedbackState();
            if (currentState !== window.MCPFeedback.Utils.CONSTANTS.FEEDBACK_SUBMITTED) {
                this.uiManager.setFeedbackState(window.MCPFeedback.Utils.CONSTANTS.FEEDBACK_WAITING, newSessionId);
                console.log('🔄 会话更新：重置回馈状态为等待新回馈');
            } else {
                console.log('🔒 会话更新：保护已提交状态，不重置');
                // 更新会话ID但保持已提交状态
                this.uiManager.setFeedbackState(window.MCPFeedback.Utils.CONSTANTS.FEEDBACK_SUBMITTED, newSessionId);
            }

            // 检查并启动自动提交（如果条件满足）
            const self = this;
            setTimeout(function() {
                self.checkAndStartAutoSubmit();
            }, 200); // 延迟确保状态更新完成

            // 更新页面标题
            if (data.session_info.project_directory) {
                const projectName = data.session_info.project_directory.split(/[/\\]/).pop();
                document.title = 'MCP Feedback - ' + projectName;
            }

            // 使用局部更新替代整页刷新
            this.refreshPageContent();
        } else {
            console.log('⚠️ 会话更新没有包含会话信息，仅重置状态');
            this.uiManager.setFeedbackState(window.MCPFeedback.Utils.CONSTANTS.FEEDBACK_WAITING);
        }

        console.log('✅ 会话更新处理完成');
    };

    /**
     * 处理会话更新（防抖版本）
     */
    FeedbackApp.prototype.handleSessionUpdated = function(data) {
        if (this._debouncedHandleSessionUpdated) {
            this._debouncedHandleSessionUpdated(data);
        } else {
            // 回退到原始方法（防抖未初始化时）
            this._originalHandleSessionUpdated(data);
        }
    };

    /**
     * 处理状态更新（原始版本，供防抖使用）
     */
    FeedbackApp.prototype._originalHandleStatusUpdate = function(statusInfo) {
        console.log('📊 处理状态更新:', statusInfo);

        const sessionId = statusInfo.session_id;
        console.log('🔍 状态更新详情:', {
            currentSessionId: this.currentSessionId,
            newSessionId: sessionId,
            status: statusInfo.status,
            message: statusInfo.message,
            isNewSession: sessionId !== this.currentSessionId
        });

        // 更新 SessionManager 的状态资讯
        if (this.sessionManager && this.sessionManager.updateStatusInfo) {
            this.sessionManager.updateStatusInfo(statusInfo);
        }

        // 更新页面标题显示会话信息
        if (statusInfo.project_directory) {
            const projectName = statusInfo.project_directory.split(/[/\\]/).pop();
            document.title = 'MCP Feedback - ' + projectName;
        }

        // 使用之前已声明的 sessionId

        // 前端只管理会话ID，所有状态都从服务器获取
        console.log('📊 收到服务器状态更新:', statusInfo.status, '会话ID:', sessionId);

        // 更新当前会话ID
        if (sessionId) {
            this.currentSessionId = sessionId;
            console.log('🔄 更新当前会话ID:', sessionId.substring(0, 8) + '...');
        }

        // 刷新会话列表以显示最新状态
        this.refreshSessionList();

        // 根据服务器状态更新消息显示（不修改前端状态）
        switch (statusInfo.status) {
            case 'feedback_submitted':
                const submittedMessage = window.i18nManager ? window.i18nManager.t('feedback.submittedWaiting') : '已送出反馈，等待下次 MCP 调用...';
                this.updateSummaryStatus(submittedMessage);
                break;
            case 'waiting':
                const waitingMessage = window.i18nManager ? window.i18nManager.t('feedback.waitingForUser') : '等待用户回馈...';
                this.updateSummaryStatus(waitingMessage);

                // 检查并启动自动提交（如果条件满足）
                const self = this;
                setTimeout(function() {
                    self.checkAndStartAutoSubmit();
                }, 100);
                break;
            case 'completed':
                const completedMessage = window.i18nManager ? window.i18nManager.t('feedback.completed') : '会话已完成';
                this.updateSummaryStatus(completedMessage);
                break;
        }
    };

    /**
     * 处理状态更新（防抖版本）
     */
    FeedbackApp.prototype.handleStatusUpdate = function(statusInfo) {
        if (this._debouncedHandleStatusUpdate) {
            this._debouncedHandleStatusUpdate(statusInfo);
        } else {
            // 回退到原始方法（防抖未初始化时）
            this._originalHandleStatusUpdate(statusInfo);
        }
    };

    /**
     * 提交回馈
     */
    FeedbackApp.prototype.submitFeedback = function() {
        console.log('📤 尝试提交回馈...');

        // 检查是否可以提交回馈
        if (!this.canSubmitFeedback()) {
            console.log('⚠️ 无法提交回馈');
            this.handleSubmitError();
            return;
        }

        // 收集回馈数据并提交
        const feedbackData = this.collectFeedbackData();
        if (!feedbackData) {
            return;
        }

        this.submitFeedbackInternal(feedbackData);
    };

    /**
     * 检查是否可以提交回馈
     */
    FeedbackApp.prototype.canSubmitFeedback = function() {
        // 简化检查：只检查WebSocket连接，状态由服务器端验证
        const wsReady = this.webSocketManager && this.webSocketManager.isReady();

        console.log('🔍 提交检查:', {
            wsReady: wsReady,
            sessionId: this.currentSessionId
        });

        return wsReady;
    };

    /**
     * 处理提交错误
     */
    FeedbackApp.prototype.handleSubmitError = function() {
        const feedbackState = this.uiManager ? this.uiManager.getFeedbackState() : null;

        if (feedbackState === window.MCPFeedback.Utils.CONSTANTS.FEEDBACK_SUBMITTED) {
            const submittedWarning = window.i18nManager ? window.i18nManager.t('feedback.alreadySubmitted') : '回馈已提交，请等待下次 MCP 调用';
            window.MCPFeedback.Utils.showMessage(submittedWarning, window.MCPFeedback.Utils.CONSTANTS.MESSAGE_WARNING);
        } else if (feedbackState === window.MCPFeedback.Utils.CONSTANTS.FEEDBACK_PROCESSING) {
            const processingWarning = window.i18nManager ? window.i18nManager.t('feedback.processingFeedback') : '正在处理中，请稍候';
            window.MCPFeedback.Utils.showMessage(processingWarning, window.MCPFeedback.Utils.CONSTANTS.MESSAGE_WARNING);
        } else if (!this.webSocketManager || !this.webSocketManager.isReady()) {
            // 收集回馈数据，等待连接就绪后提交
            const feedbackData = this.collectFeedbackData();
            if (feedbackData) {
                this.pendingSubmission = feedbackData;
                const connectingMessage = window.i18nManager ? window.i18nManager.t('feedback.connectingMessage') : 'WebSocket 连接中，回馈将在连接就绪后自动提交...';
                window.MCPFeedback.Utils.showMessage(connectingMessage, window.MCPFeedback.Utils.CONSTANTS.MESSAGE_INFO);
            }
        } else {
            const invalidStateMessage = window.i18nManager ? window.i18nManager.t('feedback.invalidState') : '当前状态不允许提交';
            window.MCPFeedback.Utils.showMessage(invalidStateMessage + ': ' + feedbackState, window.MCPFeedback.Utils.CONSTANTS.MESSAGE_WARNING);
        }
    };

    /**
     * 收集回馈数据
     */
    FeedbackApp.prototype.collectFeedbackData = function() {
        // 获取合并模式的回馈内容
        let feedback = '';
        const combinedFeedbackInput = window.MCPFeedback.Utils.safeQuerySelector('#combinedFeedbackText');
        feedback = combinedFeedbackInput ? combinedFeedbackInput.value.trim() : '';

        const images = this.imageHandler ? this.imageHandler.getImages() : [];

        if (!feedback && images.length === 0) {
            const message = window.i18nManager ? 
                window.i18nManager.t('feedback.provideTextOrImage', '请提供回馈文字或上传图片') : 
                '请提供回馈文字或上传图片';
            window.MCPFeedback.Utils.showMessage(message, window.MCPFeedback.Utils.CONSTANTS.MESSAGE_WARNING);
            return null;
        }

        return {
            feedback: feedback,
            images: images,
            settings: {
                image_size_limit: this.imageHandler ? this.imageHandler.imageSizeLimit : 0,
                enable_base64_detail: this.imageHandler ? this.imageHandler.enableBase64Detail : false
            }
        };
    };

    /**
     * 内部提交回馈方法
     */
    FeedbackApp.prototype.submitFeedbackInternal = function(feedbackData) {
        console.log('📤 内部提交回馈...');

        try {
            // 1. 首先记录用户讯息到会话历史（立即保存到伺服器）
            this.recordUserMessage(feedbackData);

            // 2. 设置处理状态
            if (this.uiManager) {
                this.uiManager.setFeedbackState(window.MCPFeedback.Utils.CONSTANTS.FEEDBACK_PROCESSING);
            }

            // 停止自动提交计时器（如果正在运行）
            if (this.autoSubmitManager && this.autoSubmitManager.isEnabled) {
                console.log('⏸️ 手动提交反馈，停止自动提交倒数计时器');
                this.autoSubmitManager.stop();
            }
            
            // 停止会话超时计时器
            if (this.webSocketManager) {
                console.log('⏸️ 提交反馈，停止会话超时计时器');
                this.webSocketManager.stopSessionTimeout();
            }

            // 3. 发送回馈到 AI 助手
            const success = this.webSocketManager.send({
                type: 'submit_feedback',
                feedback: feedbackData.feedback,
                images: feedbackData.images,
                settings: feedbackData.settings
            });

            if (success) {
                // 重置表单状态但保留文字内容
                if (this.uiManager) {
                    this.uiManager.resetFeedbackForm(false);  // false 表示不清空文字
                }
                // 只清空图片
                if (this.imageHandler) {
                    this.imageHandler.clearImages();
                }
                console.log('📤 回馈已发送，等待服务器确认...');
            } else {
                throw new Error('WebSocket 发送失败');
            }

        } catch (error) {
            console.error('❌ 发送回馈失败:', error);
            const sendFailedMessage = window.i18nManager ? window.i18nManager.t('feedback.sendFailed') : '发送失败，请重试';
            window.MCPFeedback.Utils.showMessage(sendFailedMessage, window.MCPFeedback.Utils.CONSTANTS.MESSAGE_ERROR);

            // 恢复到等待状态
            if (this.uiManager) {
                this.uiManager.setFeedbackState(window.MCPFeedback.Utils.CONSTANTS.FEEDBACK_WAITING);
            }
        }
    };

    /**
     * 记录用户讯息到会话历史
     */
    FeedbackApp.prototype.recordUserMessage = function(feedbackData) {
        console.log('📝 记录用户讯息到会话历史...');

        try {
            // 检查是否有会话管理器
            if (!this.sessionManager || !this.sessionManager.dataManager) {
                console.warn('📝 会话管理器未初始化，跳过用户讯息记录');
                return;
            }

            // 判断提交方式
            const submissionMethod = this.autoSubmitManager && this.autoSubmitManager.isEnabled ? 'auto' : 'manual';

            // 建立讯息记录资料
            const messageData = {
                content: feedbackData.feedback || '',
                images: feedbackData.images || [],
                submission_method: submissionMethod
            };

            // 记录到会话历史
            const success = this.sessionManager.dataManager.addUserMessage(messageData);

            if (success) {
                console.log('📝 用户讯息已记录到会话历史');
            } else {
                console.log('📝 用户讯息记录被跳过（可能因隐私设定或其他原因）');
            }

        } catch (error) {
            console.error('❌ 记录用户讯息失败:', error);
            // 不影响主要功能，只记录错误
        }
    };

    /**
     * 清空回馈内容
     */
    FeedbackApp.prototype.clearFeedback = function() {
        console.log('🧹 清空回馈内容...');

        // 使用 UI 管理器重置表单，并清空文字
        if (this.uiManager) {
            this.uiManager.resetFeedbackForm(true);  // 传入 true 表示要清空文字
        }

        // 清空图片数据
        if (this.imageHandler) {
            this.imageHandler.clearImages();
        }

        console.log('✅ 回馈内容清空完成');
    };

    /**
     * 复制用户回馈内容
     */
    FeedbackApp.prototype.copyUserFeedback = function() {
        console.log('📋 复制用户回馈内容...');

        const feedbackInput = window.MCPFeedback.Utils.safeQuerySelector('#combinedFeedbackText');
        if (!feedbackInput || !feedbackInput.value.trim()) {
            window.MCPFeedback.Utils.showMessage(
                window.i18nManager ? window.i18nManager.t('feedback.noContent') : '没有可复制的内容',
                window.MCPFeedback.Utils.CONSTANTS.MESSAGE_WARNING
            );
            return;
        }

        const textContent = feedbackInput.value;

        // 复制到剪贴板
        navigator.clipboard.writeText(textContent)
            .then(function() {
                console.log('✅ 内容已复制到剪贴板');
                window.MCPFeedback.Utils.showMessage(
                    window.i18nManager ? window.i18nManager.t('feedback.copySuccess') : '内容已复制到剪贴板',
                    window.MCPFeedback.Utils.CONSTANTS.MESSAGE_SUCCESS
                );
            })
            .catch(function(err) {
                console.error('❌ 复制失败:', err);
                // 降级方案：使用旧的复制方法
                const textarea = document.createElement('textarea');
                textarea.value = textContent;
                textarea.style.position = 'fixed';
                textarea.style.left = '-999999px';
                document.body.appendChild(textarea);
                textarea.select();
                try {
                    document.execCommand('copy');
                    window.MCPFeedback.Utils.showMessage(
                        window.i18nManager ? window.i18nManager.t('feedback.copySuccess') : '内容已复制到剪贴板',
                        window.MCPFeedback.Utils.CONSTANTS.MESSAGE_SUCCESS
                    );
                } catch (error) {
                    window.MCPFeedback.Utils.showMessage(
                        window.i18nManager ? window.i18nManager.t('feedback.copyFailed') : '复制失败',
                        window.MCPFeedback.Utils.CONSTANTS.MESSAGE_ERROR
                    );
                }
                document.body.removeChild(textarea);
            });
    };

    /**
     * 取消回馈
     */
    FeedbackApp.prototype.cancelFeedback = function() {
        console.log('❌ 取消回馈');
        this.clearFeedback();
    };

    /**
     * 聚焦到输入框 (Ctrl+I 快捷键)
     */
    FeedbackApp.prototype.focusInput = function() {
        console.log('🎯 执行聚焦输入框...');

        // 聚焦到合并模式的输入框
        const targetInput = window.MCPFeedback.Utils.safeQuerySelector('#combinedFeedbackText');

        // 确保在工作区分页
        if (this.uiManager && this.uiManager.getCurrentTab() !== 'combined') {
            this.uiManager.switchTab('combined');
        }

        if (targetInput) {
            // 聚焦并滚动到可见区域
            targetInput.focus();
            targetInput.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });

            console.log('✅ 已聚焦到输入框');
        } else {
            console.warn('⚠️ 未找到目标输入框');
        }
    };

    /**
     * 执行命令
     */
    FeedbackApp.prototype.runCommand = function() {
        const commandInput = window.MCPFeedback.Utils.safeQuerySelector('#commandInput');
        const command = commandInput ? commandInput.value.trim() : '';

        if (!command) {
            const emptyCommandMessage = window.i18nManager ? window.i18nManager.t('commands.emptyCommand') : '请输入命令';
            this.appendCommandOutput('⚠️ ' + emptyCommandMessage + '\n');
            return;
        }

        if (!this.webSocketManager || !this.webSocketManager.isConnected) {
            const notConnectedMessage = window.i18nManager ? window.i18nManager.t('commands.notConnected') : 'WebSocket 未连接，无法执行命令';
            this.appendCommandOutput('❌ ' + notConnectedMessage + '\n');
            return;
        }

        // 显示执行的命令
        this.appendCommandOutput('$ ' + command + '\n');

        // 发送命令
        try {
            const success = this.webSocketManager.send({
                type: 'run_command',
                command: command
            });

            if (success) {
                // 清空输入框
                commandInput.value = '';
                const executingMessage = window.i18nManager ? window.i18nManager.t('commands.executing') : '正在执行...';
                this.appendCommandOutput('[' + executingMessage + ']\n');
            } else {
                const sendFailedMessage = window.i18nManager ? window.i18nManager.t('commands.sendFailed') : '发送命令失败';
                this.appendCommandOutput('❌ ' + sendFailedMessage + '\n');
            }

        } catch (error) {
            const sendFailedMessage = window.i18nManager ? window.i18nManager.t('commands.sendFailed') : '发送命令失败';
            this.appendCommandOutput('❌ ' + sendFailedMessage + ': ' + error.message + '\n');
        }
    };

    /**
     * 添加命令输出
     */
    FeedbackApp.prototype.appendCommandOutput = function(output) {
        const commandOutput = window.MCPFeedback.Utils.safeQuerySelector('#commandOutput');
        if (commandOutput) {
            // 检查是否是空的（首次使用）
            if (commandOutput.textContent === '' && output.startsWith('$')) {
                // 如果是空的且输出以 $ 开头，添加欢迎讯息
                const projectPathElement = window.MCPFeedback.Utils.safeQuerySelector('#projectPathDisplay');
                const projectPath = projectPathElement ? projectPathElement.getAttribute('data-full-path') : 'unknown';
                
                const welcomeText = `欢迎使用互动回馈终端
========================================
专案目录: ${projectPath}
输入命令后按 Enter 或点击执行按钮
支援的命令: ls, dir, pwd, cat, type 等

`;
                commandOutput.textContent = welcomeText;
            }
            
            commandOutput.textContent += output;
            commandOutput.scrollTop = commandOutput.scrollHeight;
        }
    };

    /**
     * 启用命令输入
     */
    FeedbackApp.prototype.enableCommandInput = function() {
        const commandInput = window.MCPFeedback.Utils.safeQuerySelector('#commandInput');
        const runCommandBtn = window.MCPFeedback.Utils.safeQuerySelector('#runCommandBtn');

        if (commandInput) commandInput.disabled = false;
        if (runCommandBtn) {
            runCommandBtn.disabled = false;
            runCommandBtn.textContent = '▶️ 执行';
        }
    };

    /**
     * 执行新会话自动命令
     */
    FeedbackApp.prototype.executeAutoCommandOnNewSession = function() {
        if (!this.settingsManager) return;
        
        const settings = this.settingsManager.currentSettings;
        if (!settings.autoCommandEnabled || !settings.commandOnNewSession) {
            console.log('⏩ 新会话自动命令未启用或未设定');
            return;
        }
        
        const command = settings.commandOnNewSession.trim();
        if (!command) return;
        
        console.log('🚀 执行新会话自动命令:', command);
        this.appendCommandOutput('🆕 [自动执行] $ ' + command + '\n');
        
        // 使用 WebSocket 发送命令
        if (this.webSocketManager && this.webSocketManager.isConnected) {
            console.log('📡 WebSocket 已连接，发送命令:', command);
            this.webSocketManager.send({
                type: 'run_command',
                command: command
            });
        } else {
            console.error('❌ 无法执行自动命令：WebSocket 未连接');
            this.appendCommandOutput('[错误] WebSocket 未连接，无法执行命令\n');
        }
    };
    
    /**
     * 执行提交回馈后自动命令
     */
    FeedbackApp.prototype.executeAutoCommandOnFeedbackSubmit = function() {
        if (!this.settingsManager) return;
        
        const settings = this.settingsManager.currentSettings;
        if (!settings.autoCommandEnabled || !settings.commandOnFeedbackSubmit) {
            console.log('⏩ 提交回馈后自动命令未启用或未设定');
            return;
        }
        
        const command = settings.commandOnFeedbackSubmit.trim();
        if (!command) return;
        
        console.log('🚀 执行提交回馈后自动命令:', command);
        this.appendCommandOutput('✅ [自动执行] $ ' + command + '\n');
        
        // 使用 WebSocket 发送命令
        if (this.webSocketManager && this.webSocketManager.isConnected) {
            console.log('📡 WebSocket 已连接，发送命令:', command);
            this.webSocketManager.send({
                type: 'run_command',
                command: command
            });
        } else {
            console.error('❌ 无法执行自动命令：WebSocket 未连接');
            this.appendCommandOutput('[错误] WebSocket 未连接，无法执行命令\n');
        }
    };

    /**
     * 更新摘要状态
     */
    FeedbackApp.prototype.updateSummaryStatus = function(message) {
        const summaryElements = document.querySelectorAll('.ai-summary-content');
        summaryElements.forEach(function(element) {
            element.innerHTML = '<div style="padding: 16px; background: var(--success-color); color: white; border-radius: 6px; text-align: center;">✅ ' + message + '</div>';
        });
    };

    /**
     * 设置自动命令相关事件
     */
    FeedbackApp.prototype.setupAutoCommandEvents = function() {
        const self = this;
        
        // 自动命令开关
        const autoCommandEnabled = window.MCPFeedback.Utils.safeQuerySelector('#autoCommandEnabled');
        if (autoCommandEnabled) {
            // 载入设定
            if (this.settingsManager) {
                autoCommandEnabled.checked = this.settingsManager.currentSettings.autoCommandEnabled;
                this.updateAutoCommandUI(autoCommandEnabled.checked);
            }
            
            autoCommandEnabled.addEventListener('change', function() {
                const enabled = autoCommandEnabled.checked;
                self.updateAutoCommandUI(enabled);
                
                if (self.settingsManager) {
                    self.settingsManager.saveSettings({
                        autoCommandEnabled: enabled
                    });
                }
            });
        }
        
        // 新会话命令输入
        const commandOnNewSession = window.MCPFeedback.Utils.safeQuerySelector('#commandOnNewSession');
        if (commandOnNewSession) {
            // 载入设定
            if (this.settingsManager) {
                commandOnNewSession.value = this.settingsManager.currentSettings.commandOnNewSession || '';
            }
            
            commandOnNewSession.addEventListener('change', function() {
                if (self.settingsManager) {
                    self.settingsManager.saveSettings({
                        commandOnNewSession: commandOnNewSession.value
                    });
                }
            });
        }
        
        // 提交回馈后命令输入
        const commandOnFeedbackSubmit = window.MCPFeedback.Utils.safeQuerySelector('#commandOnFeedbackSubmit');
        if (commandOnFeedbackSubmit) {
            // 载入设定
            if (this.settingsManager) {
                commandOnFeedbackSubmit.value = this.settingsManager.currentSettings.commandOnFeedbackSubmit || '';
            }
            
            commandOnFeedbackSubmit.addEventListener('change', function() {
                if (self.settingsManager) {
                    self.settingsManager.saveSettings({
                        commandOnFeedbackSubmit: commandOnFeedbackSubmit.value
                    });
                }
            });
        }
        
        // 测试执行按钮
        const testNewSessionCommand = window.MCPFeedback.Utils.safeQuerySelector('#testNewSessionCommand');
        if (testNewSessionCommand) {
            testNewSessionCommand.addEventListener('click', function() {
                const command = commandOnNewSession ? commandOnNewSession.value.trim() : '';
                if (command) {
                    self.testCommand(command, '🆕 [测试] ');
                } else {
                    window.MCPFeedback.Utils.showMessage('请先输入命令', window.MCPFeedback.Utils.CONSTANTS.MESSAGE_WARNING);
                }
            });
        }
        
        const testFeedbackCommand = window.MCPFeedback.Utils.safeQuerySelector('#testFeedbackCommand');
        if (testFeedbackCommand) {
            testFeedbackCommand.addEventListener('click', function() {
                const command = commandOnFeedbackSubmit ? commandOnFeedbackSubmit.value.trim() : '';
                if (command) {
                    self.testCommand(command, '✅ [测试] ');
                } else {
                    window.MCPFeedback.Utils.showMessage('请先输入命令', window.MCPFeedback.Utils.CONSTANTS.MESSAGE_WARNING);
                }
            });
        }
    };
    
    /**
     * 更新自动命令 UI 状态
     */
    FeedbackApp.prototype.updateAutoCommandUI = function(enabled) {
        const autoCommandContent = window.MCPFeedback.Utils.safeQuerySelector('#autoCommandContent');
        if (autoCommandContent) {
            if (enabled) {
                autoCommandContent.classList.remove('disabled');
            } else {
                autoCommandContent.classList.add('disabled');
            }
        }
    };
    
    /**
     * 测试命令执行
     */
    FeedbackApp.prototype.testCommand = function(command, prefix) {
        if (!command) return;
        
        console.log('🧪 测试执行命令:', command);
        this.appendCommandOutput(prefix + '$ ' + command + '\n');
        
        // 使用 WebSocket 发送命令
        if (this.webSocketManager && this.webSocketManager.isConnected) {
            this.webSocketManager.send({
                type: 'run_command',
                command: command
            });
        } else {
            this.appendCommandOutput('❌ WebSocket 未连接\n');
        }
    };

    /**
     * 处理会话更新（来自自动刷新）
     */
    FeedbackApp.prototype.handleSessionUpdate = function(sessionData) {
        console.log('🔄 处理自动检测到的会话更新:', sessionData);

        // 只更新当前会话 ID，不管理状态
        this.currentSessionId = sessionData.session_id;

        // 局部更新页面内容
        this.refreshPageContent();
    };

    /**
     * 刷新页面内容
     */
    FeedbackApp.prototype.refreshPageContent = function() {
        console.log('🔄 局部更新页面内容...');

        const self = this;

        fetch('/api/current-session')
            .then(function(response) {
                if (!response.ok) {
                    throw new Error('API 请求失败: ' + response.status);
                }
                return response.json();
            })
            .then(function(sessionData) {
                console.log('📥 获取到最新会话资料:', sessionData);

                // 检查并保护已提交状态
                if (sessionData.session_id && self.uiManager) {
                    const currentState = self.uiManager.getFeedbackState();
                    if (currentState !== window.MCPFeedback.Utils.CONSTANTS.FEEDBACK_SUBMITTED) {
                        self.uiManager.setFeedbackState(window.MCPFeedback.Utils.CONSTANTS.FEEDBACK_WAITING, sessionData.session_id);
                        console.log('🔄 局部更新：重置回馈状态为等待中');
                    } else {
                        console.log('🔒 局部更新：保护已提交状态，不重置');
                        // 只更新会话ID，保持已提交状态
                        self.uiManager.setFeedbackState(window.MCPFeedback.Utils.CONSTANTS.FEEDBACK_SUBMITTED, sessionData.session_id);
                    }
                }

                // 更新 AI 摘要内容
                if (self.uiManager) {
                    // console.log('🔧 准备更新 AI 摘要内容，summary 长度:', sessionData.summary ? sessionData.summary.length : 'undefined');
                    self.uiManager.updateAISummaryContent(sessionData.summary);
                    self.uiManager.resetFeedbackForm(false);  // 不清空文字内容
                    self.uiManager.updateStatusIndicator();
                }

                // 更新页面标题
                if (sessionData.project_directory) {
                    const projectName = sessionData.project_directory.split(/[/\\]/).pop();
                    document.title = 'MCP Feedback - ' + projectName;
                }

                console.log('✅ 局部更新完成');
            })
            .catch(function(error) {
                console.error('❌ 局部更新失败:', error);
                const updateFailedMessage = window.i18nManager ? window.i18nManager.t('app.updateFailed') : '更新内容失败，请手动刷新页面以查看新的 AI 工作摘要';
                window.MCPFeedback.Utils.showMessage(updateFailedMessage, window.MCPFeedback.Utils.CONSTANTS.MESSAGE_WARNING);
            });
    };

    /**
     * 初始化自动提交管理器
     */
    FeedbackApp.prototype.initializeAutoSubmitManager = function() {
        console.log('⏰ 初始化自动提交管理器...');

        try {
            const self = this;

            // 创建自动提交管理器
            this.autoSubmitManager = {
                countdown: null,
                isEnabled: false,
                currentPromptId: null,

                // 启动自动提交
                start: function(timeoutSeconds, promptId) {
                    this.stop(); // 先停止现有的倒数计时

                    this.isEnabled = true;
                    this.currentPromptId = promptId;

                    // 显示倒数计时器
                    self.showCountdownDisplay();

                    // 创建倒数计时器
                    this.countdown = window.MCPFeedback.Utils.Time.createAutoSubmitCountdown(
                        timeoutSeconds,
                        function(remainingTime, isCompleted) {
                            // 更新倒数计时显示
                            self.updateCountdownDisplay(remainingTime);
                        },
                        function() {
                            // 时间到，自动提交
                            self.performAutoSubmit();
                        }
                    );

                    this.countdown.start();
                    console.log('⏰ 自动提交倒数计时已启动:', timeoutSeconds + '秒');
                },

                // 停止自动提交
                stop: function() {
                    if (this.countdown) {
                        this.countdown.stop();
                        this.countdown = null;
                    }

                    this.isEnabled = false;
                    this.currentPromptId = null;

                    // 隐藏倒数计时器
                    self.hideCountdownDisplay();

                    console.log('⏸️ 自动提交倒数计时已停止');
                },

                // 暂停倒数计时
                pause: function() {
                    if (this.countdown && this.countdown.pause) {
                        this.countdown.pause();
                        self.updateCountdownPauseState(true);
                        console.log('⏸ 自动提交倒数计时已暂停');
                    }
                },

                // 恢复倒数计时
                resume: function() {
                    if (this.countdown && this.countdown.resume) {
                        this.countdown.resume();
                        self.updateCountdownPauseState(false);
                        console.log('▶ 自动提交倒数计时已恢复');
                    }
                },

                // 切换暂停/恢复状态
                togglePause: function() {
                    if (!this.countdown) return;
                    
                    if (this.countdown.isPaused()) {
                        this.resume();
                    } else {
                        this.pause();
                    }
                }
            };

            console.log('✅ 自动提交管理器初始化完成');

        } catch (error) {
            console.error('❌ 自动提交管理器初始化失败:', error);
        }
    };

    /**
     * 检查并启动自动提交（原始版本，供防抖使用）
     */
    FeedbackApp.prototype._originalCheckAndStartAutoSubmit = function() {
        // 减少重复日志：只在首次检查或条件变化时记录
        if (!this._lastAutoSubmitCheck || Date.now() - this._lastAutoSubmitCheck > 1000) {
            console.log('🔍 检查自动提交条件...');
            this._lastAutoSubmitCheck = Date.now();
        }

        if (!this.autoSubmitManager || !this.settingsManager || !this.promptManager) {
            console.log('⚠️ 自动提交管理器、设定管理器或提示词管理器未初始化');
            return;
        }

        // 检查自动提交是否已启用
        const autoSubmitEnabled = this.settingsManager.get('autoSubmitEnabled');
        const autoSubmitPromptId = this.settingsManager.get('autoSubmitPromptId');
        const autoSubmitTimeout = this.settingsManager.get('autoSubmitTimeout');

        console.log('🔍 自动提交设定检查:', {
            enabled: autoSubmitEnabled,
            promptId: autoSubmitPromptId,
            timeout: autoSubmitTimeout
        });

        // 双重检查：设定中的 promptId 和提示词的 isAutoSubmit 状态
        let validAutoSubmitPrompt = null;
        if (autoSubmitPromptId) {
            const prompt = this.promptManager.getPromptById(autoSubmitPromptId);
            if (prompt && prompt.isAutoSubmit) {
                validAutoSubmitPrompt = prompt;
            } else {
                console.log('⚠️ 自动提交提示词验证失败:', {
                    promptExists: !!prompt,
                    isAutoSubmit: prompt ? prompt.isAutoSubmit : false,
                    reason: !prompt ? '提示词不存在' : '提示词未标记为自动提交'
                });
                // 只清空无效的 promptId，保留用户的 autoSubmitEnabled 设定
                // 这样避免因为提示词问题而强制关闭用户的自动提交偏好
                this.settingsManager.set('autoSubmitPromptId', null);
                console.log('🔧 已清空无效的 autoSubmitPromptId，保留 autoSubmitEnabled 设定:', autoSubmitEnabled);
            }
        }

        // 检查当前状态是否为等待回馈
        const currentState = this.uiManager ? this.uiManager.getFeedbackState() : null;
        const isWaitingForFeedback = currentState === window.MCPFeedback.Utils.CONSTANTS.FEEDBACK_WAITING;

        console.log('🔍 当前回馈状态:', currentState, '是否等待回馈:', isWaitingForFeedback);

        // 如果所有条件都满足，启动自动提交
        if (autoSubmitEnabled && validAutoSubmitPrompt && autoSubmitTimeout && isWaitingForFeedback) {
            console.log('✅ 自动提交条件满足，启动倒数计时器');
            this.autoSubmitManager.start(autoSubmitTimeout, autoSubmitPromptId);
            this.updateAutoSubmitStatus('enabled', autoSubmitTimeout);
        } else {
            console.log('❌ 自动提交条件不满足，停止倒数计时器');
            this.autoSubmitManager.stop();
            this.updateAutoSubmitStatus('disabled');
        }
    };

    /**
     * 检查并启动自动提交（防抖版本）
     */
    FeedbackApp.prototype.checkAndStartAutoSubmit = function() {
        if (this._debouncedCheckAndStartAutoSubmit) {
            this._debouncedCheckAndStartAutoSubmit();
        } else {
            // 回退到原始方法（防抖未初始化时）
            this._originalCheckAndStartAutoSubmit();
        }
    };

    /**
     * 处理自动提交状态变更
     */
    FeedbackApp.prototype.handleAutoSubmitStateChange = function(enabled, settings) {
        console.log('⏰ 处理自动提交状态变更:', enabled, settings);

        if (!this.autoSubmitManager) {
            console.warn('⚠️ 自动提交管理器未初始化');
            return;
        }

        if (enabled && settings.promptId && settings.timeout) {
            // 检查当前状态是否适合启动自动提交
            const currentState = this.uiManager ? this.uiManager.getFeedbackState() : null;
            const isWaitingForFeedback = currentState === window.MCPFeedback.Utils.CONSTANTS.FEEDBACK_WAITING;

            if (isWaitingForFeedback) {
                // 启动自动提交
                this.autoSubmitManager.start(settings.timeout, settings.promptId);
                this.updateAutoSubmitStatus('enabled', settings.timeout);
                console.log('⏰ 自动提交已启动（设定变更触发）');
            } else {
                // 只更新状态显示，不启动倒数计时器
                this.updateAutoSubmitStatus('enabled', settings.timeout);
                console.log('⏰ 自动提交设定已启用，等待适当时机启动');
            }
        } else {
            // 停止自动提交
            this.autoSubmitManager.stop();
            this.updateAutoSubmitStatus('disabled');
            console.log('⏸️ 自动提交已停用（设定变更触发）');
        }
    };

    /**
     * 执行自动提交
     */
    FeedbackApp.prototype.performAutoSubmit = function() {
        console.log('⏰ 执行自动提交...');

        if (!this.autoSubmitManager || !this.promptManager || !this.settingsManager) {
            console.error('❌ 自动提交管理器、提示词管理器或设定管理器未初始化');
            this.autoSubmitManager && this.autoSubmitManager.stop();
            return;
        }

        const promptId = this.autoSubmitManager.currentPromptId;
        const autoSubmitPromptId = this.settingsManager.get('autoSubmitPromptId');

        // 双重检查：确保 promptId 有效且与设定一致
        if (!promptId || !autoSubmitPromptId || promptId !== autoSubmitPromptId) {
            console.error('❌ 自动提交提示词 ID 不一致或为空:', {
                currentPromptId: promptId,
                settingsPromptId: autoSubmitPromptId
            });
            this.pauseAutoSubmit('提示词 ID 不一致');
            return;
        }

        const prompt = this.promptManager.getPromptById(promptId);

        if (!prompt) {
            console.error('❌ 找不到自动提交提示词:', promptId);
            this.pauseAutoSubmit('找不到指定的提示词');
            return;
        }

        // 检查提示词的 isAutoSubmit 状态
        if (!prompt.isAutoSubmit) {
            console.error('❌ 提示词不是自动提交状态:', prompt.name);
            this.pauseAutoSubmit('提示词不是自动提交状态');
            return;
        }

        // 设定提示词内容到回馈输入框
        const feedbackInput = window.MCPFeedback.Utils.safeQuerySelector('#combinedFeedbackText');
        if (feedbackInput) {
            feedbackInput.value = prompt.content;
        }

        // 显示自动提交讯息
        const message = window.i18nManager ?
            window.i18nManager.t('autoSubmit.executing', '正在执行自动提交...') :
            '正在执行自动提交...';
        window.MCPFeedback.Utils.showMessage(message, window.MCPFeedback.Utils.CONSTANTS.MESSAGE_INFO);

        // 执行提交
        this.submitFeedback();

        // 更新提示词使用记录
        this.promptManager.usePrompt(promptId);

        // 停止自动提交
        this.autoSubmitManager.stop();
    };

    /**
     * 暂停自动提交功能（当检查失败时）
     */
    FeedbackApp.prototype.pauseAutoSubmit = function(reason) {
        console.error('⏸️ 暂停自动提交功能，原因:', reason);

        // 停止倒数计时器
        if (this.autoSubmitManager) {
            this.autoSubmitManager.stop();
        }

        // 清空自动提交设定
        if (this.settingsManager) {
            this.settingsManager.set('autoSubmitEnabled', false);
            this.settingsManager.set('autoSubmitPromptId', null);
        }

        // 清空所有提示词的自动提交标记
        if (this.promptManager) {
            this.promptManager.clearAutoSubmitPrompt();
        }

        // 更新 UI 状态
        this.updateAutoSubmitStatus('disabled');

        // 显示错误讯息
        const message = window.i18nManager ?
            window.i18nManager.t('autoSubmit.paused', '自动提交已暂停：') + reason :
            '自动提交已暂停：' + reason;
        window.MCPFeedback.Utils.showMessage(message, window.MCPFeedback.Utils.CONSTANTS.MESSAGE_ERROR);
    };

    /**
     * 显示倒数计时器
     */
    FeedbackApp.prototype.showCountdownDisplay = function() {
        const countdownDisplay = document.getElementById('countdownDisplay');

        if (countdownDisplay) {
            countdownDisplay.style.display = 'flex';
        }
    };

    /**
     * 隐藏倒数计时器
     */
    FeedbackApp.prototype.hideCountdownDisplay = function() {
        const countdownDisplay = document.getElementById('countdownDisplay');

        if (countdownDisplay) {
            countdownDisplay.style.display = 'none';
            // 重置暂停状态
            this.updateCountdownPauseState(false);
        }
    };

    /**
     * 更新倒数计时显示
     */
    FeedbackApp.prototype.updateCountdownDisplay = function(remainingSeconds) {
        const countdownTimer = document.getElementById('countdownTimer');

        const formattedTime = window.MCPFeedback.Utils.Time.formatAutoSubmitCountdown(remainingSeconds);

        // 更新倒数计时器
        if (countdownTimer) {
            countdownTimer.textContent = formattedTime;

            // 根据剩余时间调整样式
            countdownTimer.className = 'countdown-timer';
            if (remainingSeconds <= 10) {
                countdownTimer.classList.add('danger');
            } else if (remainingSeconds <= 30) {
                countdownTimer.classList.add('warning');
            }
        }
    };

    /**
     * 更新自动提交状态显示
     */
    FeedbackApp.prototype.updateAutoSubmitStatus = function(status, timeout) {
        const statusElement = document.getElementById('autoSubmitStatus');
        if (!statusElement) return;

        const statusIcon = statusElement.querySelector('span:first-child');
        const statusText = statusElement.querySelector('.button-text');

        if (status === 'enabled') {
            // 直接设定 HTML 内容，就像提示词按钮一样
            if (statusIcon) statusIcon.innerHTML = '⏰';
            if (statusText) {
                const enabledText = window.i18nManager ?
                    window.i18nManager.t('autoSubmit.enabled', '已启用') :
                    '已启用';
                statusText.textContent = `${enabledText} (${timeout}秒)`;
            }
            statusElement.className = 'auto-submit-status-btn enabled';
        } else {
            // 直接设定 HTML 内容，就像提示词按钮一样
            if (statusIcon) statusIcon.innerHTML = '⏸️';
            if (statusText) {
                const disabledText = window.i18nManager ?
                    window.i18nManager.t('autoSubmit.disabled', '已停用') :
                    '已停用';
                statusText.textContent = disabledText;
            }
            statusElement.className = 'auto-submit-status-btn disabled';
        }
    };

    /**
     * 更新倒数计时器暂停状态
     */
    FeedbackApp.prototype.updateCountdownPauseState = function(isPaused) {
        const countdownDisplay = document.getElementById('countdownDisplay');
        const pauseBtn = document.getElementById('countdownPauseBtn');
        
        if (!countdownDisplay || !pauseBtn) return;
        
        // 更新暂停/恢复图标
        const pauseIcon = pauseBtn.querySelector('.pause-icon');
        const resumeIcon = pauseBtn.querySelector('.resume-icon');
        
        if (isPaused) {
            countdownDisplay.classList.add('paused');
            if (pauseIcon) pauseIcon.style.display = 'none';
            if (resumeIcon) resumeIcon.style.display = 'inline';
            
            // 更新按钮的 tooltip
            const resumeTitle = window.i18nManager ?
                window.i18nManager.t('autoSubmit.resumeCountdown', '恢复倒数') :
                '恢复倒数';
            pauseBtn.setAttribute('title', resumeTitle);
            pauseBtn.setAttribute('data-i18n-title', 'autoSubmit.resumeCountdown');
        } else {
            countdownDisplay.classList.remove('paused');
            if (pauseIcon) pauseIcon.style.display = 'inline';
            if (resumeIcon) resumeIcon.style.display = 'none';
            
            // 更新按钮的 tooltip
            const pauseTitle = window.i18nManager ?
                window.i18nManager.t('autoSubmit.pauseCountdown', '暂停倒数') :
                '暂停倒数';
            pauseBtn.setAttribute('title', pauseTitle);
            pauseBtn.setAttribute('data-i18n-title', 'autoSubmit.pauseCountdown');
        }
    };

    /**
     * 设置用户活动监听器（用于重置会话超时）
     */
    FeedbackApp.prototype.setupUserActivityListeners = function() {
        const self = this;
        
        // 定义需要监听的活动事件
        const activityEvents = ['click', 'keypress', 'mousemove', 'touchstart', 'scroll'];
        
        // 防抖处理，避免过于频繁地重置计时器
        const resetTimeout = window.MCPFeedback.Utils.DOM.debounce(function() {
            if (self.webSocketManager) {
                self.webSocketManager.resetSessionTimeout();
            }
        }, 5000, false); // 5秒内的连续活动只重置一次
        
        // 为每个事件添加监听器
        activityEvents.forEach(function(eventType) {
            document.addEventListener(eventType, resetTimeout, { passive: true });
        });
        
        console.log('✅ 用户活动监听器已设置');
    };

    /**
     * 清理资源
     */
    FeedbackApp.prototype.cleanup = function() {
        console.log('🧹 清理应用程式资源...');

        if (this.autoSubmitManager) {
            this.autoSubmitManager.stop();
        }

        if (this.tabManager) {
            this.tabManager.cleanup();
        }

        if (this.webSocketManager) {
            this.webSocketManager.close();
        }

        if (this.connectionMonitor) {
            this.connectionMonitor.cleanup();
        }

        if (this.sessionManager) {
            this.sessionManager.cleanup();
        }

        if (this.imageHandler) {
            this.imageHandler.cleanup();
        }

        if (this.textareaHeightManager) {
            this.textareaHeightManager.destroy();
        }

        console.log('✅ 应用程式资源清理完成');
    };

    // 将 FeedbackApp 加入命名空间
    window.MCPFeedback.FeedbackApp = FeedbackApp;

    console.log('✅ FeedbackApp 主模组载入完成');

})();