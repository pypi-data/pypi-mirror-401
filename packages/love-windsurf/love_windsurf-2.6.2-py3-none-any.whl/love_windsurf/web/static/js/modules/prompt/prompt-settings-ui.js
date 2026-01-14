/**
 * MCP Feedback Enhanced - 提示词设定 UI 模组
 * =========================================
 * 
 * 处理设定页签中的提示词管理介面
 */

(function() {
    'use strict';

    // 确保命名空间存在
    window.MCPFeedback = window.MCPFeedback || {};
    window.MCPFeedback.Prompt = window.MCPFeedback.Prompt || {};

    const Utils = window.MCPFeedback.Utils;

    /**
     * 提示词设定 UI 管理器
     */
    function PromptSettingsUI(options) {
        options = options || {};

        // 依赖注入
        this.promptManager = options.promptManager || null;
        this.promptModal = options.promptModal || null;
        this.settingsManager = options.settingsManager || null;

        // UI 元素
        this.container = null;
        this.promptList = null;
        this.addButton = null;

        // 状态
        this.isInitialized = false;

        console.log('🎨 PromptSettingsUI 初始化完成');
    }

    /**
     * 初始化设定 UI
     */
    PromptSettingsUI.prototype.init = function(containerSelector) {
        this.container = document.querySelector(containerSelector);
        if (!this.container) {
            console.error('❌ 找不到提示词设定容器:', containerSelector);
            return false;
        }

        // 创建 UI 结构
        this.createUI();

        // 设置事件监听器
        this.setupEventListeners();

        // 载入提示词列表
        this.refreshPromptList();

        this.isInitialized = true;
        console.log('✅ PromptSettingsUI 初始化完成');
        return true;
    };

    /**
     * 创建 UI 结构
     */
    PromptSettingsUI.prototype.createUI = function() {
        const html = `
            <div class="prompt-management-section">
                <div class="prompt-management-header">
                    <h4 class="prompt-management-title" data-i18n="prompts.management.title">
                        📝 常用提示词管理
                    </h4>
                    <button type="button" class="btn btn-primary prompt-add-btn" id="promptAddBtn">
                        <span data-i18n="prompts.management.addNew">新增提示词</span>
                    </button>
                </div>
                <div class="prompt-management-description" data-i18n="prompts.management.description">
                    管理您的常用提示词模板，可在回馈输入时快速选用
                </div>
                <div class="prompt-settings-list" id="promptSettingsList">
                    <!-- 提示词列表将在这里动态生成 -->
                </div>
            </div>
        `;

        this.container.insertAdjacentHTML('beforeend', html);

        // 获取 UI 元素引用
        this.promptList = this.container.querySelector('#promptSettingsList');
        this.addButton = this.container.querySelector('#promptAddBtn');
    };

    /**
     * 设置事件监听器
     */
    PromptSettingsUI.prototype.setupEventListeners = function() {
        const self = this;

        // 新增按钮事件
        if (this.addButton) {
            this.addButton.addEventListener('click', function() {
                self.handleAddPrompt();
            });
        }

        // 设置提示词管理器回调
        if (this.promptManager) {
            this.promptManager.addPromptsChangeCallback(function(prompts) {
                console.log('🎨 提示词列表变更，重新渲染 UI');
                self.refreshPromptList();
            });
        }

        // 设置弹窗回调
        if (this.promptModal) {
            this.promptModal.onSave = function(promptData, type) {
                self.handlePromptSave(promptData, type);
            };
        }
    };

    /**
     * 刷新提示词列表
     */
    PromptSettingsUI.prototype.refreshPromptList = function() {
        if (!this.promptList || !this.promptManager) {
            return;
        }

        const prompts = this.promptManager.getAllPrompts();
        
        if (prompts.length === 0) {
            this.promptList.innerHTML = this.createEmptyStateHTML();
        } else {
            this.promptList.innerHTML = prompts.map(prompt => 
                this.createPromptItemHTML(prompt)
            ).join('');
            
            // 设置项目事件监听器
            this.setupPromptItemEvents();
        }

        // 更新翻译
        this.updateTranslations();

        // 更新自动提交下拉选单
        this.updateAutoSubmitSelect();
    };

    /**
     * 创建空状态 HTML
     */
    PromptSettingsUI.prototype.createEmptyStateHTML = function() {
        return `
            <div class="empty-state">
                <div style="font-size: 48px; margin-bottom: 12px;">📝</div>
                <div data-i18n="prompts.management.emptyState">
                    尚未建立任何常用提示词
                </div>
                <div style="font-size: 12px; color: var(--text-secondary); margin-top: 8px;" data-i18n="prompts.management.emptyHint">
                    点击上方「新增提示词」按钮开始建立您的第一个提示词模板
                </div>
            </div>
        `;
    };

    /**
     * 创建提示词项目 HTML
     */
    PromptSettingsUI.prototype.createPromptItemHTML = function(prompt) {
        const createdDate = this.formatDate(prompt.createdAt);
        const lastUsedDate = prompt.lastUsedAt ? this.formatDate(prompt.lastUsedAt) : null;
        const truncatedContent = this.truncateText(prompt.content, 80);
        const isAutoSubmit = prompt.isAutoSubmit || false;

        return `
            <div class="prompt-settings-item ${isAutoSubmit ? 'auto-submit-prompt' : ''}" data-prompt-id="${prompt.id}">
                <div class="prompt-settings-info">
                    <div class="prompt-settings-name">
                        ${isAutoSubmit ? '<span class="auto-submit-badge" title="自动提交提示词">⏰</span>' : ''}
                        ${Utils.escapeHtml(prompt.name)}
                    </div>
                    <div class="prompt-settings-content">${Utils.escapeHtml(truncatedContent)}</div>
                    <div class="prompt-settings-meta">
                        <span data-i18n="prompts.management.created">建立于</span>: ${createdDate}
                        ${lastUsedDate ? `| <span data-i18n="prompts.management.lastUsed">最近使用</span>: ${lastUsedDate}` : ''}
                        ${isAutoSubmit ? `| <span class="auto-submit-status" data-i18n="prompts.management.autoSubmit">自动提交</span>` : ''}
                    </div>
                </div>
                <div class="prompt-settings-actions">
                    <button type="button" class="prompt-action-btn auto-submit-btn ${isAutoSubmit ? 'active' : ''}"
                            data-prompt-id="${prompt.id}"
                            title="${isAutoSubmit ? '取消自动提交' : '设定为自动提交'}"
                            data-i18n="${isAutoSubmit ? 'prompts.management.cancelAutoSubmit' : 'prompts.management.setAutoSubmit'}">
                        ${isAutoSubmit ? '⏸️' : '⏰'}
                    </button>
                    <button type="button" class="prompt-action-btn edit-btn" data-prompt-id="${prompt.id}" data-i18n="prompts.management.edit">
                        编辑
                    </button>
                    <button type="button" class="prompt-action-btn delete-btn delete" data-prompt-id="${prompt.id}" data-i18n="prompts.management.delete">
                        删除
                    </button>
                </div>
            </div>
        `;
    };

    /**
     * 设置提示词项目事件监听器
     */
    PromptSettingsUI.prototype.setupPromptItemEvents = function() {
        const self = this;

        // 编辑按钮事件
        const editButtons = this.promptList.querySelectorAll('.edit-btn');
        editButtons.forEach(function(button) {
            button.addEventListener('click', function(e) {
                e.stopPropagation();
                const promptId = button.getAttribute('data-prompt-id');
                self.handleEditPrompt(promptId);
            });
        });

        // 删除按钮事件
        const deleteButtons = this.promptList.querySelectorAll('.delete-btn');
        deleteButtons.forEach(function(button) {
            button.addEventListener('click', function(e) {
                e.stopPropagation();
                const promptId = button.getAttribute('data-prompt-id');
                self.handleDeletePrompt(promptId);
            });
        });

        // 自动提交按钮事件
        const autoSubmitButtons = this.promptList.querySelectorAll('.auto-submit-btn');
        autoSubmitButtons.forEach(function(button) {
            button.addEventListener('click', function(e) {
                e.stopPropagation();
                const promptId = button.getAttribute('data-prompt-id');
                self.handleToggleAutoSubmit(promptId);
            });
        });
    };

    /**
     * 处理新增提示词
     */
    PromptSettingsUI.prototype.handleAddPrompt = function() {
        if (!this.promptModal) {
            console.error('❌ PromptModal 未设定');
            return;
        }

        this.promptModal.showAddModal();
    };

    /**
     * 处理编辑提示词
     */
    PromptSettingsUI.prototype.handleEditPrompt = function(promptId) {
        if (!this.promptManager || !this.promptModal) {
            console.error('❌ PromptManager 或 PromptModal 未设定');
            return;
        }

        const prompt = this.promptManager.getPromptById(promptId);
        if (!prompt) {
            this.showError(this.t('prompts.management.notFound', '找不到指定的提示词'));
            return;
        }

        this.promptModal.showEditModal(prompt);
    };

    /**
     * 处理删除提示词
     */
    PromptSettingsUI.prototype.handleDeletePrompt = function(promptId) {
        if (!this.promptManager) {
            console.error('❌ PromptManager 未设定');
            return;
        }

        const prompt = this.promptManager.getPromptById(promptId);
        if (!prompt) {
            this.showError(this.t('prompts.management.notFound', '找不到指定的提示词'));
            return;
        }

        const confirmMessage = this.t('prompts.management.confirmDelete', '确定要删除此提示词吗？') + 
                              '\n\n' + prompt.name;

        if (confirm(confirmMessage)) {
            try {
                this.promptManager.deletePrompt(promptId);
                this.showSuccess(this.t('prompts.management.deleteSuccess', '提示词已删除'));
            } catch (error) {
                this.showError(error.message);
            }
        }
    };

    /**
     * 处理自动提交切换
     */
    PromptSettingsUI.prototype.handleToggleAutoSubmit = function(promptId) {
        if (!this.promptManager) {
            console.error('❌ PromptManager 未设定');
            return;
        }

        const prompt = this.promptManager.getPromptById(promptId);
        if (!prompt) {
            this.showError(this.t('prompts.management.notFound', '找不到指定的提示词'));
            return;
        }

        try {
            if (prompt.isAutoSubmit) {
                // 取消自动提交
                this.promptManager.clearAutoSubmitPrompt();
                this.showSuccess(this.t('prompts.management.autoSubmitCancelled', '已取消自动提交设定'));

                // 清空设定管理器中的自动提交设定
                if (this.settingsManager) {
                    this.settingsManager.set('autoSubmitPromptId', null);
                    this.settingsManager.set('autoSubmitEnabled', false);
                    console.log('🔄 已清空自动提交设定');
                } else {
                    console.warn('⚠️ settingsManager 未设定，无法清空自动提交设定');
                }
            } else {
                // 设定为自动提交
                this.promptManager.setAutoSubmitPrompt(promptId);
                this.showSuccess(this.t('prompts.management.autoSubmitSet', '已设定为自动提交提示词：') + prompt.name);

                // 更新设定管理器中的自动提交设定
                if (this.settingsManager) {
                    console.log('🔧 设定前的 autoSubmitPromptId:', this.settingsManager.get('autoSubmitPromptId'));
                    this.settingsManager.set('autoSubmitPromptId', promptId);
                    this.settingsManager.set('autoSubmitEnabled', true);
                    console.log('✅ 已设定自动提交提示词 ID:', promptId);
                    console.log('🔧 设定后的 autoSubmitPromptId:', this.settingsManager.get('autoSubmitPromptId'));
                } else {
                    console.warn('⚠️ settingsManager 未设定，无法更新自动提交设定');
                }
            }

            // 更新自动提交下拉选单
            this.updateAutoSubmitSelect();

            // 触发自动提交状态变更事件
            if (this.settingsManager && this.settingsManager.triggerAutoSubmitStateChange) {
                this.settingsManager.triggerAutoSubmitStateChange(prompt.isAutoSubmit);
            } else {
                console.warn('⚠️ settingsManager 或 triggerAutoSubmitStateChange 方法未设定');
            }
        } catch (error) {
            this.showError(error.message);
        }
    };

    /**
     * 更新自动提交下拉选单
     */
    PromptSettingsUI.prototype.updateAutoSubmitSelect = function() {
        console.log('🔄 updateAutoSubmitSelect 开始执行');
        const autoSubmitSelect = document.getElementById('autoSubmitPromptSelect');
        if (!autoSubmitSelect || !this.promptManager) {
            console.log('❌ updateAutoSubmitSelect: 缺少必要元素');
            return;
        }

        // 清空现有选项（保留第一个预设选项）
        while (autoSubmitSelect.children.length > 1) {
            autoSubmitSelect.removeChild(autoSubmitSelect.lastChild);
        }

        // 新增所有提示词选项
        const prompts = this.promptManager.getAllPrompts();
        let autoSubmitPromptId = null;
        console.log('🔄 updateAutoSubmitSelect 检查提示词:', prompts.map(p => ({id: p.id, name: p.name, isAutoSubmit: p.isAutoSubmit})));

        prompts.forEach(function(prompt) {
            const option = document.createElement('option');
            option.value = prompt.id;
            option.textContent = prompt.name;
            if (prompt.isAutoSubmit) {
                option.selected = true;
                autoSubmitPromptId = prompt.id;
                console.log('🔄 找到自动提交提示词:', prompt.name, prompt.id);
            }
            autoSubmitSelect.appendChild(option);
        });

        // 同步更新设定管理器中的自动提交提示词 ID
        if (this.settingsManager) {
            console.log('🔄 updateAutoSubmitSelect 设定前:', this.settingsManager.get('autoSubmitPromptId'));
            const currentAutoSubmitEnabled = this.settingsManager.get('autoSubmitEnabled');

            if (autoSubmitPromptId) {
                // 检查状态一致性：如果设定中的 promptId 与找到的不一致，以找到的为准
                const currentPromptId = this.settingsManager.get('autoSubmitPromptId');
                if (currentPromptId !== autoSubmitPromptId) {
                    console.log('🔧 状态不一致，修正 autoSubmitPromptId:', currentPromptId, '->', autoSubmitPromptId);
                    this.settingsManager.set('autoSubmitPromptId', autoSubmitPromptId);
                }

                // 不自动改变 autoSubmitEnabled 的值，完全尊重用户的设定
                // updateAutoSubmitSelect 只负责同步 promptId 和下拉选单显示
                console.log('🔄 updateAutoSubmitSelect 同步 promptId，保持 autoSubmitEnabled 状态:', {
                    promptId: autoSubmitPromptId,
                    enabled: currentAutoSubmitEnabled
                });
            } else {
                // 没有找到自动提交提示词，清空 promptId 但完全保留 enabled 状态
                this.settingsManager.set('autoSubmitPromptId', null);
                console.log('🔄 updateAutoSubmitSelect 清空 promptId，完全保留 autoSubmitEnabled 状态:', currentAutoSubmitEnabled);
            }
            console.log('🔄 updateAutoSubmitSelect 设定后:', {
                promptId: this.settingsManager.get('autoSubmitPromptId'),
                enabled: this.settingsManager.get('autoSubmitEnabled')
            });
        } else {
            console.warn('⚠️ updateAutoSubmitSelect: settingsManager 未设定，无法同步设定');
        }
    };

    /**
     * 处理提示词保存
     */
    PromptSettingsUI.prototype.handlePromptSave = function(promptData, type) {
        if (!this.promptManager) {
            console.error('❌ PromptManager 未设定');
            return;
        }

        try {
            if (type === 'add') {
                this.promptManager.addPrompt(promptData.name, promptData.content);
                this.showSuccess(this.t('prompts.management.addSuccess', '提示词已新增'));
            } else if (type === 'edit') {
                this.promptManager.updatePrompt(promptData.id, promptData.name, promptData.content);
                this.showSuccess(this.t('prompts.management.updateSuccess', '提示词已更新'));
            }

            // 更新自动提交下拉选单
            this.updateAutoSubmitSelect();
        } catch (error) {
            throw error; // 重新抛出错误，让弹窗处理
        }
    };

    /**
     * 更新翻译
     */
    PromptSettingsUI.prototype.updateTranslations = function() {
        if (window.i18nManager && typeof window.i18nManager.applyTranslations === 'function') {
            window.i18nManager.applyTranslations();
        }
    };

    /**
     * 显示成功讯息
     */
    PromptSettingsUI.prototype.showSuccess = function(message) {
        if (window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.showMessage) {
            window.MCPFeedback.Utils.showMessage(message, 'success');
        } else {
            console.log('✅', message);
        }
    };

    /**
     * 显示错误讯息
     */
    PromptSettingsUI.prototype.showError = function(message) {
        if (window.MCPFeedback && window.MCPFeedback.Utils && window.MCPFeedback.Utils.showMessage) {
            window.MCPFeedback.Utils.showMessage(message, 'error');
        } else {
            alert(message);
        }
    };

    /**
     * 翻译函数
     */
    PromptSettingsUI.prototype.t = function(key, fallback) {
        if (window.i18nManager && typeof window.i18nManager.t === 'function') {
            return window.i18nManager.t(key, fallback);
        }
        return fallback || key;
    };

    /**
     * 格式化日期
     */
    PromptSettingsUI.prototype.formatDate = function(dateString) {
        if (!dateString) return '';
        
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        } catch (error) {
            return dateString;
        }
    };

    /**
     * 截断文字
     */
    PromptSettingsUI.prototype.truncateText = function(text, maxLength) {
        if (!text || text.length <= maxLength) {
            return text;
        }
        return text.substring(0, maxLength) + '...';
    };

    // 将 PromptSettingsUI 加入命名空间
    window.MCPFeedback.Prompt.PromptSettingsUI = PromptSettingsUI;

    console.log('✅ PromptSettingsUI 模组载入完成');

})();
