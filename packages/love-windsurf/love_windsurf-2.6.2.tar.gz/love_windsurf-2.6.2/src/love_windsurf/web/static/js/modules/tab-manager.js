/**
 * MCP Feedback Enhanced - 标签页管理模组
 * ====================================
 * 
 * 处理多标签页状态同步和智能浏览器管理
 */

(function() {
    'use strict';

    // 确保命名空间和依赖存在
    window.MCPFeedback = window.MCPFeedback || {};
    const Utils = window.MCPFeedback.Utils;

    /**
     * 标签页管理器建构函数
     */
    function TabManager() {
        this.tabId = Utils.generateId('tab');
        this.heartbeatInterval = null;
        this.heartbeatFrequency = Utils.CONSTANTS.DEFAULT_TAB_HEARTBEAT_FREQUENCY;
        this.storageKey = 'mcp_feedback_tabs';
        this.lastActivityKey = 'mcp_feedback_last_activity';

        this.init();
    }

    /**
     * 初始化标签页管理器
     */
    TabManager.prototype.init = function() {
        // 注册当前标签页
        this.registerTab();

        // 向服务器注册标签页
        this.registerTabToServer();

        // 开始心跳
        this.startHeartbeat();

        // 监听页面关闭事件
        const self = this;
        window.addEventListener('beforeunload', function() {
            self.unregisterTab();
        });

        // 监听 localStorage 变化（其他标签页的状态变化）
        window.addEventListener('storage', function(e) {
            if (e.key === self.storageKey) {
                self.handleTabsChange();
            }
        });

        console.log('📋 TabManager 初始化完成，标签页 ID: ' + this.tabId);
    };

    /**
     * 注册当前标签页
     */
    TabManager.prototype.registerTab = function() {
        const tabs = this.getActiveTabs();
        tabs[this.tabId] = {
            timestamp: Date.now(),
            url: window.location.href,
            active: true
        };
        
        if (Utils.isLocalStorageSupported()) {
            localStorage.setItem(this.storageKey, JSON.stringify(tabs));
        }
        
        this.updateLastActivity();
        console.log('✅ 标签页已注册: ' + this.tabId);
    };

    /**
     * 注销当前标签页
     */
    TabManager.prototype.unregisterTab = function() {
        const tabs = this.getActiveTabs();
        delete tabs[this.tabId];
        
        if (Utils.isLocalStorageSupported()) {
            localStorage.setItem(this.storageKey, JSON.stringify(tabs));
        }
        
        console.log('❌ 标签页已注销: ' + this.tabId);
    };

    /**
     * 开始心跳
     */
    TabManager.prototype.startHeartbeat = function() {
        const self = this;
        this.heartbeatInterval = setInterval(function() {
            self.sendHeartbeat();
        }, this.heartbeatFrequency);
    };

    /**
     * 发送心跳
     */
    TabManager.prototype.sendHeartbeat = function() {
        const tabs = this.getActiveTabs();
        if (tabs[this.tabId]) {
            tabs[this.tabId].timestamp = Date.now();
            
            if (Utils.isLocalStorageSupported()) {
                localStorage.setItem(this.storageKey, JSON.stringify(tabs));
            }
            
            this.updateLastActivity();
        }
    };

    /**
     * 更新最后活动时间
     */
    TabManager.prototype.updateLastActivity = function() {
        if (Utils.isLocalStorageSupported()) {
            localStorage.setItem(this.lastActivityKey, Date.now().toString());
        }
    };

    /**
     * 获取活跃标签页
     */
    TabManager.prototype.getActiveTabs = function() {
        if (!Utils.isLocalStorageSupported()) {
            return {};
        }

        try {
            const stored = localStorage.getItem(this.storageKey);
            const tabs = stored ? Utils.safeJsonParse(stored, {}) : {};

            // 清理过期的标签页
            const now = Date.now();
            const expiredThreshold = Utils.CONSTANTS.TAB_EXPIRED_THRESHOLD;

            for (const tabId in tabs) {
                if (tabs.hasOwnProperty(tabId)) {
                    if (now - tabs[tabId].timestamp > expiredThreshold) {
                        delete tabs[tabId];
                    }
                }
            }

            return tabs;
        } catch (error) {
            console.error('获取活跃标签页失败:', error);
            return {};
        }
    };

    /**
     * 检查是否有活跃标签页
     */
    TabManager.prototype.hasActiveTabs = function() {
        const tabs = this.getActiveTabs();
        return Object.keys(tabs).length > 0;
    };

    /**
     * 检查是否为唯一活跃标签页
     */
    TabManager.prototype.isOnlyActiveTab = function() {
        const tabs = this.getActiveTabs();
        return Object.keys(tabs).length === 1 && tabs[this.tabId];
    };

    /**
     * 处理其他标签页状态变化
     */
    TabManager.prototype.handleTabsChange = function() {
        console.log('🔄 检测到其他标签页状态变化');
        // 可以在这里添加更多逻辑
    };

    /**
     * 向服务器注册标签页
     */
    TabManager.prototype.registerTabToServer = function() {
        const self = this;
        
        fetch('/api/register-tab', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                tabId: this.tabId
            })
        })
        .then(function(response) {
            if (response.ok) {
                return response.json();
            } else {
                console.warn('⚠️ 标签页服务器注册失败: ' + response.status);
            }
        })
        .then(function(data) {
            if (data) {
                console.log('✅ 标签页已向服务器注册: ' + self.tabId);
            }
        })
        .catch(function(error) {
            console.warn('⚠️ 标签页服务器注册错误: ' + error);
        });
    };

    /**
     * 清理资源
     */
    TabManager.prototype.cleanup = function() {
        if (this.heartbeatInterval) {
            clearInterval(this.heartbeatInterval);
            this.heartbeatInterval = null;
        }
        this.unregisterTab();
    };

    /**
     * 获取当前标签页 ID
     */
    TabManager.prototype.getTabId = function() {
        return this.tabId;
    };

    // 将 TabManager 加入命名空间
    window.MCPFeedback.TabManager = TabManager;

    console.log('✅ TabManager 模组载入完成');

})();