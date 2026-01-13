// ========== 全局变量 ==========
let busy = false, currentSessionId = null, editingSessionId = null, toolIdCounter = 0;
let editingModelKey = null, editingProviderId = null, confirmCallback = null;
let editingMsgId = null, editingMsgRole = null;
let currentModelKey = null;
let editingMCPId = null;
let toolsEnabled = true;  // 从后端获取

// ========== 移动端侧边栏控制 ==========
function toggleMobileSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.getElementById('mobileSidebarOverlay');
    sidebar.classList.toggle('mobile-open');
    overlay.classList.toggle('show');
}

function closeMobileSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.getElementById('mobileSidebarOverlay');
    sidebar.classList.remove('mobile-open');
    overlay.classList.remove('show');
}

// ========== 工具函数 ==========
function getUser() { return document.getElementById('username').value.trim() || 'guest'; }
function escapeHtml(text) { const div = document.createElement('div'); div.textContent = text; return div.innerHTML; }

// Markdown 渲染配置
if (typeof marked !== 'undefined') {
    marked.setOptions({
        breaks: true,        // 支持换行
        gfm: true,           // GitHub 风格 Markdown
        headerIds: false,    // 禁用标题 ID（避免样式冲突）
        mangle: false        // 禁用邮箱地址混淆
    });
}

// LaTeX 公式预处理：保护公式不被 Markdown 解析器破坏
function protectLatex(text) {
    const placeholders = [];
    let idx = 0;
    
    // 保护块级公式 $$...$$ 和 \[...\]
    text = text.replace(/\$\$([\s\S]*?)\$\$/g, (match, p1) => {
        placeholders.push({ type: 'block', content: p1 });
        return `%%LATEX_BLOCK_${idx++}%%`;
    });
    text = text.replace(/\\\[([\s\S]*?)\\\]/g, (match, p1) => {
        placeholders.push({ type: 'block', content: p1 });
        return `%%LATEX_BLOCK_${idx++}%%`;
    });
    
    // 保护行内公式 $...$ 和 \(...\)
    text = text.replace(/\$([^\$\n]+?)\$/g, (match, p1) => {
        placeholders.push({ type: 'inline', content: p1 });
        return `%%LATEX_INLINE_${idx++}%%`;
    });
    text = text.replace(/\\\(([\s\S]*?)\\\)/g, (match, p1) => {
        placeholders.push({ type: 'inline', content: p1 });
        return `%%LATEX_INLINE_${idx++}%%`;
    });
    
    return { text, placeholders };
}

// 还原 LaTeX 公式并渲染
function restoreAndRenderLatex(html, placeholders) {
    if (!placeholders.length) return html;
    
    placeholders.forEach((p, i) => {
        let rendered;
        try {
            if (typeof katex !== 'undefined') {
                rendered = katex.renderToString(p.content, {
                    displayMode: p.type === 'block',
                    throwOnError: false,
                    trust: true
                });
            } else {
                // KaTeX 未加载，显示原始公式
                rendered = p.type === 'block' ? `$$${p.content}$$` : `$${p.content}$`;
            }
        } catch (e) {
            console.error('LaTeX 渲染失败:', e);
            rendered = `<span class="latex-error" title="${escapeHtml(e.message)}">${escapeHtml(p.content)}</span>`;
        }
        
        const placeholder = p.type === 'block' ? `%%LATEX_BLOCK_${i}%%` : `%%LATEX_INLINE_${i}%%`;
        html = html.replace(placeholder, rendered);
    });
    
    return html;
}

function fmt(t) {
    if (!t) return '';
    
    // 先保护 LaTeX 公式
    const { text: protectedText, placeholders } = protectLatex(t);
    
    // 使用 marked 渲染 Markdown
    let html;
    if (typeof marked !== 'undefined') {
        try {
            html = marked.parse(protectedText);
        } catch (e) {
            console.error('Markdown 渲染失败:', e);
            html = protectedText;
        }
    } else {
        // 降级处理：简单的文本格式化
        html = escapeHtml(protectedText);
        html = html.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
        html = html.replace(/\n/g, '<br>');
    }
    
    // 还原并渲染 LaTeX 公式
    html = restoreAndRenderLatex(html, placeholders);
    
    return html;
}

// ========== Toast 通知系统 ==========
const toastIcons = {
    success: '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
    error: '<circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>',
    warning: '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    info: '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>'
};

function showToast(message, type = 'info', duration = 3000) {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
                <svg class="toast-icon ${type}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">${toastIcons[type] || toastIcons.info}</svg>
                <div class="toast-content">${escapeHtml(message)}</div>
                <button class="toast-close" onclick="this.parentElement.remove()">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                </button>
            `;
    container.appendChild(toast);
    if (duration > 0) {
        setTimeout(() => {
            toast.classList.add('hiding');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }
}

// ========== Alert 对话框系统 ==========
const alertIcons = {
    error: '<circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>',
    warning: '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    info: '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>'
};

function showAlert(message, title = '提示', type = 'info') {
    const modal = document.getElementById('alertModal');
    const icon = document.getElementById('alertIcon');
    const titleEl = document.getElementById('alertTitle');
    const bodyEl = document.getElementById('alertBody');
    icon.innerHTML = alertIcons[type] || alertIcons.info;
    icon.className = 'alert-icon ' + type;
    titleEl.textContent = title;

    // 支持 HTML 内容 - 检查是否包含 HTML 标签
    const hasHtml = message.indexOf('<') !== -1 && message.indexOf('>') !== -1;
    if (hasHtml) {
        bodyEl.innerHTML = message;
    } else {
        bodyEl.textContent = message;
    }

    modal.classList.add('show');
}

function closeAlert() {
    document.getElementById('alertModal').classList.remove('show');
}

// ========== 主题 ==========
const iconSun = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
const iconMoon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
const iconEdit = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>';
const iconDelete = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M3 6h18"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>';
const iconCopy = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';
const iconRefresh = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>';
const iconTokens = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>';
const iconBrain = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M12 2a4 4 0 0 0-4 4v1a4 4 0 0 0-4 4c0 1.5.8 2.8 2 3.4V16a4 4 0 0 0 4 4h4a4 4 0 0 0 4-4v-1.6c1.2-.6 2-1.9 2-3.4a4 4 0 0 0-4-4V6a4 4 0 0 0-4-4z"/><path d="M12 2v20"/><path d="M8 6h8"/><path d="M6 11h12"/></svg>';
const iconSettings = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>';
const iconPlus = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>';
const iconWarning = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>';
const iconEditLg = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>';
const iconTool = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>';
const iconServer = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"/><rect x="2" y="14" width="20" height="8" rx="2" ry="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/></svg>';
const iconLink = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>';
const iconEye = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>';

// 模型标签配置 - 使用SVG图标
const MODEL_TAGS = {
    'tool': { label: '工具', color: '#10b981', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>' },
    'reasoning': { label: '推理', color: '#f59e0b', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><path d="M12 2a4 4 0 0 0-4 4v1a4 4 0 0 0-4 4c0 1.5.8 2.8 2 3.4V16a4 4 0 0 0 4 4h4a4 4 0 0 0 4-4v-1.6c1.2-.6 2-1.9 2-3.4a4 4 0 0 0-4-4V6a4 4 0 0 0-4-4z"/></svg>' },
    'vision': { label: '视觉', color: '#6366f1', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>' }
};

function renderModelTags(tags) {
    if (!tags || tags.length === 0) return '';
    return tags.map(tag => {
        const config = MODEL_TAGS[tag] || { label: tag, color: '#6b7280', icon: '' };
        return `<span class="model-tag" style="background:${config.color}20;color:${config.color};border:1px solid ${config.color}40;">${config.icon}</span>`;
    }).join('');
}

// 模型类型配置
const MODEL_TYPES = {
    'chat': { label: '对话', color: '#6366f1', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>' },
    'embedding': { label: '嵌入', color: '#8b5cf6', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="8"/><line x1="12" y1="2" x2="12" y2="4"/><line x1="12" y1="20" x2="12" y2="22"/><line x1="2" y1="12" x2="4" y2="12"/><line x1="20" y1="12" x2="22" y2="12"/></svg>' }
};

function renderModelType(type) {
    const config = MODEL_TYPES[type] || MODEL_TYPES['chat'];
    return `<span class="model-type-tag" style="background:${config.color}20;color:${config.color};border:1px solid ${config.color}40;">${config.icon} ${config.label}</span>`;
}

function toggleTheme() {
    const html = document.documentElement;
    const current = localStorage.getItem('nex_theme');
    let newTheme;
    if (current === 'auto' || !current) {
        newTheme = 'light';
    } else if (current === 'light') {
        newTheme = 'dark';
    } else {
        newTheme = 'auto';
    }
    localStorage.setItem('nex_theme', newTheme);
    applyTheme(newTheme);
    updateThemeIcon();
}

function applyTheme(theme) {
    const html = document.documentElement;
    if (theme === 'auto') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        html.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
    } else {
        html.setAttribute('data-theme', theme);
    }
}

function updateThemeIcon() {
    const btn = document.getElementById('themeBtn');
    if (!btn) return; // 如果按钮不存在，直接返回
    const saved = localStorage.getItem('nex_theme') || 'auto';
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    if (saved === 'auto') {
        btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>';
        btn.title = '跟随系统 (点击切换到浅色)';
    } else if (isDark) {
        btn.innerHTML = iconSun;
        btn.title = '深色模式 (点击切换到跟随系统)';
    } else {
        btn.innerHTML = iconMoon;
        btn.title = '浅色模式 (点击切换到深色)';
    }
}

async function initTheme() {
    // 设置默认值
    window.avatarMode = 'icon';  // icon, text, hide
    window.currentPersonaAvatar = '';
    
    // 先应用 localStorage 中的主题（避免闪烁）
    const localTheme = localStorage.getItem('nex_theme') || 'auto';
    applyTheme(localTheme);
    updateThemeIcon();

    // 监听系统主题变化
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
        if (localStorage.getItem('nex_theme') === 'auto') {
            applyTheme('auto');
        }
    });

    // 从数据库加载样式设置（会覆盖 localStorage）
    await loadStyleSettings();
}

async function loadCustomAvatar() {
    // 角色卡头像在 updatePersonaDisplay 中加载
}

function updateAvatarPreview() {
    // 不再需要全局头像预览
}

function setAvatarMode(mode) {
    window.avatarMode = mode;
    fetch('/nex/settings', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ settings: { avatar_mode: mode } })
    });
    updateAvatarModeUI();
    // 自动刷新消息
    if (currentSessionId) {
        loadMessages(currentSessionId);
    }
}

function updateAvatarModeUI() {
    document.getElementById('avatarIcon')?.classList.toggle('active', window.avatarMode === 'icon');
    document.getElementById('avatarText')?.classList.toggle('active', window.avatarMode === 'text');
    document.getElementById('avatarHide')?.classList.toggle('active', window.avatarMode === 'hide');
}
// ========== 样式设置 ==========
async function loadStyleSettings() {
    try {
        const r = await fetch('/nex/settings');
        const d = await r.json();
        const settings = d.data || {};
        console.log('加载样式设置:', settings);

        // 应用主题模式（优先级最高，先应用）
        if (settings.theme_mode && settings.theme_mode !== '') {
            localStorage.setItem('nex_theme', settings.theme_mode);
            applyTheme(settings.theme_mode);
            updateThemeIcon();
        }

        // 应用主题色
        if (settings.accent_color && settings.accent_color !== '') {
            console.log('应用主题色:', settings.accent_color);
            applyAccentColor(settings.accent_color);
        }

        // 应用字体大小
        if (settings.font_size && settings.font_size !== '') {
            console.log('应用字体大小:', settings.font_size);
            applyFontSize(settings.font_size);
        }

        // 应用头像模式设置
        if (settings.avatar_mode && settings.avatar_mode !== '') {
            window.avatarMode = settings.avatar_mode;
        } else {
            window.avatarMode = 'icon';  // 默认消息图标模式
        }
    } catch (e) { console.error('加载样式设置失败', e); }
}

function setThemeMode(mode) {
    localStorage.setItem('nex_theme', mode);
    applyTheme(mode);
    updateThemeIcon();
    updateStylePanelUI();
    saveStyleSetting('theme_mode', mode);
}

function setAccentColor(color) {
    applyAccentColor(color);
    // 更新颜色选项的选中状态
    document.querySelectorAll('.color-option').forEach(btn => {
        btn.classList.remove('active');
        if (!btn.classList.contains('custom')) {
            const btnColor = getComputedStyle(btn).getPropertyValue('--color').trim();
            if (btnColor === color) btn.classList.add('active');
        }
    });
    // 重置自定义按钮
    const customBtn = document.getElementById('customColorBtn');
    if (customBtn) {
        customBtn.style.background = '';
        customBtn.classList.remove('active');
    }
    // 隐藏自定义输入区域
    const customInput = document.getElementById('customColorInput');
    if (customInput) customInput.style.display = 'none';

    saveStyleSetting('accent_color', color);
}

function showCustomColorInput() {
    const customInput = document.getElementById('customColorInput');
    const customText = document.getElementById('customColorText');
    const previewBox = document.getElementById('customColorPreviewBox');
    const currentColor = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim();

    if (customInput.style.display === 'none' || customInput.style.display === '') {
        customInput.style.display = 'flex';
        customText.value = currentColor;
        previewBox.style.background = currentColor;
        customText.focus();
        customText.select();
    } else {
        customInput.style.display = 'none';
    }
}

function previewCustomColor(value) {
    const previewBox = document.getElementById('customColorPreviewBox');
    // 验证是否是有效的十六进制颜色
    if (/^#[0-9A-Fa-f]{6}$/.test(value)) {
        previewBox.style.background = value;
    } else if (/^[0-9A-Fa-f]{6}$/.test(value)) {
        previewBox.style.background = '#' + value;
    }
}

function applyCustomColorFromInput() {
    let value = document.getElementById('customColorText').value.trim();
    // 自动补全 #
    if (/^[0-9A-Fa-f]{6}$/.test(value)) {
        value = '#' + value;
    }
    // 验证格式
    if (!/^#[0-9A-Fa-f]{6}$/.test(value)) {
        showToast('请输入有效的颜色值，如 #6366f1', 'warning');
        return;
    }

    applyAccentColor(value);
    // 取消所有预设颜色的选中
    document.querySelectorAll('.color-option:not(.custom)').forEach(btn => btn.classList.remove('active'));
    // 设置自定义按钮的颜色和选中状态
    const customBtn = document.getElementById('customColorBtn');
    if (customBtn) {
        customBtn.style.background = value;
        customBtn.classList.add('active');
    }
    saveStyleSetting('accent_color', value);
    showToast('颜色已应用', 'success');
}

function applyAccentColor(color) {
    if (!color || color === '') return;
    // 确保颜色格式正确
    color = color.trim().toLowerCase();
    if (!color.startsWith('#')) {
        color = '#' + color;
    }
    console.log('应用主题色到CSS:', color);
    document.documentElement.style.setProperty('--accent', color);
    // 计算hover颜色（稍微深一点）
    const hoverColor = adjustColor(color, -20);
    document.documentElement.style.setProperty('--accent-hover', hoverColor);
    // 更新用户消息背景色
    document.documentElement.style.setProperty('--user', color);
}

function adjustColor(color, amount) {
    // 简单的颜色调整函数
    const hex = color.replace('#', '');
    const r = Math.max(0, Math.min(255, parseInt(hex.substr(0, 2), 16) + amount));
    const g = Math.max(0, Math.min(255, parseInt(hex.substr(2, 2), 16) + amount));
    const b = Math.max(0, Math.min(255, parseInt(hex.substr(4, 2), 16) + amount));
    return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
}

function setFontSize(size) {
    applyFontSize(size);
    updateStylePanelUI();
    saveStyleSetting('font_size', size);
}

function applyFontSize(size) {
    if (!size || size === '') return;
    const sizes = { small: '14px', medium: '16px', large: '18px' };
    const fontSize = sizes[size] || '16px';
    console.log('应用字体大小到CSS:', fontSize);
    document.documentElement.style.setProperty('font-size', fontSize);
}

async function saveStyleSetting(key, value) {
    console.log('保存样式设置:', key, '=', value);
    try {
        const r = await fetch('/nex/settings', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ settings: { [key]: value } })
        });
        const d = await r.json();
        console.log('保存结果:', d);
    } catch (e) { console.error('保存样式设置失败', e); }
}
function updateStylePanelUI() {
    // 更新主题模式按钮
    const themeMode = localStorage.getItem('nex_theme') || 'auto';
    document.getElementById('themeLight')?.classList.remove('active');
    document.getElementById('themeDark')?.classList.remove('active');
    document.getElementById('themeAuto')?.classList.remove('active');
    if (themeMode === 'light') document.getElementById('themeLight')?.classList.add('active');
    else if (themeMode === 'dark') document.getElementById('themeDark')?.classList.add('active');
    else document.getElementById('themeAuto')?.classList.add('active');

    // 更新颜色选择
    const currentColor = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim().toLowerCase();
    const presetColors = ['#6366f1', '#8b5cf6', '#ec4899', '#ef4444', '#f97316', '#eab308', '#22c55e', '#14b8a6', '#0ea5e9'];
    let isPreset = false;

    document.querySelectorAll('.color-option:not(.custom)').forEach(btn => {
        btn.classList.remove('active');
        const btnColor = getComputedStyle(btn).getPropertyValue('--color').trim().toLowerCase();
        if (btnColor === currentColor) {
            btn.classList.add('active');
            isPreset = true;
        }
    });

    // 如果不是预设颜色，显示为自定义
    const customBtn = document.getElementById('customColorBtn');
    const customInput = document.getElementById('customColorInput');
    const customText = document.getElementById('customColorText');
    const previewBox = document.getElementById('customColorPreviewBox');

    if (customBtn) {
        if (!isPreset && currentColor && currentColor !== '#6366f1') {
            customBtn.style.background = currentColor;
            customBtn.classList.add('active');
        } else {
            customBtn.style.background = '';
            customBtn.classList.remove('active');
        }
    }
    if (customText) customText.value = currentColor;
    if (previewBox) previewBox.style.background = currentColor;

    // 更新字体大小按钮
    const fontSize = document.documentElement.style.fontSize || '16px';
    const sizeMap = { '14px': 0, '16px': 1, '18px': 2 };
    const currentSizeIdx = sizeMap[fontSize] ?? 1;
    const fontSizeSection = document.querySelectorAll('#panel-style .style-section')[2];
    if (fontSizeSection) {
        fontSizeSection.querySelectorAll('.style-option').forEach((btn, i) => {
            btn.classList.toggle('active', i === currentSizeIdx);
        });
    }

    // 更新头像模式按钮
    updateAvatarModeUI();
    updateAvatarPreview();
}

async function resetStyleSettings() {
    // 重置为默认值
    localStorage.setItem('nex_theme', 'auto');
    applyTheme('auto');
    applyAccentColor('#6366f1');
    document.documentElement.style.removeProperty('font-size');
    window.avatarMode = 'icon';
    updateStylePanelUI();

    // 保存到数据库
    try {
        await fetch('/nex/settings', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ settings: { theme_mode: 'auto', accent_color: '#6366f1', font_size: 'medium', avatar_mode: 'icon' } })
        });
        showToast('已恢复默认设置', 'success');
        // 刷新消息列表以应用头像设置
        if (typeof loadMessages === 'function' && currentSessionId) {
            loadMessages(currentSessionId);
        }
    } catch (e) {
        console.error('重置失败', e);
        showToast('重置失败', 'error');
    }
}

// ========== 工具卡片 ==========
function createToolCardHtml(name, args, result, id) {
    const isDone = result !== undefined;
    return `<div class="tool-card" id="tool-${id}">
        <div class="tool-header" onclick="toggleTool('${id}')">
            <div class="tool-title"><span class="icon">${iconTool}</span><span>${escapeHtml(name)}</span>
                <span class="tool-status ${isDone ? 'done' : 'running'}">${isDone ? '完成' : '运行中'}</span></div>
            <span class="tool-arrow">▼</span>
        </div>
        <div class="tool-body"><div class="tool-content">
            <div class="tool-section"><div class="tool-section-title">参数</div><pre>${escapeHtml(JSON.stringify(args, null, 2))}</pre></div>
            ${isDone ? `<div class="tool-section"><div class="tool-section-title">结果</div><pre>${escapeHtml(result)}</pre></div>` : '<div class="tool-section tool-result" style="display:none"><div class="tool-section-title">结果</div><pre></pre></div>'}
        </div></div>
    </div>`;
}

function toggleTool(id) { document.getElementById('tool-' + id)?.classList.toggle('open'); }

function updateToolResult(id, result) {
    const card = document.getElementById('tool-' + id);
    if (!card) return;
    card.querySelector('.tool-status').className = 'tool-status done';
    card.querySelector('.tool-status').textContent = '完成';
    const rs = card.querySelector('.tool-result');
    if (rs) { rs.style.display = 'block'; rs.querySelector('pre').textContent = result; }
}

// ========== 思考过程卡片 ==========
function createThinkingCardHtml(content, id, isDone = true) {
    return `<div class="tool-card thinking" id="thinking-${id}">
        <div class="tool-header" onclick="toggleThinking('${id}')">
            <div class="tool-title"><span class="icon">${iconBrain}</span><span>深度思考</span>
                <span class="tool-status ${isDone ? 'done' : 'running'}">${isDone ? '完成' : '思考中...'}</span></div>
            <span class="tool-arrow">▼</span>
        </div>
        <div class="tool-body"><div class="tool-content">
            <div class="tool-section"><div class="tool-section-title">思考过程</div><pre id="thinking-content-${id}">${escapeHtml(content || '')}</pre></div>
        </div></div>
    </div>`;
}

function toggleThinking(id) { document.getElementById('thinking-' + id)?.classList.toggle('open'); }

function updateThinkingContent(id, content, isDone = false) {
    const card = document.getElementById('thinking-' + id);
    if (!card) return;
    const pre = document.getElementById('thinking-content-' + id);
    if (pre) pre.textContent = content;
    if (isDone) {
        card.querySelector('.tool-status').className = 'tool-status done';
        card.querySelector('.tool-status').textContent = '完成';
    }
}

// ========== 会话列表（角色卡分组） ==========
let allGroupedData = [];
let expandedPersonas = new Set(['default']);

async function loadSessions() {
    await loadPersonaGroupedSessions();
}

async function loadPersonaGroupedSessions() {
    try {
        const r = await fetch('/nex/sessions/grouped');
        const d = await r.json();
        allGroupedData = d.data || [];
        renderPersonaList(allGroupedData);

        // 如果没有当前会话，选择第一个
        if (!currentSessionId) {
            for (const group of allGroupedData) {
                if (group.sessions && group.sessions.length > 0) {
                    currentSessionId = group.sessions[0].id;
                    const personaId = group.persona ? group.persona.id : 'default';
                    expandedPersonas.add(personaId);
                    break;
                }
            }
        }

        if (currentSessionId) {
            for (const group of allGroupedData) {
                const session = group.sessions?.find(s => s.id === currentSessionId);
                if (session) {
                    const personaId = group.persona ? group.persona.id : 'default';
                    expandedPersonas.add(personaId);
                    break;
                }
            }
            renderPersonaList(allGroupedData);
            // 先更新角色显示（设置 window.currentPersonaAvatar），再加载消息
            await updatePersonaDisplay();
            await loadMessages(currentSessionId);
        } else {
            // 没有会话时显示欢迎界面
            document.getElementById('sessionTitle').textContent = 'NexAgent';
            document.getElementById('currentPersonaName').textContent = '';
            window.currentPersonaAvatar = '';
            showWelcomeState();
        }
    } catch (e) { console.error('加载分组会话失败', e); }
}

function renderPersonaList(groupedData) {
    const list = document.getElementById('personaList');
    const searchText = document.getElementById('sessionSearch')?.value?.toLowerCase().trim() || '';

    if (!groupedData || groupedData.length === 0) {
        list.innerHTML = '<div style="padding:20px;color:var(--text2);text-align:center">暂无会话<br><span style="font-size:0.85rem">点击"新建"开始</span></div>';
        return;
    }

    let html = '';
    let hasVisibleContent = false;

    for (const group of groupedData) {
        const persona = group.persona;
        const sessions = group.sessions || [];
        const personaId = persona ? persona.id : 'default';
        const personaName = persona ? persona.name : '默认助手';
        const isExpanded = expandedPersonas.has(personaId);

        let filteredSessions = sessions;
        if (searchText) {
            filteredSessions = sessions.filter(s =>
                s.name.toLowerCase().includes(searchText) ||
                (s.user && s.user.toLowerCase().includes(searchText))
            );
            if (personaName.toLowerCase().includes(searchText)) {
                filteredSessions = sessions;
            }
            if (filteredSessions.length === 0 && !personaName.toLowerCase().includes(searchText)) {
                continue;
            }
        }

        hasVisibleContent = true;
        const sessionCount = filteredSessions.length;
        const firstLetter = personaName.charAt(0).toUpperCase();
        const bgColor = persona ? getPersonaColor(persona.id) : 'var(--text2)';
        const personaAvatar = persona?.avatar;
        
        // 角色图标：有头像用头像，没有用首字母
        const iconHtml = personaAvatar 
            ? `<img src="${personaAvatar}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">`
            : firstLetter;

        html += `
                    <div class="persona-group ${isExpanded ? 'expanded' : ''}" data-persona-id="${personaId}">
                        <div class="persona-group-header" onclick="togglePersonaGroup(${persona ? persona.id : "'default'"})">
                            <div class="persona-group-icon" style="background:${personaAvatar ? 'transparent' : bgColor}">${iconHtml}</div>
                            <div class="persona-group-info">
                                <div class="persona-group-name">${escapeHtml(personaName)}</div>
                                <div class="persona-group-meta">${sessionCount} 个会话</div>
                            </div>
                            <div class="persona-group-arrow">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="18" height="18">
                                    <polyline points="6 9 12 15 18 9"/>
                                </svg>
                            </div>
                        </div>
                        <div class="persona-sessions">
                            ${filteredSessions.map(s => `
                                <div class="persona-session-item ${s.id === currentSessionId ? 'active' : ''}" data-id="${s.id}" onclick="switchSession(${s.id})">
                                    <div class="persona-session-info">
                                        <div class="persona-session-name">${escapeHtml(s.name)}</div>
                                        <div class="persona-session-meta">${s.message_count || 0}条消息 · ${s.user || 'guest'}</div>
                                    </div>
                                    <div class="persona-session-actions">
                                        <button class="btn-icon" onclick="event.stopPropagation();editSession(${s.id},'${escapeHtml(s.name).replace(/'/g, "\\'")}')" title="编辑">${iconEdit}</button>
                                        <button class="btn-icon delete" onclick="event.stopPropagation();deleteSession(${s.id})" title="删除">${iconDelete}</button>
                                    </div>
                                </div>
                            `).join('')}
                            <div class="persona-add-session" onclick="createSessionForPersona(${persona ? persona.id : 'null'})">
                                + 新建会话
                            </div>
                        </div>
                    </div>
                `;
    }

    if (!hasVisibleContent) {
        list.innerHTML = '<div style="padding:20px;color:var(--text2);text-align:center">没有找到匹配的会话</div>';
    } else {
        list.innerHTML = html;
    }
}

function getPersonaColor(id) {
    const colors = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'];
    return colors[id % colors.length];
}

function togglePersonaGroup(personaId) {
    // personaId 可能是数字或字符串 'default'
    const key = personaId === 'default' ? 'default' : (typeof personaId === 'number' ? personaId : parseInt(personaId));
    if (expandedPersonas.has(key)) {
        expandedPersonas.delete(key);
    } else {
        expandedPersonas.add(key);
    }
    renderPersonaList(allGroupedData);
}

async function switchSession(id) {
    if (id === currentSessionId) return;
    currentSessionId = id;
    renderPersonaList(allGroupedData);
    // 先更新角色显示（设置 window.currentPersonaAvatar），再加载消息
    await updatePersonaDisplay();
    await loadMessages(id);
    // 移动端切换会话后关闭侧边栏
    closeMobileSidebar();
}

async function createSessionForPersona(personaId) {
    try {
        const r = await fetch('/nex/sessions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: '新会话', user: getUser() })
        });
        const d = await r.json();
        const newSessionId = d.data.session_id;

        if (personaId) {
            await fetch(`/nex/sessions/${newSessionId}/persona`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ persona_id: personaId })
            });
        }

        currentSessionId = newSessionId;
        expandedPersonas.add(personaId || 'default');
        await loadPersonaGroupedSessions();
        // 移动端创建会话后关闭侧边栏
        closeMobileSidebar();
    } catch (e) { showToast('创建失败: ' + e.message, 'error'); }
}

function filterPersonaList() {
    renderPersonaList(allGroupedData);
}

async function refreshPersonaList() {
    const btn = document.getElementById('refreshSessionsBtn');
    btn.classList.add('loading');
    await loadPersonaGroupedSessions();
    btn.classList.remove('loading');
}

async function updateSessionList() {
    await loadPersonaGroupedSessions();
}

// ========== 输入工具栏 ==========
function toggleToolbarDropdown(id) {
    const dropdown = document.getElementById(id);
    const wasOpen = dropdown.classList.contains('open');

    // 关闭所有下拉菜单
    document.querySelectorAll('.toolbar-dropdown').forEach(d => d.classList.remove('open'));

    // 如果之前是关闭的，则打开
    if (!wasOpen) {
        dropdown.classList.add('open');
        
        // 移动端调整菜单位置
        if (window.innerWidth <= 600) {
            const menu = dropdown.querySelector('.toolbar-dropdown-menu');
            if (menu) {
                const inputArea = document.querySelector('.input-area');
                if (inputArea) {
                    const inputRect = inputArea.getBoundingClientRect();
                    menu.style.bottom = (window.innerHeight - inputRect.top + 8) + 'px';
                }
            }
        }
        
        // 加载对应的内容
        if (id === 'toolbarModelDropdown') loadToolbarModels();
        else if (id === 'toolbarToolsDropdown') loadToolbarTools();
        else if (id === 'toolbarPersonaDropdown') loadToolbarPersonas();
    }
}

async function loadToolbarModels() {
    const menu = document.getElementById('toolbarModelMenu');
    try {
        const r = await fetch('/nex/models');
        const d = await r.json();
        const chatModels = d.data.models.filter(m => m.model_type !== 'embedding');

        if (chatModels.length === 0) {
            menu.innerHTML = '<div class="toolbar-empty">暂无可用模型</div>';
            return;
        }

        let html = '<div class="toolbar-dropdown-header">选择模型</div>';
        html += chatModels.map(m => `
                    <div class="toolbar-dropdown-item ${m.key === currentModelKey ? 'active' : ''}" onclick="selectToolbarModel('${m.key}')">
                        <div class="toolbar-dropdown-item-icon">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                                <path d="M2 17l10 5 10-5"/>
                                <path d="M2 12l10 5 10-5"/>
                            </svg>
                        </div>
                        <div class="toolbar-dropdown-item-info">
                            <div class="toolbar-dropdown-item-name">${escapeHtml(m.name)}</div>
                            <div class="toolbar-dropdown-item-desc">${escapeHtml(m.model)} · ${escapeHtml(m.provider_name)}</div>
                        </div>
                    </div>
                `).join('');
        menu.innerHTML = html;
    } catch (e) { menu.innerHTML = '<div class="toolbar-empty">加载失败</div>'; }
}

async function selectToolbarModel(key) {
    document.getElementById('toolbarModelDropdown').classList.remove('open');
    if (key === currentModelKey) return;
    currentModelKey = key;
    localStorage.setItem('currentModelKey', key);
    // 重新加载模型列表以更新显示
    await loadModels();
}

function updateToolbarModelName() {
    const el = document.getElementById('toolbarModelName');
    const current = document.getElementById('currentModelName')?.textContent;
    if (current && el) {
        // 截取显示名称，最多显示10个字符
        el.textContent = current.length > 10 ? current.substring(0, 10) + '...' : current;
    }
}

async function loadToolbarTools() {
    const menu = document.getElementById('toolbarToolsMenu');
    try {
        const r = await fetch('/nex/tools');
        const d = await r.json();
        const tools = d.data || [];
        toolsEnabled = d.enabled !== false;
        
        // 只统计启用的工具
        const enabledTools = tools.filter(t => t.enabled);
        const enabledCount = enabledTools.length;

        const badge = document.getElementById('toolbarToolsCount');
        if (toolsEnabled && enabledCount > 0) {
            badge.textContent = enabledCount;
            badge.style.display = '';
        } else {
            badge.textContent = '';
            badge.style.display = 'none';
        }

        // 工具总开关
        let html = `
            <div class="toolbar-dropdown-item" style="justify-content:space-between;cursor:default;">
                <div style="display:flex;align-items:center;gap:8px;">
                    <div class="toolbar-dropdown-item-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
                    </div>
                    <span>启用工具调用</span>
                </div>
                <label class="toggle-switch" style="margin:0;">
                    <input type="checkbox" ${toolsEnabled ? 'checked' : ''} onchange="toggleToolsEnabled(this.checked)">
                    <span class="toggle-slider"></span>
                </label>
            </div>
        `;

        // 可用工具标题 + 刷新按钮
        html += `
            <div class="toolbar-dropdown-header" style="display:flex;justify-content:space-between;align-items:center;">
                <span>可用工具 <span style="color:var(--accent)">${enabledCount}</span></span>
                <button class="btn-icon" onclick="reloadTools(event)" title="重新加载工具" style="width:24px;height:24px;padding:0;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;">
                        <path d="M23 4v6h-6"/><path d="M1 20v-6h6"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
                    </svg>
                </button>
            </div>
        `;

        if (enabledCount === 0) {
            html += '<div class="toolbar-empty">暂无可用工具</div>';
            menu.innerHTML = html;
            return;
        }

        // 按类型分组（只显示启用的）
        const builtinTools = enabledTools.filter(t => t.type === 'builtin');
        const mcpTools = enabledTools.filter(t => t.type === 'mcp');
        const customTools = enabledTools.filter(t => t.type === 'custom');

        if (builtinTools.length > 0) {
            html += builtinTools.map(t => renderToolbarToolItem(t, '内置')).join('');
        }
        if (mcpTools.length > 0) {
            html += mcpTools.map(t => renderToolbarToolItem(t, 'MCP')).join('');
        }
        if (customTools.length > 0) {
            html += customTools.map(t => renderToolbarToolItem(t, '自定义')).join('');
        }

        menu.innerHTML = html;
    } catch (e) { menu.innerHTML = '<div class="toolbar-empty">加载失败</div>'; }
}

async function reloadTools(e) {
    e.stopPropagation();
    try {
        const r = await fetch('/nex/tools/reload', { method: 'POST' });
        const d = await r.json();
        if (d.data.errors && d.data.errors.length > 0) {
            showToast(`加载完成，${d.data.errors.length} 个工具出错`, 'warning');
        } else {
            showToast(`已加载 ${d.data.loaded.length} 个自定义工具`, 'success');
        }
        await loadToolbarTools();
        await loadToolbarToolsCount();
    } catch (e) {
        showToast('刷新失败', 'error');
    }
}

async function toggleToolsEnabled(enabled) {
    try {
        await fetch(`/nex/tools/toggle?enabled=${enabled}`, { method: 'PUT' });
        toolsEnabled = enabled;
        // 更新角标显示
        await loadToolbarToolsCount();
    } catch (e) {
        showToast('切换失败', 'error');
    }
}

function renderToolbarToolItem(tool, typeLabel) {
    const iconSvg = tool.type === 'mcp'
        ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>'
        : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>';

    return `
                <div class="toolbar-dropdown-item" title="${escapeHtml(tool.description || '')}">
                    <div class="toolbar-dropdown-item-icon">${iconSvg}</div>
                    <div class="toolbar-dropdown-item-info">
                        <div class="toolbar-dropdown-item-name">${escapeHtml(tool.name)}</div>
                        <div class="toolbar-dropdown-item-desc">${typeLabel} · ${escapeHtml((tool.description || '').substring(0, 30))}${(tool.description || '').length > 30 ? '...' : ''}</div>
                    </div>
                </div>
            `;
}

async function loadToolbarPersonas() {
    const menu = document.getElementById('toolbarPersonaMenu');
    try {
        const r = await fetch('/nex/personas');
        const d = await r.json();
        const personas = d.data || [];

        let html = '<div class="toolbar-dropdown-header">切换角色卡</div>';
        html += `
                    <div class="toolbar-dropdown-item ${!currentSessionPersonaId ? 'active' : ''}" onclick="selectToolbarPersona(null)">
                        <div class="toolbar-dropdown-item-icon">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                                <circle cx="12" cy="7" r="4"/>
                            </svg>
                        </div>
                        <div class="toolbar-dropdown-item-info">
                            <div class="toolbar-dropdown-item-name">默认助手</div>
                            <div class="toolbar-dropdown-item-desc">通用对话</div>
                        </div>
                    </div>
                `;

        html += personas.map(p => {
            const iconHtml = p.avatar 
                ? `<img src="${p.avatar}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">`
                : `<span style="color:white;font-size:0.75rem;font-weight:600;">${p.name.charAt(0).toUpperCase()}</span>`;
            return `
                    <div class="toolbar-dropdown-item ${currentSessionPersonaId === p.id ? 'active' : ''}" onclick="selectToolbarPersona(${p.id})">
                        <div class="toolbar-dropdown-item-icon" style="background:${p.avatar ? 'transparent' : getPersonaColor(p.id)}">
                            ${iconHtml}
                        </div>
                        <div class="toolbar-dropdown-item-info">
                            <div class="toolbar-dropdown-item-name">${escapeHtml(p.name)}</div>
                            <div class="toolbar-dropdown-item-desc">${escapeHtml((p.system_prompt || '').substring(0, 30))}${(p.system_prompt || '').length > 30 ? '...' : ''}</div>
                        </div>
                    </div>
                `;
        }).join('');

        menu.innerHTML = html;
    } catch (e) { menu.innerHTML = '<div class="toolbar-empty">加载失败</div>'; }
}

async function selectToolbarPersona(personaId) {
    document.getElementById('toolbarPersonaDropdown').classList.remove('open');
    if (!currentSessionId) {
        showToast('请先选择或创建会话', 'warning');
        return;
    }
    try {
        await fetch(`/nex/sessions/${currentSessionId}/persona`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ persona_id: personaId })
        });
        currentSessionPersonaId = personaId;
        // 先更新角色显示（设置 window.currentPersonaAvatar），再刷新消息
        await updatePersonaDisplay();
        await loadMessages(currentSessionId);
        // 刷新侧边栏
        await loadPersonaGroupedSessions();
    } catch (e) { showToast('切换失败: ' + e.message, 'error'); }
}

// 初始化时加载工具数量
async function loadToolbarToolsCount() {
    try {
        const r = await fetch('/nex/tools');
        const d = await r.json();
        toolsEnabled = d.enabled !== false;
        const tools = d.data || [];
        // 只统计启用的工具
        const enabledCount = tools.filter(t => t.enabled).length;
        const badge = document.getElementById('toolbarToolsCount');
        if (toolsEnabled && enabledCount > 0) {
            badge.textContent = enabledCount;
            badge.style.display = '';
        } else {
            badge.textContent = '';
            badge.style.display = 'none';
        }
    } catch (e) { }
}

// 更新用户名显示
function updateUserName(name) {
    const displayName = name.trim() || 'guest';
    document.getElementById('username').value = displayName;
    document.getElementById('toolbarUserName').textContent = displayName.length > 8 ? displayName.substring(0, 8) + '...' : displayName;
    localStorage.setItem('nex_user', displayName);
    document.getElementById('toolbarUserDropdown').classList.remove('open');
}

// 系统提示词开关状态
let systemPromptEnabled = false;
let systemPromptContent = '';

// 切换系统提示词
function toggleSystemPrompt() {
    systemPromptEnabled = !systemPromptEnabled;
    const btn = document.getElementById('systemPromptToggle');
    if (systemPromptEnabled) {
        btn.classList.add('active');
        showToast('系统提示词已启用', 'success');
    } else {
        btn.classList.remove('active');
        showToast('系统提示词已禁用', 'info');
    }
    localStorage.setItem('nex_system_prompt_enabled', systemPromptEnabled);
}

// 加载系统提示词
async function loadSystemPrompt() {
    try {
        const r = await fetch('/nex/prompts');
        const d = await r.json();
        systemPromptContent = d.data?.prompt || '';
        // 恢复开关状态
        systemPromptEnabled = localStorage.getItem('nex_system_prompt_enabled') === 'true';
        if (systemPromptEnabled) {
            document.getElementById('systemPromptToggle')?.classList.add('active');
        }
    } catch (e) { console.error('加载系统提示词失败', e); }
}

// 获取系统提示词（供发送消息时使用）
function getSystemPromptIfEnabled() {
    return systemPromptEnabled ? systemPromptContent : '';
}

// ========== 初始化 ==========
async function init() {
    await initTheme();
    const saved = localStorage.getItem('nex_user');
    if (saved) document.getElementById('username').value = saved;
    // 更新工具栏用户名显示
    const userName = document.getElementById('username').value || 'guest';
    document.getElementById('toolbarUserName').textContent = userName.length > 8 ? userName.substring(0, 8) + '...' : userName;
    document.getElementById('username').addEventListener('change', e => {
        localStorage.setItem('nex_user', e.target.value);
        updateUserName(e.target.value);
    });
    await loadModels();
    await loadSessions();
    await loadVersion();
    await loadToolbarToolsCount();
    await loadSystemPrompt();
    updateToolbarModelName();

    const inp = document.getElementById('inp');
    // 清空输入框，防止浏览器自动填充
    inp.value = '';
    // 延迟再次清空，防止某些浏览器扩展延迟填充
    setTimeout(() => { if (inp.value && !inp.dataset.userInput) inp.value = ''; }, 100);
    setTimeout(() => { if (inp.value && !inp.dataset.userInput) inp.value = ''; }, 500);
    
    inp.addEventListener('keydown', e => {
        // 移动端回车换行，桌面端 Shift+Enter 换行
        const isMobile = window.innerWidth <= 600;
        if (e.key === 'Enter') {
            if (isMobile) {
                // 移动端：回车换行，不发送
                // 默认行为就是换行，不需要处理
            } else if (!e.shiftKey) {
                // 桌面端：回车发送，Shift+Enter 换行
                e.preventDefault();
                send();
            }
        }
    });
    // 标记用户输入
    inp.addEventListener('input', e => {
        inp.dataset.userInput = 'true';
        autoResizeTextarea(e);
    });
    // 输入框自动高度
    inp.addEventListener('input', autoResizeTextarea);

    // 点击其他地方关闭下拉菜单
    document.addEventListener('click', e => {
        const dropdown = document.getElementById('modelDropdown');
        if (!dropdown.contains(e.target)) dropdown.classList.remove('open');

        // 关闭工具栏下拉菜单
        document.querySelectorAll('.toolbar-dropdown').forEach(d => {
            if (!d.contains(e.target)) d.classList.remove('open');
        });

        // 关闭自定义选择器
        document.querySelectorAll('.custom-select').forEach(s => {
            if (!s.contains(e.target)) s.classList.remove('open');
        });

        // 关闭嵌入模型下拉菜单
        const embedDropdown = document.getElementById('embedModelDropdown');
        const embedMenu = document.getElementById('embedModelMenu');
        if (embedDropdown && embedMenu) {
            // 检查点击是否在下拉按钮或菜单内
            if (!embedDropdown.contains(e.target) && !embedMenu.contains(e.target)) {
                embedDropdown.classList.remove('open');
                // 恢复菜单的相对定位
                embedMenu.style.position = '';
                embedMenu.style.top = '';
                embedMenu.style.left = '';
                embedMenu.style.bottom = '';
            }
        }
    });
}

// ========== 角色卡下拉框 ==========
let currentSessionPersonaId = null;

function togglePersonaDropdown() {
    document.getElementById('personaDropdown').classList.toggle('open');
    loadPersonaMenu();
}

async function loadPersonaMenu() {
    try {
        const r = await fetch('/nex/personas');
        const d = await r.json();
        const menu = document.getElementById('personaMenu');
        let html = `<div class="dropdown-item ${!currentSessionPersonaId ? 'active' : ''}" onclick="selectSessionPersona(null)">
                    <div class="dropdown-item-name">默认</div>
                </div>`;
        html += d.data.map(p => `
                    <div class="dropdown-item ${currentSessionPersonaId === p.id ? 'active' : ''}" onclick="selectSessionPersona(${p.id})">
                        <div class="dropdown-item-name">${escapeHtml(p.name)}</div>
                    </div>
                `).join('');
        menu.innerHTML = html;
    } catch (e) { console.error('加载角色卡失败', e); }
}

async function selectSessionPersona(personaId) {
    document.getElementById('personaDropdown').classList.remove('open');
    if (!currentSessionId) {
        showToast('请先选择或创建会话', 'warning');
        return;
    }
    try {
        await fetch(`/nex/sessions/${currentSessionId}/persona`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ persona_id: personaId })
        });
        currentSessionPersonaId = personaId;
        // 先更新角色显示（设置 window.currentPersonaAvatar），再刷新消息
        await updatePersonaDisplay();
        await loadMessages(currentSessionId);
        // 刷新侧边栏
        await loadPersonaGroupedSessions();
    } catch (e) { showToast('切换失败: ' + e.message, 'error'); }
}

async function updatePersonaDisplay() {
    if (!currentSessionId) {
        document.getElementById('currentPersonaName').textContent = '默认';
        currentSessionPersonaId = null;
        window.currentPersonaAvatar = '';
        return;
    }
    try {
        const r = await fetch(`/nex/sessions/${currentSessionId}/persona`);
        const d = await r.json();
        if (d.data) {
            currentSessionPersonaId = d.data.id;
            document.getElementById('currentPersonaName').textContent = d.data.name;
            window.currentPersonaAvatar = d.data.avatar || '';
        } else {
            currentSessionPersonaId = null;
            document.getElementById('currentPersonaName').textContent = '默认';
            window.currentPersonaAvatar = '';
        }
    } catch (e) {
        currentSessionPersonaId = null;
        document.getElementById('currentPersonaName').textContent = '默认';
        window.currentPersonaAvatar = '';
    }
}

// ========== 输入框自动高度 ==========
function autoResizeTextarea() {
    const inp = document.getElementById('inp');
    inp.style.height = 'auto';
    inp.style.height = Math.min(inp.scrollHeight, 200) + 'px';
}

function resetTextareaHeight() {
    const inp = document.getElementById('inp');
    inp.style.height = 'auto';
}

// ========== 版本号 ==========
async function loadVersion() {
    try {
        const r = await fetch('/nex/version');
        const d = await r.json();
        if (d.code === 0 && d.data.version) {
            document.getElementById('appVersion').textContent = d.data.version;
        }
    } catch (e) { console.error('获取版本号失败', e); }
}

// ========== 模型下拉框 ==========
function toggleModelDropdown() {
    document.getElementById('modelDropdown').classList.toggle('open');
}

async function selectModel(key) {
    document.getElementById('modelDropdown').classList.remove('open');
    if (key === currentModelKey) return;
    currentModelKey = key;
    localStorage.setItem('currentModelKey', key);
    // 重新加载模型列表以更新显示
    await loadModels();
}

// ========== 模型管理 ==========
async function loadModels() {
    try {
        const r = await fetch('/nex/models');
        const d = await r.json();
        // 只显示对话模型（嵌入模型不能用于对话）
        const chatModels = d.data.models.filter(m => m.model_type !== 'embedding');
        
        if (chatModels.length === 0) {
            document.getElementById('currentModelName').textContent = '未配置模型';
            document.getElementById('modelMenu').innerHTML = '<div style="padding:12px;color:var(--text2)">请先添加对话模型</div>';
            currentModelKey = null;
            localStorage.removeItem('currentModelKey');
        } else {
            // 从 localStorage 读取上次选择的模型
            const savedKey = localStorage.getItem('currentModelKey');
            const savedModel = savedKey ? chatModels.find(m => m.key === savedKey) : null;
            
            if (savedModel) {
                currentModelKey = savedModel.key;
            } else {
                // 没有保存的或已删除，选第一个
                currentModelKey = chatModels[0].key;
                localStorage.setItem('currentModelKey', currentModelKey);
            }
            
            const currentModel = chatModels.find(m => m.key === currentModelKey);
            document.getElementById('currentModelName').textContent = currentModel.name;
            document.getElementById('modelMenu').innerHTML = chatModels.map(m => `
                    <div class="dropdown-item ${m.key === currentModelKey ? 'active' : ''}" onclick="selectModel('${m.key}')">
                        <div class="dropdown-item-name">${escapeHtml(m.name)} ${renderModelTags(m.tags)}</div>
                        <div class="dropdown-item-model">${escapeHtml(m.model)} · ${escapeHtml(m.provider_name)}</div>
                    </div>
                `).join('');
        }
        updateToolbarModelName();
    } catch { }
}

// ========== 服务商管理 ==========
let currentProviderIdEdit = null;
let currentMCPIdEdit = null;
let selectedProviderId = null;

async function loadProviderListPanel() {
    try {
        const r = await fetch('/nex/providers');
        const d = await r.json();
        const panel = document.getElementById('providerListPanel');
        if (d.data.length === 0) {
            panel.innerHTML = '<div style="padding:20px;color:var(--text2);text-align:center">暂无服务商<br><span style="font-size:0.85rem">点击上方按钮添加</span></div>';
            return;
        }
        panel.innerHTML = d.data.map(p => `
                    <div class="provider-item ${selectedProviderId === p.id ? 'active' : ''}" onclick="selectProvider('${p.id}')">
                        <div class="provider-item-name">${escapeHtml(p.name)}</div>
                        <div class="provider-item-detail">${escapeHtml(p.base_url)}</div>
                    </div>
                `).join('');
    } catch (e) { showToast('加载失败: ' + e.message, 'error'); }
}

function showAddProvider() {
    currentProviderIdEdit = null;
    selectedProviderId = null;
    document.getElementById('providerDetailTitle').textContent = '添加服务商';
    document.getElementById('providerIdInput').value = '';
    document.getElementById('providerIdInput').disabled = false;
    document.getElementById('providerNameInput').value = '';
    document.getElementById('providerApiKeyInput').value = '';
    document.getElementById('providerApiKeyInput').placeholder = 'sk-...';
    document.getElementById('providerBaseUrlInput').value = '';
    document.getElementById('providerViewMode').style.display = 'none';
    document.getElementById('providerEditMode').style.display = 'block';
    document.getElementById('providerDeleteRow').style.display = 'none';
    document.getElementById('detail-provider').classList.add('active');
}

async function selectProvider(id) {
    selectedProviderId = id;
    try {
        const r = await fetch(`/nex/providers/${id}`);
        const d = await r.json();

        // 更新列表高亮
        await loadProviderListPanel();

        // 显示查看模式
        document.getElementById('providerDetailTitle').textContent = d.data.name;
        document.getElementById('providerViewName').textContent = d.data.name;
        document.getElementById('providerViewUrl').textContent = d.data.base_url;
        document.getElementById('providerViewKey').textContent = 'API Key: ' + d.data.api_key_masked;
        document.getElementById('providerViewMode').style.display = 'block';
        document.getElementById('providerEditMode').style.display = 'none';
        document.getElementById('detail-provider').classList.add('active');

        await loadProviderModels(id);
    } catch (e) { showToast('加载失败: ' + e.message, 'error'); }
}

function switchToProviderEditMode() {
    if (!selectedProviderId) return;
    currentProviderIdEdit = selectedProviderId;
    fetch(`/nex/providers/${selectedProviderId}`).then(r => r.json()).then(d => {
        document.getElementById('providerDetailTitle').textContent = '编辑服务商';
        document.getElementById('providerIdInput').value = selectedProviderId;
        document.getElementById('providerIdInput').disabled = true;
        document.getElementById('providerNameInput').value = d.data.name;
        document.getElementById('providerApiKeyInput').value = '';
        document.getElementById('providerApiKeyInput').placeholder = d.data.api_key_masked + ' (留空不修改)';
        document.getElementById('providerBaseUrlInput').value = d.data.base_url;
        document.getElementById('providerViewMode').style.display = 'none';
        document.getElementById('providerEditMode').style.display = 'block';
        document.getElementById('providerDeleteRow').style.display = 'flex';
    });
}

function cancelProviderEdit() {
    if (selectedProviderId) {
        selectProvider(selectedProviderId);
    } else {
        closeProviderDetail();
    }
}

async function loadProviderModels(providerId) {
    try {
        const r = await fetch('/nex/models');
        const d = await r.json();
        const models = d.data.models.filter(m => m.provider_id === providerId);
        const list = document.getElementById('providerModelsList');
        if (models.length === 0) {
            list.innerHTML = '<div style="color:var(--text2);font-size:0.85rem;text-align:center;padding:12px;">暂无模型</div>';
            return;
        }

        // 分离对话模型和嵌入模型
        const chatModels = models.filter(m => m.model_type !== 'embedding');
        const embeddingModels = models.filter(m => m.model_type === 'embedding');

        let html = '';

        // 对话模型
        if (chatModels.length > 0) {
            html += '<div class="model-section-title">对话模型</div>';
            html += chatModels.map(m => `
                        <div class="model-item" onclick="selectModelForEdit('${m.key}')">
                            <div class="model-item-name">${escapeHtml(m.name)} ${renderModelTags(m.tags)}</div>
                            <div class="model-item-detail">${escapeHtml(m.model)}</div>
                        </div>
                    `).join('');
        }

        // 嵌入模型
        if (embeddingModels.length > 0) {
            if (chatModels.length > 0) {
                html += '<div class="model-section-divider"></div>';
            }
            html += '<div class="model-section-title">嵌入模型</div>';
            html += embeddingModels.map(m => `
                        <div class="model-item embedding" onclick="selectModelForEdit('${m.key}')">
                            <div class="model-item-name">${escapeHtml(m.name)}</div>
                            <div class="model-item-detail">${escapeHtml(m.model)}</div>
                        </div>
                    `).join('');
        }

        list.innerHTML = html;
    } catch (e) { showToast('加载失败: ' + e.message, 'error'); }
}

async function saveProviderInline() {
    const id = document.getElementById('providerIdInput').value.trim();
    const name = document.getElementById('providerNameInput').value.trim();
    const apiKey = document.getElementById('providerApiKeyInput').value.trim();
    const baseUrl = document.getElementById('providerBaseUrlInput').value.trim();

    if (!id || !name || !baseUrl) { showAlert('请填写完整信息', '提示', 'warning'); return; }
    if (!currentProviderIdEdit && !apiKey) { showAlert('请填写 API Key', '提示', 'warning'); return; }

    try {
        if (currentProviderIdEdit) {
            const body = { name, base_url: baseUrl };
            if (apiKey) body.api_key = apiKey;
            await fetch(`/nex/providers/${currentProviderIdEdit}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
        } else {
            await fetch('/nex/providers', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id, name, api_key: apiKey, base_url: baseUrl }) });
            selectedProviderId = id;
        }
        showToast('保存成功', 'success');
        closeProviderDetail();
        if (selectedProviderId) {
            await selectProvider(selectedProviderId);
        } else {
            await loadProviderListPanel();
        }
    } catch (e) { showToast('保存失败: ' + e.message, 'error'); }
}

async function deleteCurrentProvider() {
    if (!currentProviderIdEdit) {
        showToast('无法删除：未选择服务商', 'error');
        return;
    }
    
    showConfirm('删除服务商', `确定要删除服务商 "${currentProviderIdEdit}" 吗？该服务商下的所有模型也将被删除。`, async () => {
        try {
            const r = await fetch(`/nex/providers/${currentProviderIdEdit}`, { method: 'DELETE' });
            const d = await r.json();
            if (d.code === 0) {
                showToast('删除成功', 'success');
                closeProviderDetail();
                await loadProviderListPanel();
                await loadModels();
            } else {
                showToast('删除失败: ' + (d.message || '未知错误'), 'error');
            }
        } catch (e) {
            showToast('删除失败: ' + e.message, 'error');
        }
    });
}

function closeProviderDetail() {
    closeSettingsDetail('detail-provider', () => {
        currentProviderIdEdit = null;
        selectedProviderId = null;
        loadProviderListPanel();
    });
}

// 通用关闭详情面板函数（带动画）
function closeSettingsDetail(detailId, callback) {
    const detail = document.getElementById(detailId);
    if (!detail || !detail.classList.contains('active')) {
        if (callback) callback();
        return;
    }
    
    detail.classList.add('closing');
    setTimeout(() => {
        detail.classList.remove('active', 'closing');
        if (callback) callback();
    }, 200);
}

// ========== 供应商模型列表弹窗 ==========
let allProviderModels = [];  // 存储所有模型数据
let currentModelFilter = 'all';  // 当前筛选类型

async function showProviderModelsModal() {
    if (!selectedProviderId) return;

    const modal = document.getElementById('providerModelsModal');
    const content = document.getElementById('providerModelsListContent');
    const countEl = document.getElementById('providerModelsCount');

    // 获取供应商名称
    try {
        const providerR = await fetch(`/nex/providers/${selectedProviderId}`);
        const providerD = await providerR.json();
        document.getElementById('providerModelsModalTitle').textContent = `${providerD.data.name} 模型列表`;
    } catch {
        document.getElementById('providerModelsModalTitle').textContent = '模型列表';
    }

    // 重置搜索和筛选
    document.getElementById('providerModelsSearch').value = '';
    setModelFilter('all');

    modal.classList.add('show');
    content.innerHTML = '<div style="padding:60px;text-align:center;color:var(--text2);"><span class="typing"><span></span><span></span><span></span></span> 正在加载模型列表...</div>';
    countEl.textContent = '';

    await loadProviderModelsData();
}

async function loadProviderModelsData() {
    const content = document.getElementById('providerModelsListContent');
    const countEl = document.getElementById('providerModelsCount');

    try {
        const r = await fetch(`/nex/providers/${selectedProviderId}/models`);
        const d = await r.json();

        if (d.code !== 0) {
            content.innerHTML = `<div style="padding:60px;text-align:center;color:var(--error);">获取失败: ${escapeHtml(d.detail || '未知错误')}</div>`;
            return;
        }

        allProviderModels = d.data || [];
        renderProviderModelsModal();
    } catch (e) {
        content.innerHTML = `<div style="padding:60px;text-align:center;color:var(--error);">获取失败: ${escapeHtml(e.message)}</div>`;
    }
}

async function refreshProviderModels() {
    const btn = document.getElementById('refreshModelsBtn');
    btn.classList.add('loading');

    const content = document.getElementById('providerModelsListContent');
    content.innerHTML = '<div style="padding:60px;text-align:center;color:var(--text2);"><span class="typing"><span></span><span></span><span></span></span> 正在刷新...</div>';

    await loadProviderModelsData();
    btn.classList.remove('loading');
    showToast('刷新成功', 'success');
}

function setModelFilter(filter) {
    currentModelFilter = filter;
    // 更新标签页状态
    document.querySelectorAll('.modal-filter-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.filter === filter);
    });
    renderProviderModelsModal();
}

function filterProviderModels() {
    renderProviderModelsModal();
}

function renderProviderModelsModal() {
    const content = document.getElementById('providerModelsListContent');
    const countEl = document.getElementById('providerModelsCount');
    const searchText = document.getElementById('providerModelsSearch').value.toLowerCase().trim();

    // 筛选模型
    let filtered = allProviderModels.filter(m => {
        // 标签页筛选
        if (currentModelFilter === 'embedding') {
            if (m.model_type !== 'embedding') return false;
        } else if (currentModelFilter === 'reasoning') {
            if (m.model_type === 'embedding') return false;
            if (!m.capabilities || !m.capabilities.includes('reasoning')) return false;
        } else if (currentModelFilter === 'vision') {
            if (m.model_type === 'embedding') return false;
            if (!m.capabilities || !m.capabilities.includes('vision')) return false;
        } else if (currentModelFilter === 'tool') {
            if (m.model_type === 'embedding') return false;
            if (!m.capabilities || !m.capabilities.includes('tool')) return false;
        }
        // 搜索筛选
        if (searchText && !m.id.toLowerCase().includes(searchText)) return false;
        return true;
    });

    if (filtered.length === 0) {
        content.innerHTML = '<div style="padding:60px;text-align:center;color:var(--text2);">没有找到匹配的模型</div>';
        countEl.textContent = `共 ${allProviderModels.length} 个模型`;
        return;
    }

    // 分组显示（仅在"全部"标签页时分组）
    if (currentModelFilter === 'all') {
        const chatModels = filtered.filter(m => m.model_type !== 'embedding');
        const embeddingModels = filtered.filter(m => m.model_type === 'embedding');

        let html = '';

        if (chatModels.length > 0) {
            html += '<div class="model-section-title" style="padding:10px 14px;background:var(--card);">对话模型 (' + chatModels.length + ')</div>';
            html += chatModels.map(m => renderProviderModelItem(m)).join('');
        }

        if (embeddingModels.length > 0) {
            if (chatModels.length > 0) {
                html += '<div class="model-section-divider" style="margin:0;"></div>';
            }
            html += '<div class="model-section-title" style="padding:10px 14px;background:var(--card);">嵌入模型 (' + embeddingModels.length + ')</div>';
            html += embeddingModels.map(m => renderProviderModelItem(m)).join('');
        }

        content.innerHTML = html;
    } else {
        content.innerHTML = filtered.map(m => renderProviderModelItem(m)).join('');
    }

    countEl.textContent = `显示 ${filtered.length} / ${allProviderModels.length} 个模型`;
}

function renderProviderModelItem(m) {
    const isEmbedding = m.model_type === 'embedding';
    const capsHtml = !isEmbedding && m.capabilities && m.capabilities.length > 0
        ? renderModelTags(m.capabilities)
        : '';

    return `
                <div class="provider-model-item ${isEmbedding ? 'embedding' : ''}" onclick="addModelFromBrowser('${escapeHtml(m.id)}', '${m.model_type || 'chat'}', ${JSON.stringify(m.capabilities || []).replace(/"/g, '&quot;')})">
                    <div class="provider-model-item-info">
                        <div class="provider-model-item-name">
                            ${escapeHtml(m.id)} ${capsHtml}
                        </div>
                        ${m.owned_by ? `<div class="provider-model-item-meta">${escapeHtml(m.owned_by)}</div>` : ''}
                    </div>
                    <div class="provider-model-item-action">
                        <button class="btn-add-small" onclick="event.stopPropagation();addModelFromBrowser('${escapeHtml(m.id)}', '${m.model_type || 'chat'}', ${JSON.stringify(m.capabilities || []).replace(/"/g, '&quot;')})">添加</button>
                    </div>
                </div>
            `;
}

function addModelFromBrowser(modelId, modelType, capabilities) {
    closeProviderModelsModal();
    showAddModelForProvider();

    // 填充表单
    document.getElementById('modelIdInput').value = modelId;
    const displayName = modelId
        .replace(/-/g, ' ')
        .replace(/_/g, ' ')
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
    document.getElementById('modelDisplayNameInput').value = displayName;
    document.getElementById('modelTypeInput').value = modelType;
    onModelTypeChange();

    if (modelType !== 'embedding' && capabilities && capabilities.length > 0) {
        setModelTags(capabilities);
    } else {
        setModelTags([]);
    }
}

function closeProviderModelsModal() {
    document.getElementById('providerModelsModal').classList.remove('show');
    allProviderModels = [];
}

// ========== 模型管理（内联） ==========
let editingModelProviderIdInline = null;
let providerModelsCache = null;  // 缓存供应商模型列表

function showAddModelForProvider() {
    if (!selectedProviderId) return;
    editingModelProviderIdInline = selectedProviderId;
    editingModelKey = null;
    document.getElementById('modelDetailTitle').textContent = '添加模型';
    document.getElementById('modelTypeInput').value = 'chat';
    document.getElementById('modelIdInput').value = '';
    document.getElementById('modelIdInput').disabled = false;
    document.getElementById('modelDisplayNameInput').value = '';
    setModelTags([]);
    document.getElementById('modelTagsSection').style.display = 'block';
    document.getElementById('modelDeleteRow').style.display = 'none';

    document.getElementById('detail-model').classList.add('active');
}

function onModelTypeChange() {
    const modelType = document.getElementById('modelTypeInput').value;
    const tagsSection = document.getElementById('modelTagsSection');
    if (modelType === 'embedding') {
        tagsSection.style.display = 'none';
        // 清除所有标签
        setModelTags([]);
    } else {
        tagsSection.style.display = 'block';
    }
}

function setModelTags(tags) {
    const checkboxes = document.querySelectorAll('#modelTagsGroup .tag-checkbox');
    checkboxes.forEach(cb => {
        const input = cb.querySelector('input');
        const isChecked = tags && tags.includes(input.value);
        input.checked = isChecked;
        cb.classList.toggle('active', isChecked);
    });
}

function getModelTags() {
    const tags = [];
    document.querySelectorAll('#modelTagsGroup .tag-checkbox input:checked').forEach(input => {
        tags.push(input.value);
    });
    return tags;
}

// 标签复选框点击事件
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('#modelTagsGroup .tag-checkbox').forEach(cb => {
        cb.addEventListener('click', () => {
            const input = cb.querySelector('input');
            input.checked = !input.checked;
            cb.classList.toggle('active', input.checked);
        });
    });
});

async function selectModelForEdit(key) {
    try {
        const r = await fetch(`/nex/models/${key}`);
        const d = await r.json();
        editingModelKey = key;
        editingModelProviderIdInline = d.data.provider_id;
        document.getElementById('modelDetailTitle').textContent = '编辑模型';
        document.getElementById('modelTypeInput').value = d.data.model_type || 'chat';
        document.getElementById('modelIdInput').value = d.data.model_id;
        document.getElementById('modelIdInput').disabled = false;
        document.getElementById('modelDisplayNameInput').value = d.data.display_name;
        setModelTags(d.data.tags || []);
        // 根据模型类型显示/隐藏能力标签
        onModelTypeChange();
        document.getElementById('modelDeleteRow').style.display = 'flex';
        document.getElementById('detail-model').classList.add('active');
    } catch (e) { showToast('加载失败: ' + e.message, 'error'); }
}

async function saveModelInline() {
    const modelType = document.getElementById('modelTypeInput').value;
    const modelId = document.getElementById('modelIdInput').value.trim();
    const displayName = document.getElementById('modelDisplayNameInput').value.trim();
    // 嵌入模型不保存标签
    const tags = modelType === 'embedding' ? [] : getModelTags();

    if (!modelId || !displayName) { showAlert('请填写模型ID和显示名称', '提示', 'warning'); return; }

    try {
        if (editingModelKey) {
            const body = { model_id: modelId, display_name: displayName, tags: tags, model_type: modelType };
            const r = await fetch(`/nex/models/${editingModelKey}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
            if (!r.ok) { const d = await r.json(); throw new Error(d.detail); }
            const d = await r.json();
            // 更新 editingModelKey 为新的 key
            if (d.data && d.data.new_key) {
                editingModelKey = d.data.new_key;
            }
        } else {
            const r = await fetch('/nex/models', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ provider_id: editingModelProviderIdInline, model_id: modelId, display_name: displayName, tags: tags, model_type: modelType }) });
            if (!r.ok) { const d = await r.json(); throw new Error(d.detail); }
        }
        showToast('保存成功', 'success');
        closeModelDetail();
        if (selectedProviderId) {
            await selectProvider(selectedProviderId);
        }
        await loadModels();
    } catch (e) { showToast('保存失败: ' + e.message, 'error'); }
}

function deleteModelInline() {
    if (!editingModelKey) return;
    showConfirm('删除模型', '确定要删除此模型吗？', async () => {
        try {
            const r = await fetch(`/nex/models/${editingModelKey}`, { method: 'DELETE' });
            if (!r.ok) { const d = await r.json(); throw new Error(d.detail); }
            closeModelDetail();
            if (selectedProviderId) {
                await selectProvider(selectedProviderId);
            }
            await loadModels();
        } catch (e) { showToast('删除失败: ' + e.message, 'error'); }
    });
}

function closeModelDetail() {
    closeSettingsDetail('detail-model', () => {
        editingModelKey = null;
        editingModelProviderIdInline = null;
    });
}

// ========== 设置面板 ==========
function openSettings() {
    document.getElementById('settingsModal').classList.add('show');
    switchSettingsNav('about');
}

function closeSettings() {
    document.getElementById('settingsModal').classList.remove('show');
    closeProviderDetail();
    closeMCPDetail();
    closeModelDetail();
    closePersonaDetail();
}

function switchSettingsNav(name) {
    document.querySelectorAll('.settings-nav-item').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.settings-panel').forEach(t => t.classList.remove('active'));
    document.querySelector(`.settings-nav-item[onclick="switchSettingsNav('${name}')"]`).classList.add('active');
    document.getElementById('panel-' + name).classList.add('active');
    document.querySelectorAll('.settings-detail').forEach(d => d.classList.remove('active'));
    if (name === 'providers') loadProviderListPanel();
    if (name === 'tools') loadToolsListPanel();
    if (name === 'mcp') loadMCPListPanel();
    if (name === 'personas') loadPersonaListPanel();
    if (name === 'style') updateStylePanelUI();
    if (name === 'memory') loadMemoryPanel();
    if (name === 'openapi') loadOpenAPIConfigsPanel();
    if (name === 'about') loadAboutPanel();
}

// 加载关于面板
async function loadAboutPanel() {
    try {
        const r = await fetch('/nex/version');
        const d = await r.json();
        document.getElementById('appVersion').textContent = d.data?.version || '-';
    } catch (e) { }
}

// ========== 记忆管理 ==========
let editingMemoryId = null;
let currentEmbedModelId = null;

async function loadMemoryPanel() {
    // 加载记忆开关状态
    try {
        const r = await fetch('/nex/settings/memory_enabled');
        const d = await r.json();
        document.getElementById('memoryEnabledToggle').checked = d.data.value === 'true';
    } catch (e) { }

    // 加载嵌入模型列表
    await loadEmbedModelDropdown();

    // 加载记忆列表
    await loadMemoryList();
}

async function loadEmbedModelDropdown() {
    try {
        const r = await fetch('/nex/embedding/status');
        const d = await r.json();
        const models = d.data.models || [];
        currentEmbedModelId = d.data.model_id;

        const nameEl = document.getElementById('embedModelName');
        const menuEl = document.getElementById('embedModelMenu');

        if (models.length === 0) {
            nameEl.textContent = '未配置';
            menuEl.innerHTML = '<div class="toolbar-empty">请先在服务商中添加嵌入模型</div>';
        } else {
            const currentModel = models.find(m => m.id === currentEmbedModelId);
            nameEl.textContent = currentModel ? currentModel.name : models[0].name;

            let html = '<div class="toolbar-dropdown-header">选择嵌入模型</div>';
            html += models.map(m => `
                        <div class="toolbar-dropdown-item ${m.id === currentEmbedModelId ? 'active' : ''}" onclick="selectEmbedModel('${escapeHtml(m.id)}', '${escapeHtml(m.name)}')">
                            <div class="toolbar-dropdown-item-icon">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="8"/>
                                </svg>
                            </div>
                            <div class="toolbar-dropdown-item-info">
                                <div class="toolbar-dropdown-item-name">${escapeHtml(m.name)}</div>
                            </div>
                        </div>
                    `).join('');
            menuEl.innerHTML = html;
        }
    } catch (e) {
        document.getElementById('embedModelName').textContent = '加载失败';
    }
}

function toggleEmbedModelDropdown(event) {
    if (event) event.stopPropagation();
    const dropdown = document.getElementById('embedModelDropdown');
    const menu = document.getElementById('embedModelMenu');
    const btn = dropdown.querySelector('.toolbar-btn');
    
    const isOpen = dropdown.classList.contains('open');
    
    // 先关闭其他下拉菜单
    document.querySelectorAll('.toolbar-dropdown.open').forEach(d => {
        if (d !== dropdown) d.classList.remove('open');
    });
    
    if (isOpen) {
        dropdown.classList.remove('open');
        // 把菜单移回原位
        dropdown.appendChild(menu);
    } else {
        // 把菜单移到body下，避免被overflow:hidden裁剪
        document.body.appendChild(menu);
        
        // 计算按钮位置，使用fixed定位
        const rect = btn.getBoundingClientRect();
        menu.style.position = 'fixed';
        menu.style.top = (rect.bottom + 6) + 'px';
        menu.style.left = rect.left + 'px';
        menu.style.bottom = 'auto';
        menu.style.zIndex = '1300';
        menu.style.display = 'block';
        menu.style.opacity = '1';
        menu.style.transform = 'translateY(0)';
        dropdown.classList.add('open');
    }
}

async function selectEmbedModel(modelId, modelName) {
    document.getElementById('embedModelName').textContent = modelName;
    const embedDropdown = document.getElementById('embedModelDropdown');
    const embedMenu = document.getElementById('embedModelMenu');
    embedDropdown.classList.remove('open');
    // 恢复菜单的相对定位
    embedMenu.style.position = '';
    embedMenu.style.top = '';
    embedMenu.style.left = '';
    embedMenu.style.bottom = '';
    currentEmbedModelId = modelId;
    await setEmbeddingModel(modelId);
}

async function setEmbeddingModel(modelKey) {
    try {
        await fetch(`/nex/embedding/model?model_key=${encodeURIComponent(modelKey)}`, { method: 'PUT' });
    } catch (e) {
        showToast('设置失败', 'error');
    }
}

async function loadMemoryList() {
    const panel = document.getElementById('memoryListPanel');
    try {
        const user = getUser();
        const r = await fetch(`/nex/memories?user=${encodeURIComponent(user)}&limit=50`);
        const d = await r.json();
        if (d.data.length === 0) {
            panel.innerHTML = '<div style="padding:20px;color:var(--text2);text-align:center;font-size:0.9rem;">暂无记忆<br><span style="font-size:0.8rem;">AI 会自动记住重要信息，或手动添加</span></div>';
            return;
        }
        panel.innerHTML = d.data.map(m => `
                    <div class="provider-item" onclick="editMemory(${m.id})" style="margin-bottom:8px;">
                        <div class="provider-item-name" style="display:flex;justify-content:space-between;align-items:center;">
                            <span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${escapeHtml(m.content.substring(0, 40))}${m.content.length > 40 ? '...' : ''}</span>
                            <span style="font-size:0.7rem;color:var(--accent);margin-left:8px;">重要度: ${m.importance}</span>
                        </div>
                        <div class="provider-item-detail">${escapeHtml(m.created_at.substring(0, 10))}</div>
                    </div>
                `).join('');
    } catch (e) {
        panel.innerHTML = '<div style="padding:20px;color:var(--error);text-align:center;">加载失败</div>';
    }
}

async function toggleMemoryEnabled(enabled) {
    try {
        await fetch('/nex/settings', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ settings: { memory_enabled: enabled ? 'true' : 'false' } })
        });
    } catch (e) {
        showToast('设置失败', 'error');
    }
}

function showAddMemory() {
    editingMemoryId = null;
    showPrompt('添加记忆', '输入要记住的内容', '', async (content) => {
        if (!content) return;
        try {
            const r = await fetch(`/nex/memories?user=${encodeURIComponent(getUser())}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content, importance: 5 })
            });
            if (!r.ok) {
                const d = await r.json();
                throw new Error(d.detail);
            }
            await loadMemoryList();
        } catch (e) {
            showToast('添加失败: ' + e.message, 'error');
        }
    });
}

function editMemory(id) {
    editingMemoryId = id;
    fetch(`/nex/memories/${id}`).then(r => r.json()).then(d => {
        const m = d.data;
        document.getElementById('memoryDetailContent').textContent = m.content;
        document.getElementById('memoryDetailMeta').textContent = `重要度: ${m.importance} | 创建时间: ${m.created_at.substring(0, 19).replace('T', ' ')}`;
        document.getElementById('memoryDetailModal').classList.add('show');
    }).catch(e => showToast('加载失败', 'error'));
}

function closeMemoryDetail() {
    document.getElementById('memoryDetailModal').classList.remove('show');
}

async function deleteCurrentMemory() {
    if (!editingMemoryId) return;
    try {
        await fetch(`/nex/memories/${editingMemoryId}`, { method: 'DELETE' });
        closeMemoryDetail();
        await loadMemoryList();
    } catch (e) {
        showToast('删除失败', 'error');
    }
}

// 简单的输入对话框
function showPrompt(title, message, defaultValue, callback) {
    const html = `
                <div style="margin-bottom:16px;">${escapeHtml(message)}</div>
                <textarea id="promptInput" style="width:100%;height:80px;padding:10px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius-sm);color:var(--text);font-size:0.9rem;resize:none;">${escapeHtml(defaultValue)}</textarea>
            `;
    document.getElementById('alertTitle').textContent = title;
    document.getElementById('alertBody').innerHTML = html;
    document.getElementById('alertModal').querySelector('.alert-actions').innerHTML = `
                <button class="alert-btn-ok" style="background:var(--card);color:var(--text);" onclick="closeAlert()">取消</button>
                <button class="alert-btn-ok" onclick="const v=document.getElementById('promptInput').value;closeAlert();(${callback.toString()})(v)">确定</button>
            `;
    document.getElementById('alertModal').classList.add('show');
    setTimeout(() => document.getElementById('promptInput')?.focus(), 100);
}

// ========== 角色卡管理 ==========
let editingPersonaId = null;

async function loadPersonaListPanel() {
    try {
        const r = await fetch('/nex/personas');
        const d = await r.json();
        const panel = document.getElementById('personaListPanel');
        if (d.data.length === 0) {
            panel.innerHTML = '<div style="padding:20px;color:var(--text2);text-align:center">暂无角色卡<br><span style="font-size:0.85rem">点击上方按钮添加</span></div>';
            return;
        }
        panel.innerHTML = d.data.map(p => `
                    <div class="provider-item ${editingPersonaId === p.id ? 'active' : ''}" onclick="selectPersona(${p.id})">
                        <div class="provider-item-name">${escapeHtml(p.name)}</div>
                        <div class="provider-item-detail" style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:200px;">${escapeHtml(p.system_prompt.substring(0, 50))}${p.system_prompt.length > 50 ? '...' : ''}</div>
                    </div>
                `).join('');
    } catch (e) { showToast('加载失败: ' + e.message, 'error'); }
}

function showAddPersona() {
    editingPersonaId = null;
    document.getElementById('personaDetailTitle').textContent = '添加角色卡';
    document.getElementById('personaNameInput').value = '';
    document.getElementById('personaPromptInput').value = '';
    document.getElementById('personaMaxTokensInput').value = '';
    document.getElementById('personaTemperatureInput').value = '';
    document.getElementById('personaTopPInput').value = '';
    document.getElementById('personaAvatarData').value = '';
    document.getElementById('deletePersonaBtn').style.display = 'none';
    updatePersonaAvatarPreview('', 'P');
    document.getElementById('detail-persona').classList.add('active');
}

async function selectPersona(id) {
    editingPersonaId = id;
    try {
        const r = await fetch(`/nex/personas/${id}`);
        const d = await r.json();
        document.getElementById('personaDetailTitle').textContent = '编辑角色卡';
        document.getElementById('personaNameInput').value = d.data.name;
        document.getElementById('personaPromptInput').value = d.data.system_prompt;
        document.getElementById('personaMaxTokensInput').value = d.data.max_tokens || '';
        document.getElementById('personaTemperatureInput').value = d.data.temperature !== null ? d.data.temperature : '';
        document.getElementById('personaTopPInput').value = d.data.top_p !== null ? d.data.top_p : '';
        document.getElementById('personaAvatarData').value = d.data.avatar || '';
        document.getElementById('deletePersonaBtn').style.display = 'block';
        updatePersonaAvatarPreview(d.data.avatar, d.data.name.charAt(0).toUpperCase(), getPersonaColor(id));
        document.getElementById('detail-persona').classList.add('active');
        await loadPersonaListPanel();
    } catch (e) { showToast('加载失败: ' + e.message, 'error'); }
}

function updatePersonaAvatarPreview(avatar, letter, bgColor) {
    const preview = document.getElementById('personaAvatarPreview');
    const letterEl = document.getElementById('personaAvatarLetter');
    if (avatar) {
        preview.innerHTML = `<img src="${avatar}" style="width:100%;height:100%;object-fit:cover;">`;
    } else {
        preview.style.background = bgColor || 'var(--accent)';
        preview.innerHTML = `<span style="color:white;font-weight:600;font-size:1rem;">${letter || 'P'}</span>`;
    }
}

function previewPersonaAvatar(input) {
    const file = input.files[0];
    if (!file) return;
    
    if (file.size > 500 * 1024) {
        showToast('图片大小不能超过500KB', 'error');
        input.value = '';
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById('personaAvatarData').value = e.target.result;
        updatePersonaAvatarPreview(e.target.result);
    };
    reader.readAsDataURL(file);
}

function clearPersonaAvatar() {
    document.getElementById('personaAvatarData').value = '';
    document.getElementById('personaAvatarUpload').value = '';
    const name = document.getElementById('personaNameInput').value || 'P';
    const bgColor = editingPersonaId ? getPersonaColor(editingPersonaId) : 'var(--accent)';
    updatePersonaAvatarPreview('', name.charAt(0).toUpperCase(), bgColor);
}

async function savePersonaInline() {
    const name = document.getElementById('personaNameInput').value.trim();
    const systemPrompt = document.getElementById('personaPromptInput').value.trim();
    if (!name || !systemPrompt) { showAlert('请填写完整信息', '提示', 'warning'); return; }

    const maxTokensVal = document.getElementById('personaMaxTokensInput').value;
    const temperatureVal = document.getElementById('personaTemperatureInput').value;
    const topPVal = document.getElementById('personaTopPInput').value;
    const avatarVal = document.getElementById('personaAvatarData').value;

    const body = { name, system_prompt: systemPrompt, avatar: avatarVal || null };
    if (maxTokensVal) body.max_tokens = parseInt(maxTokensVal);
    if (temperatureVal) body.temperature = parseFloat(temperatureVal);
    if (topPVal) body.top_p = parseFloat(topPVal);

    try {
        if (editingPersonaId) {
            await fetch(`/nex/personas/${editingPersonaId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
        } else {
            await fetch('/nex/personas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
        }
        showToast('保存成功', 'success');
        closePersonaDetail();
        await loadPersonaListPanel();
        // 刷新侧边栏和消息列表以显示新头像
        await loadPersonaGroupedSessions();
        if (currentSessionId) {
            await updatePersonaDisplay();
            await loadMessages(currentSessionId);
        }
    } catch (e) { showToast('保存失败: ' + e.message, 'error'); }
}

function deletePersonaInline() {
    if (!editingPersonaId) return;
    showConfirm('删除角色卡', '确定要删除此角色卡吗？使用该角色卡的会话将恢复默认提示词。', async () => {
        try {
            await fetch(`/nex/personas/${editingPersonaId}`, { method: 'DELETE' });
            showToast('删除成功', 'success');
            closePersonaDetail();
            await loadPersonaListPanel();
        } catch (e) { showToast('删除失败: ' + e.message, 'error'); }
    });
}

function closePersonaDetail() {
    closeSettingsDetail('detail-persona', () => {
        editingPersonaId = null;
    });
}

// ========== 工具管理 ==========
async function loadToolsListPanel() {
    const panel = document.getElementById('toolsListPanel');
    try {
        const r = await fetch('/nex/tools');
        const d = await r.json();
        const tools = d.data || [];
        const globalEnabled = d.enabled !== false;
        
        if (tools.length === 0) {
            panel.innerHTML = '<div style="padding:20px;color:var(--text2);text-align:center">暂无工具</div>';
            return;
        }
        
        const builtinTools = tools.filter(t => t.type === 'builtin');
        const customTools = tools.filter(t => t.type === 'custom');
        const mcpTools = tools.filter(t => t.type === 'mcp');
        
        let html = `
            <div class="memory-toggle-box" style="margin-bottom:16px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <div style="font-weight:500;">启用工具调用</div>
                        <div style="font-size:0.8rem;color:var(--text2);margin-top:4px;">关闭后所有工具将不可用（包括MCP）</div>
                    </div>
                    <label class="toggle-switch">
                        <input type="checkbox" ${globalEnabled ? 'checked' : ''} onchange="toggleToolsEnabledFromSettings(this.checked)">
                        <span class="toggle-slider"></span>
                    </label>
                </div>
            </div>
        `;
        
        // 内置工具
        if (builtinTools.length > 0) {
            const allBuiltinEnabled = builtinTools.every(t => t.enabled);
            html += `
                <div class="settings-panel-header" style="padding:8px 0;border-bottom:1px solid var(--border);">
                    <span style="font-size:0.85rem;color:var(--text2);">内置工具 (${builtinTools.length})</span>
                    <button class="btn-add-small" onclick="toggleAllToolsType('builtin', ${!allBuiltinEnabled})">${allBuiltinEnabled ? '全部关闭' : '全部开启'}</button>
                </div>
            `;
            html += builtinTools.map(t => renderToolItem(t)).join('');
        }
        
        // 自定义工具
        if (customTools.length > 0) {
            const allCustomEnabled = customTools.every(t => t.enabled);
            html += `
                <div class="settings-panel-header" style="padding:8px 0;border-bottom:1px solid var(--border);margin-top:12px;">
                    <span style="font-size:0.85rem;color:var(--text2);">自定义工具 (${customTools.length})</span>
                    <button class="btn-add-small" onclick="toggleAllToolsType('custom', ${!allCustomEnabled})">${allCustomEnabled ? '全部关闭' : '全部开启'}</button>
                </div>
            `;
            html += customTools.map(t => renderToolItem(t)).join('');
        }
        
        // MCP 工具
        if (mcpTools.length > 0) {
            html += `
                <div class="settings-panel-header" style="padding:8px 0;border-bottom:1px solid var(--border);margin-top:12px;">
                    <span style="font-size:0.85rem;color:var(--text2);">MCP 工具 (${mcpTools.length})</span>
                </div>
            `;
            html += mcpTools.map(t => renderToolItem(t)).join('');
        }
        
        panel.innerHTML = html;
    } catch (e) {
        panel.innerHTML = '<div style="padding:20px;color:var(--error);text-align:center">加载失败</div>';
    }
}

function renderToolItem(tool) {
    return `
        <div class="provider-item" style="cursor:default;">
            <div style="display:flex;justify-content:space-between;align-items:center;width:100%;">
                <div style="flex:1;min-width:0;">
                    <div class="provider-item-name">${escapeHtml(tool.name)}</div>
                    <div class="provider-item-detail">${escapeHtml((tool.description || '').substring(0, 50))}${(tool.description || '').length > 50 ? '...' : ''}</div>
                </div>
                <label class="toggle-switch" style="margin-left:12px;">
                    <input type="checkbox" ${tool.enabled ? 'checked' : ''} onchange="toggleSingleTool('${escapeHtml(tool.name)}', this.checked)">
                    <span class="toggle-slider"></span>
                </label>
            </div>
        </div>
    `;
}

async function toggleSingleTool(name, enabled) {
    try {
        await fetch(`/nex/tools/${encodeURIComponent(name)}/toggle?enabled=${enabled}`, { method: 'PUT' });
        await loadToolbarToolsCount();
        // 重新加载工具列表以更新"全部开启/关闭"按钮状态
        await loadToolsListPanel();
    } catch (e) {
        showToast('切换失败', 'error');
    }
}

async function toggleAllToolsType(type, enabled) {
    try {
        await fetch(`/nex/tools/toggle-all?enabled=${enabled}&tool_type=${type}`, { method: 'PUT' });
        await loadToolsListPanel();
        await loadToolbarToolsCount();
    } catch (e) {
        showToast('切换失败', 'error');
    }
}

async function reloadToolsFromSettings() {
    try {
        const r = await fetch('/nex/tools/reload', { method: 'POST' });
        const d = await r.json();
        if (d.data.errors && d.data.errors.length > 0) {
            showToast(`加载完成，${d.data.errors.length} 个工具出错`, 'warning');
        } else {
            showToast(`已加载 ${d.data.loaded.length} 个自定义工具`, 'success');
        }
        await loadToolsListPanel();
        await loadToolbarToolsCount();
    } catch (e) {
        showToast('刷新失败', 'error');
    }
}

async function toggleToolsEnabledFromSettings(enabled) {
    await toggleToolsEnabled(enabled);
    await loadToolsListPanel();
    updateMCPPanelTitle();
}

function updateMCPPanelTitle() {
    const title = document.querySelector('#panel-mcp .settings-panel-header h4');
    if (title) {
        title.textContent = toolsEnabled ? 'MCP 服务器' : 'MCP 服务器（工具调用已被关闭）';
    }
}

// ========== MCP 服务器管理 ==========
async function loadMCPListPanel() {
    updateMCPPanelTitle();
    try {
        const r = await fetch('/nex/mcp/servers');
        const d = await r.json();
        const panel = document.getElementById('mcpListPanel');
        if (d.data.length === 0) {
            panel.innerHTML = '<div style="padding:20px;color:var(--text2);text-align:center">暂无 MCP 服务器<br><span style="font-size:0.85rem">点击上方按钮添加</span></div>';
            return;
        }
        panel.innerHTML = d.data.map(function (s) {
            var statusClass = s.connected ? 'connected' : 'disconnected';
            var statusText = s.connected ? '已连接' : '未连接';
            var isEnabled = s.enabled !== false;
            return `<div class="mcp-item ${currentMCPIdEdit === s.id ? 'active' : ''}" onclick="selectMCP('${s.id}')">
                        <label class="toggle-switch" onclick="event.stopPropagation()">
                            <input type="checkbox" ${isEnabled ? 'checked' : ''} onchange="toggleMCPEnabled('${s.id}', this.checked)">
                            <span class="toggle-slider"></span>
                        </label>
                        <div class="mcp-item-content">
                            <div class="mcp-item-name"><span class="status-dot ${statusClass}"></span>${escapeHtml(s.name)}</div>
                            <div class="mcp-item-detail">${statusText} · ${s.tool_count || 0} 个工具</div>
                        </div>
                    </div>`;
        }).join('');
    } catch (e) { showToast('加载失败: ' + e.message, 'error'); }
}

async function toggleMCPEnabled(id, enabled) {
    try {
        showToast(enabled ? '正在连接...' : '正在断开...', 'info', 2000);
        const r = await fetch('/nex/mcp/servers/' + id, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ enabled })
        });
        if (!r.ok) {
            showToast('操作失败', 'error');
            await loadMCPListPanel();
            return;
        }
        // 等待一下让后台连接完成
        await new Promise(resolve => setTimeout(resolve, 1000));
        await loadMCPListPanel();
        await loadToolbarToolsCount(); // 刷新工具数量
        // 检查连接状态
        const statusR = await fetch('/nex/mcp/servers');
        const statusD = await statusR.json();
        const server = statusD.data.find(s => s.id === id);
        if (enabled) {
            if (server && server.connected) {
                showToast('连接成功', 'success');
            } else {
                showToast('连接中，请稍后刷新查看状态', 'warning');
            }
        } else {
            showToast('已禁用', 'info');
        }
    } catch (e) { showToast('操作失败: ' + e.message, 'error'); await loadMCPListPanel(); }
}

function showAddMCPInline() {
    currentMCPIdEdit = null;
    document.getElementById('mcpDetailTitle').textContent = '添加 MCP 服务器';
    document.getElementById('mcpIdInput').value = '';
    document.getElementById('mcpIdInput').disabled = false;
    document.getElementById('mcpNameInput').value = '';
    document.getElementById('mcpTypeInput').value = 'sse';
    document.getElementById('mcpUrlInput').value = '';
    document.getElementById('mcpHeadersInput').value = '';
    document.getElementById('detail-mcp').classList.add('active');
}

async function selectMCP(id) {
    currentMCPIdEdit = id;
    try {
        const r = await fetch('/nex/mcp/servers');
        const d = await r.json();
        const server = d.data.find(s => s.id === id);
        if (!server) { showAlert('服务器不存在', '错误', 'error'); return; }
        document.getElementById('mcpDetailTitle').textContent = '编辑 MCP 服务器';
        document.getElementById('mcpIdInput').value = id;
        document.getElementById('mcpIdInput').disabled = true;
        document.getElementById('mcpNameInput').value = server.name;
        document.getElementById('mcpTypeInput').value = server.server_type || 'sse';
        document.getElementById('mcpUrlInput').value = server.url;
        document.getElementById('mcpHeadersInput').value = server.headers ? JSON.stringify(server.headers, null, 2) : '';
        document.getElementById('detail-mcp').classList.add('active');
        await loadMCPListPanel();
    } catch (e) { showToast('加载失败: ' + e.message, 'error'); }
}

async function saveMCPInline() {
    const id = document.getElementById('mcpIdInput').value.trim();
    const name = document.getElementById('mcpNameInput').value.trim();
    const serverType = document.getElementById('mcpTypeInput').value;
    const url = document.getElementById('mcpUrlInput').value.trim();
    const headersText = document.getElementById('mcpHeadersInput').value.trim();

    if (!id || !name || !url) { showAlert('请填写完整信息', '提示', 'warning'); return; }

    let headers = null;
    if (headersText) {
        try { headers = JSON.parse(headersText); }
        catch (e) { showAlert('请求头格式错误', '格式错误', 'error'); return; }
    }

    try {
        if (currentMCPIdEdit) {
            await fetch('/nex/mcp/servers/' + currentMCPIdEdit, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, url, server_type: serverType, headers }) });
        } else {
            const r = await fetch('/nex/mcp/servers', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id, name, url, server_type: serverType, headers }) });
            const d = await r.json();
            if (d.code !== 0) { showToast('添加失败: ' + (d.detail || d.message), 'error'); return; }
            if (!d.data.connected) { showToast('添加成功，正在后台连接...', 'warning', 5000); }
            currentMCPIdEdit = id;
        }
        showToast('保存成功', 'success');
        closeMCPDetail();
    } catch (e) { showToast('保存失败: ' + e.message, 'error'); }
}

function closeMCPDetail() {
    closeSettingsDetail('detail-mcp', () => {
        currentMCPIdEdit = null;
        loadMCPListPanel();
        loadToolbarToolsCount();
    });
}

// ========== 确认弹窗 ==========
function showConfirm(title, text, callback) {
    document.getElementById('confirmModalTitle').innerHTML = iconWarning + ' ' + title;
    document.getElementById('confirmText').textContent = text;
    confirmCallback = callback;
    document.getElementById('confirmModal').classList.add('show');
}

function closeConfirm() { document.getElementById('confirmModal').classList.remove('show'); confirmCallback = null; }
function doConfirm() { if (confirmCallback) confirmCallback(); closeConfirm(); }

function editSession(id, name) {
    editingSessionId = id;
    document.getElementById('editSessionName').value = name;
    document.getElementById('editModalTitle').innerHTML = iconEditLg + ' 编辑会话名称';
    document.getElementById('editModal').classList.add('show');
}

async function saveSessionName() {
    const name = document.getElementById('editSessionName').value.trim();
    if (!name) return;
    try {
        await fetch(`/nex/sessions/${editingSessionId}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name }) });
        closeEditModal();
        await updateSessionList();
    } catch (e) { showToast('保存失败: ' + e.message, 'error'); }
}

function closeEditModal() { document.getElementById('editModal').classList.remove('show'); editingSessionId = null; }

function deleteSession(id) {
    showConfirm('删除会话', '确定要删除这个会话吗？', async function () {
        try {
            await fetch('/nex/sessions/' + id, { method: 'DELETE' });
            const wasCurrentSession = currentSessionId === id;
            if (wasCurrentSession) currentSessionId = null;
            await loadPersonaGroupedSessions();
            // 如果删除的是当前会话且没有其他会话可选，清空右侧内容
            if (wasCurrentSession && !currentSessionId) {
                document.getElementById('sessionTitle').textContent = 'NexAgent';
                showEmptyState();
                document.getElementById('currentPersonaName').textContent = '';
                window.currentPersonaAvatar = '';
            }
        } catch (e) { showToast('删除失败: ' + e.message, 'error'); }
    });
}

// ========== 新建会话弹窗 ==========
function showNewSessionModal() {
    loadNewSessionPersonaOptions();
    document.getElementById('newSessionName').value = '';
    document.getElementById('newSessionPersonaValue').value = '';
    document.getElementById('newSessionPersonaSelect').querySelector('.custom-select-text').textContent = '默认（通用助手）';
    document.getElementById('newSessionModal').classList.add('show');
}

function closeNewSessionModal() {
    document.getElementById('newSessionModal').classList.remove('show');
    document.getElementById('newSessionPersonaSelect').classList.remove('open');
}

async function loadNewSessionPersonaOptions() {
    try {
        const r = await fetch('/nex/personas');
        const d = await r.json();
        const menu = document.getElementById('newSessionPersonaMenu');
        let html = `
                    <div class="custom-select-item active" onclick="selectNewSessionPersona('', '默认（通用助手）')">
                        <div class="custom-select-item-icon" style="background:var(--text2)">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                                <circle cx="12" cy="7" r="4"/>
                            </svg>
                        </div>
                        <span class="custom-select-item-text">默认（通用助手）</span>
                    </div>
                `;
        d.data.forEach(p => {
            const iconHtml = p.avatar 
                ? `<img src="${p.avatar}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">`
                : p.name.charAt(0).toUpperCase();
            html += `
                        <div class="custom-select-item" onclick="selectNewSessionPersona('${p.id}', '${escapeHtml(p.name)}')">
                            <div class="custom-select-item-icon" style="background:${p.avatar ? 'transparent' : getPersonaColor(p.id)}">
                                ${iconHtml}
                            </div>
                            <span class="custom-select-item-text">${escapeHtml(p.name)}</span>
                        </div>
                    `;
        });
        menu.innerHTML = html;
    } catch (e) { console.error('加载角色卡失败', e); }
}

function toggleCustomSelect(id) {
    const select = document.getElementById(id);
    const wasOpen = select.classList.contains('open');

    // 关闭所有自定义选择器
    document.querySelectorAll('.custom-select').forEach(s => s.classList.remove('open'));

    if (!wasOpen) {
        select.classList.add('open');
    }
}

function selectNewSessionPersona(value, text) {
    document.getElementById('newSessionPersonaValue').value = value;
    document.getElementById('newSessionPersonaSelect').querySelector('.custom-select-text').textContent = text;
    document.getElementById('newSessionPersonaSelect').classList.remove('open');

    // 更新选中状态
    document.querySelectorAll('#newSessionPersonaMenu .custom-select-item').forEach(item => {
        item.classList.remove('active');
    });
    event.currentTarget.classList.add('active');
}

async function createNewSession() {
    const personaId = document.getElementById('newSessionPersonaValue').value;
    const name = document.getElementById('newSessionName').value.trim() || '新会话';

    try {
        const r = await fetch('/nex/sessions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, user: getUser() })
        });
        const d = await r.json();
        const newSessionId = d.data.session_id;

        if (personaId) {
            await fetch(`/nex/sessions/${newSessionId}/persona`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ persona_id: parseInt(personaId) })
            });
        }

        currentSessionId = newSessionId;
        expandedPersonas.add(personaId ? parseInt(personaId) : 'default');
        closeNewSessionModal();
        await loadPersonaGroupedSessions();
    } catch (e) { showToast('创建失败: ' + e.message, 'error'); }
}

// ========== 消息管理 ==========
async function loadMessages(sessionId) {
    try {
        const r = await fetch('/nex/sessions/' + sessionId + '/messages');
        const d = await r.json();
        const sr = await fetch('/nex/sessions/' + sessionId);
        const sd = await sr.json();
        document.getElementById('sessionTitle').textContent = sd.data.name;
        renderMessages(d.data);
    } catch { }
}

function renderMessages(messages) {
    const container = document.getElementById('msgs');
    if (messages.length === 0) {
        showEmptyState();
        return;
    }
    
    container.innerHTML = messages.map(function (m) {
        if (m.role === 'user') {
            return '<div class="msg-wrapper user">' +
                '<div class="msg user" data-id="' + m.id + '">' +
                '<div class="msg-content">' + fmt(m.content) + '</div>' +
                '<div class="msg-footer"><span></span><div class="msg-actions">' +
                '<button class="msg-action-btn" onclick="editMsg(' + m.id + ',\'user\')" title="编辑">' + iconEdit + '</button>' +
                '<button class="msg-action-btn delete" onclick="deleteMsg(' + m.id + ')" title="删除">' + iconDelete + '</button>' +
                '</div></div></div></div>';
        } else {
            var content = '';
            var extra = m.extra || {};
            if (extra.content_parts) {
                for (var i = 0; i < extra.content_parts.length; i++) {
                    var part = extra.content_parts[i];
                    if (part.type === 'text') content += fmt(part.content);
                    else if (part.type === 'tool') content += createToolCardHtml(part.name, part.args, part.result, 'h' + m.id + '-' + toolIdCounter++);
                    else if (part.type === 'thinking') content += createThinkingCardHtml(part.content, 'h' + m.id + '-think-' + toolIdCounter++);
                }
            } else {
                content = fmt(m.content);
                if (extra.tool_calls) {
                    for (var j = 0; j < extra.tool_calls.length; j++) {
                        var tc = extra.tool_calls[j];
                        content += createToolCardHtml(tc.name, tc.args, tc.result, 'h' + m.id + '-' + toolIdCounter++);
                    }
                }
            }
            var tokens = extra.tokens;
            var tokensHtml = tokens ? '<span class="msg-tokens">' + iconTokens + ' ' + tokens.total + ' tokens</span>' : '<span></span>';
            // 如果消息被中断，显示提示
            if (extra.interrupted) {
                tokensHtml = '<span class="msg-tokens">' + iconTokens + ' 输出被中断，无法显示Token消耗</span>';
            }
            var avatarHtml = getAiAvatarHtml();
            return '<div class="msg-wrapper ai">' +
                avatarHtml +
                '<div class="msg ai" data-id="' + m.id + '">' +
                '<div class="msg-content">' + content + '</div>' +
                '<div class="msg-footer">' + tokensHtml +
                '<div class="msg-actions">' +
                '<button class="msg-action-btn" onclick="copyMsg(' + m.id + ')" title="复制">' + iconCopy + '</button>' +
                '<button class="msg-action-btn" onclick="regenerateMsg()" title="重新生成">' + iconRefresh + '</button>' +
                '<button class="msg-action-btn delete" onclick="deleteMsg(' + m.id + ')" title="删除">' + iconDelete + '</button>' +
                '</div></div></div></div>';
        }
    }).join('');
    container.scrollTop = container.scrollHeight;
}

function getAiAvatarHtml() {
    if (window.avatarMode === 'hide') return '';
    
    const defaultIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>';
    
    // 检查当前角色卡是否有自定义头像
    if (window.currentPersonaAvatar) {
        return `<div class="msg-avatar"><img src="${window.currentPersonaAvatar}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;"></div>`;
    }
    
    if (window.avatarMode === 'text') {
        // 文字头像模式：显示角色名首字母
        const personaName = document.getElementById('currentPersonaName')?.textContent || '默认';
        const firstLetter = personaName.charAt(0).toUpperCase();
        const bgColor = currentSessionPersonaId ? getPersonaColor(currentSessionPersonaId) : 'var(--text2)';
        return `<div class="msg-avatar" style="background:${bgColor};color:white;font-weight:600;font-size:0.8rem;">${firstLetter}</div>`;
    }
    
    // 消息图标模式（默认）
    return '<div class="msg-avatar">' + defaultIcon + '</div>';
}

function showEmptyState() {
    document.getElementById('msgs').innerHTML = `
        <div class="empty-state">
            <div class="icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="80" height="80">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                </svg>
            </div>
            <div class="empty-state-title">NexAgent 助手</div>
            <div class="empty-state-status">
                <span class="status-dot"></span>
                在线
            </div>
            <div class="empty-state-desc">输入消息开始对话</div>
        </div>`;
}

function showWelcomeState() {
    document.getElementById('msgs').innerHTML = `
        <div class="empty-state">
            <div class="icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="80" height="80">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                </svg>
            </div>
            <div class="empty-state-title">欢迎使用 NexAgent</div>
            <div class="empty-state-status">
                <span class="status-dot"></span>
                在线
            </div>
            <div class="empty-state-desc">输入消息开始对话，将自动创建新会话</div>
        </div>`;
}

function editMsg(id, role) {
    editingMsgId = id;
    editingMsgRole = role;
    document.getElementById('editMsgModalTitle').innerHTML = iconEditLg + ' 编辑消息';
    const msgEl = document.querySelector(`.msg[data-id="${id}"] .msg-content`);
    fetch(`/nex/messages/${id}`).then(r => r.json()).then(d => {
        document.getElementById('editMsgContent').value = d.data.content;
        document.getElementById('editMsgModal').classList.add('show');
    });
}

async function saveEditedMsg(regenerate) {
    const content = document.getElementById('editMsgContent').value.trim();
    if (!content) return;

    // 保存当前编辑状态，因为 closeEditMsgModal 会清除它们
    const msgId = editingMsgId;
    const msgRole = editingMsgRole;

    try {
        const r = await fetch(`/nex/messages/${msgId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content, regenerate: regenerate && msgRole === 'user' })
        });
        const d = await r.json();
        if (d.code !== 0) {
            showAlert('保存失败: ' + (d.detail || d.message), '错误', 'error');
            return;
        }
        closeEditMsgModal();
        if (regenerate && msgRole === 'user' && d.data && d.data.session_id) {
            // 先加载消息（显示更新后的用户消息，AI回复已被删除）
            await loadMessages(d.data.session_id);
            // 重新发送消息，不保存用户消息（因为已存在）
            await sendMessage(content, false);
        } else {
            await loadMessages(currentSessionId);
        }
    } catch (e) { showToast('保存失败: ' + e.message, 'error'); }
}

function closeEditMsgModal() { document.getElementById('editMsgModal').classList.remove('show'); editingMsgId = null; editingMsgRole = null; }

function deleteMsg(id) {
    showConfirm('删除消息', '确定要删除这条消息吗？', async () => {
        try {
            await fetch(`/nex/messages/${id}`, { method: 'DELETE' });
            await loadMessages(currentSessionId);
        } catch (e) { showToast('删除失败: ' + e.message, 'error'); }
    });
}

async function regenerateMsg() {
    if (!currentSessionId || busy) return;
    try {
        const r = await fetch(`/nex/sessions/${currentSessionId}/regenerate`, { method: 'POST' });
        const d = await r.json();
        if (d.code !== 0) {
            showAlert('重新生成失败: ' + (d.detail || d.message || '未知错误'), '错误', 'error');
            return;
        }
        if (!d.data || !d.data.message) {
            showAlert('没有找到可重新生成的消息', '重新生成失败', 'error');
            return;
        }
        await loadMessages(currentSessionId);
        await sendMessage(d.data.message, false);
    } catch (e) { showToast('重新生成失败: ' + e.message, 'error'); }
}

async function clearMsgs() {
    if (!currentSessionId) return;
    showConfirm('清空消息', '确定要清空当前会话的所有消息吗？', async () => {
        try {
            await fetch(`/nex/sessions/${currentSessionId}/messages`, { method: 'DELETE' });
            await loadMessages(currentSessionId);
            await loadPersonaGroupedSessions(); // 刷新侧边栏显示正确的消息数
        } catch (e) { showToast('清空失败: ' + e.message, 'error'); }
    });
}

// ========== 发送消息 ==========
function send() {
    const inp = document.getElementById('inp');
    const msg = inp.value.trim();
    if (!msg || busy) return;
    inp.value = '';
    inp.dataset.userInput = '';
    resetTextareaHeight();
    sendMessage(msg, true);
}

async function sendMessage(message, saveUserMsg) {
    if (busy) return;
    busy = true;
    document.getElementById('btn').disabled = true;
    
    // 如果没有当前会话，先创建一个
    if (!currentSessionId) {
        try {
            const r = await fetch('/nex/sessions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: '新会话', user: getUser() })
            });
            const d = await r.json();
            currentSessionId = d.data.session_id;
            expandedPersonas.add('default');
            // 更新侧边栏
            await loadPersonaGroupedSessions();
        } catch (e) {
            showToast('创建会话失败: ' + e.message, 'error');
            busy = false;
            document.getElementById('btn').disabled = false;
            return;
        }
    }
    
    // 创建AbortController用于停止生成
    currentAbortController = new AbortController();
    
    // 显示停止按钮
    const btnEl = document.getElementById('btn');
    btnEl.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>';
    btnEl.disabled = false;
    btnEl.onclick = stopGeneration;

    // 保存消息用于重试
    lastSentMessage = message;

    const container = document.getElementById('msgs');
    if (container.querySelector('.empty-state')) container.innerHTML = '';

    // 检查用户是否在底部附近（用于智能滚动）
    const isNearBottom = () => {
        const threshold = 100; // 距离底部100px以内认为在底部
        return container.scrollHeight - container.scrollTop - container.clientHeight < threshold;
    };

    // 智能滚动：只在用户在底部附近时才自动滚动
    const smartScroll = () => {
        if (isNearBottom()) {
            container.scrollTop = container.scrollHeight;
        }
    };

    const aiAvatarHtml = getAiAvatarHtml();

    if (saveUserMsg) {
        container.innerHTML += `<div class="msg-wrapper user"><div class="msg user"><div class="msg-content">${fmt(message)}</div></div></div>`;
    }

    const aiMsgId = 'ai-' + Date.now();
    container.innerHTML += `<div class="msg-wrapper ai">${aiAvatarHtml}<div class="msg ai" id="${aiMsgId}"><div class="msg-content"><div class="typing"><span></span><span></span><span></span></div></div><div class="msg-footer" style="display:none"><span class="msg-tokens"></span><div class="msg-actions"><button class="msg-action-btn" onclick="copyMsgById('${aiMsgId}')" title="复制">${iconCopy}</button><button class="msg-action-btn" onclick="regenerateMsg()" title="重新生成">${iconRefresh}</button><button class="msg-action-btn delete" onclick="deleteMsgAndReload()" title="删除">${iconDelete}</button></div></div></div></div>`;
    container.scrollTop = container.scrollHeight;

    let totalTokens = 0;
    
    // 声明这些变量在try块外，以便在catch块中使用
    let contentParts = [];
    let currentTextContent = '';
    let currentThinkingContent = '';
    let currentToolId = null;
    let currentThinkingId = null;
    let isThinking = false;

    try {
        const response = await fetch('/nex/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user: getUser(),
                message,
                session_id: currentSessionId,
                stream: true,
                save_user_message: saveUserMsg,
                use_system_prompt: systemPromptEnabled,
                model_key: currentModelKey
            }),
            signal: currentAbortController.signal
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        // 内容流：按顺序保存各种内容块
        const aiMsg = document.getElementById(aiMsgId);
        const contentEl = aiMsg.querySelector('.msg-content');

        // 重新渲染内容的函数
        function renderContent() {
            let html = '';
            // 按顺序渲染内容块
            for (const part of contentParts) {
                if (part.type === 'thinking') {
                    html += createThinkingCardHtml(part.content, part.id, true);
                } else if (part.type === 'text') {
                    html += fmt(part.content);
                } else if (part.type === 'tool') {
                    html += createToolCardHtml(part.name, part.args, part.result, part.id);
                }
            }
            // 渲染当前正在进行的思考
            if (isThinking && currentThinkingId) {
                html += createThinkingCardHtml(currentThinkingContent, currentThinkingId, false);
            }
            // 渲染当前正在接收的文本
            if (currentTextContent) {
                html += fmt(currentTextContent);
            }
            contentEl.innerHTML = html;
        }

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            const text = decoder.decode(value);
            const lines = text.split('\n');
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.slice(6));
                        if (data.type === 'content') {
                            currentTextContent += data.data;
                            renderContent();
                        } else if (data.type === 'thinking_start') {
                            // 保存之前的文本（如果有）
                            if (currentTextContent) {
                                contentParts.push({ type: 'text', content: currentTextContent });
                                currentTextContent = '';
                            }
                            isThinking = true;
                            currentThinkingId = 'think-' + toolIdCounter++;
                            currentThinkingContent = '';
                            renderContent();
                        } else if (data.type === 'thinking') {
                            currentThinkingContent += data.data;
                            updateThinkingContent(currentThinkingId, currentThinkingContent, false);
                        } else if (data.type === 'thinking_end') {
                            // 保存完成的思考到 contentParts
                            contentParts.push({ type: 'thinking', id: currentThinkingId, content: currentThinkingContent });
                            isThinking = false;
                            currentThinkingContent = '';
                            renderContent();
                        } else if (data.type === 'tool_start') {
                            // 保存工具调用前的文本
                            if (currentTextContent) {
                                contentParts.push({ type: 'text', content: currentTextContent });
                                currentTextContent = '';
                            }
                            currentToolId = 'tool-' + toolIdCounter++;
                            contentParts.push({ type: 'tool', id: currentToolId, name: data.data.name, args: data.data.args, result: undefined });
                            renderContent();
                        } else if (data.type === 'tool_end') {
                            // 更新工具结果
                            const tool = contentParts.find(p => p.type === 'tool' && p.id === currentToolId);
                            if (tool) tool.result = data.data.result;
                            updateToolResult(currentToolId, data.data.result);
                        } else if (data.type === 'done') {
                            // 保存最后的文本内容
                            if (currentTextContent) {
                                contentParts.push({ type: 'text', content: currentTextContent });
                                currentTextContent = '';
                            }
                            if (data.session_id) currentSessionId = data.session_id;
                            if (data.tokens) totalTokens = data.tokens.total || 0;
                            // 最终渲染
                            renderContent();
                        }
                    } catch { }
                }
            }
            smartScroll();
        }

        // 确保最终内容被渲染
        if (currentTextContent) {
            contentParts.push({ type: 'text', content: currentTextContent });
            renderContent();
        }

        // 流式输出完成后，重新加载消息以获取正确的消息ID和操作栏
        await loadMessages(currentSessionId);
    } catch (e) {
        // 如果是用户主动停止，不显示错误
        if (e.name === 'AbortError') {
            // 保存已生成的内容
            if (currentTextContent) {
                contentParts.push({ type: 'text', content: currentTextContent });
                currentTextContent = '';
            }
            if (isThinking && currentThinkingId) {
                contentParts.push({ type: 'thinking', id: currentThinkingId, content: currentThinkingContent });
                isThinking = false;
                currentThinkingContent = '';
            }
            // 重新渲染已生成的内容
            let html = '';
            for (const part of contentParts) {
                if (part.type === 'thinking') {
                    html += createThinkingCardHtml(part.content, part.id, true);
                } else if (part.type === 'text') {
                    html += fmt(part.content);
                } else if (part.type === 'tool') {
                    html += createToolCardHtml(part.name, part.args, part.result, part.id);
                }
            }
            let aiMsg = document.getElementById(aiMsgId);
            if (aiMsg) {
                const contentEl = aiMsg.querySelector('.msg-content');
                contentEl.innerHTML = html;
            }
            
            // 构建完整内容
            let fullContent = '';
            for (const part of contentParts) {
                if (part.type === 'text') {
                    fullContent += part.content;
                }
            }
            
            // 显示footer和提示信息
            aiMsg = document.getElementById(aiMsgId);
            if (aiMsg) {
                const footerEl = aiMsg.querySelector('.msg-footer');
                if (footerEl) {
                    footerEl.style.display = 'flex';
                    footerEl.innerHTML = `
                        <span class="msg-tokens">输出被中断，无法显示Token消耗</span>
                        <div class="msg-actions">
                            <button class="msg-action-btn" onclick="copyMsgById('${aiMsgId}')" title="复制">${iconCopy}</button>
                            <button class="msg-action-btn" onclick="regenerateMsg()" title="重新生成">${iconRefresh}</button>
                            <button class="msg-action-btn delete" onclick="deleteMsgAndReload()" title="删除">${iconDelete}</button>
                        </div>
                    `;
                }
            }
            
            // 发送保存请求到服务器
            try {
                await fetch('/nex/messages/save', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        session_id: currentSessionId,
                        content: fullContent,
                        content_parts: contentParts,
                        tokens: totalTokens > 0 ? { total: totalTokens } : null,
                        interrupted: true  // 标记为被中断
                    })
                });
                showToast('已保存已生成的内容', 'info', 2000);
            } catch (saveErr) {
                console.error('保存消息失败:', saveErr);
                showToast('已停止生成，但保存失败', 'warning', 2000);
            }
            // 重新加载消息以显示保存的内容
            await loadMessages(currentSessionId);
            
            // 重新加载后，再次设置footer提示
            setTimeout(() => {
                const container = document.getElementById('msgs');
                const allAiMsgs = container.querySelectorAll('.msg.ai');
                if (allAiMsgs.length > 0) {
                    const lastAiMsg = allAiMsgs[allAiMsgs.length - 1];
                    const footerEl = lastAiMsg.querySelector('.msg-footer');
                    if (footerEl) {
                        footerEl.style.display = 'flex';
                        const msgId = lastAiMsg.getAttribute('data-id') || lastAiMsg.id;
                        footerEl.innerHTML = `
                            <span class="msg-tokens">${iconTokens} 输出被中断，无法显示Token消耗</span>
                            <div class="msg-actions">
                                <button class="msg-action-btn" onclick="copyMsgById('${msgId}')" title="复制">${iconCopy}</button>
                                <button class="msg-action-btn" onclick="regenerateMsg()" title="重新生成">${iconRefresh}</button>
                                <button class="msg-action-btn delete" onclick="deleteMsgAndReload()" title="删除">${iconDelete}</button>
                            </div>
                        `;
                    }
                }
            }, 100);
        } else {
            const aiMsg = document.getElementById(aiMsgId);
            if (aiMsg) {
                const contentEl = aiMsg.querySelector('.msg-content');
                const footerEl = aiMsg.querySelector('.msg-footer');
                contentEl.innerHTML = `<span style="color:var(--error)">发送失败: ${escapeHtml(e.message)}</span>`;
                // 显示操作栏，提供重试选项
                if (footerEl) {
                    footerEl.style.display = 'flex';
                    footerEl.innerHTML = `
                                <span class="msg-tokens" style="color:var(--error)">请求失败</span>
                                <div class="msg-actions">
                                    <button class="msg-action-btn" onclick="retryLastMessage()" title="重试">
                                        ${iconRefresh}
                                    </button>
                                    <button class="msg-action-btn delete" onclick="removeErrorMessage('${aiMsgId}')" title="删除">
                                        ${iconDelete}
                                    </button>
                                </div>
                            `;
                }
            }
        }
    }

    busy = false;
    document.getElementById('btn').disabled = false;
    // 恢复发送按钮
    const btnElRestore = document.getElementById('btn');
    btnElRestore.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>';
    btnElRestore.onclick = () => {
        const inp = document.getElementById('inp');
        const msg = inp.value.trim();
        if (msg) { inp.value = ''; sendMessage(msg, true); }
    };
    currentAbortController = null;
    await updateSessionList();
}

function copyMsgById(id) {
    const msgEl = document.getElementById(id)?.querySelector('.msg-content');
    if (msgEl) {
        navigator.clipboard.writeText(msgEl.innerText);
        showToast('已复制到剪贴板', 'success', 2000);
    }
}

function copyMsg(id) {
    const msgEl = document.querySelector(`.msg[data-id="${id}"] .msg-content`);
    if (msgEl) {
        navigator.clipboard.writeText(msgEl.innerText);
        showToast('已复制到剪贴板', 'success', 2000);
    }
}

// 保存最后发送的消息，用于重试
let lastSentMessage = null;
// 用于停止输出的AbortController
let currentAbortController = null;

function stopGeneration() {
    if (currentAbortController) {
        currentAbortController.abort();
        currentAbortController = null;
    }
}

function removeErrorMessage(msgId) {
    const msg = document.getElementById(msgId);
    if (msg) msg.remove();
}

async function retryLastMessage() {
    if (!lastSentMessage) {
        showToast('没有可重试的消息', 'warning');
        return;
    }
    // 移除错误消息
    const container = document.getElementById('msgs');
    const errorMsgs = container.querySelectorAll('.msg.ai');
    if (errorMsgs.length > 0) {
        const lastAiMsg = errorMsgs[errorMsgs.length - 1];
        if (lastAiMsg.querySelector('.msg-content span[style*="error"]')) {
            lastAiMsg.remove();
        }
    }
    // 重新发送
    await sendMessage(lastSentMessage, false);
}

async function deleteMsgAndReload() {
    // 删除最后一条AI消息，需要先刷新获取消息ID
    await loadMessages(currentSessionId);
}

// 初始化
init();

// ========== OpenAPI 配置管理 ==========
let currentOpenAPIConfigEdit = null;

async function loadOpenAPIConfigsPanel() {
    try {
        const r = await fetch('/nex/openapi/configs');
        const d = await r.json();
        const panel = document.getElementById('openAPIListPanel');

        if (!panel) {
            console.error('OpenAPI配置面板不存在');
            return;
        }

        if (d.data.length === 0) {
            panel.innerHTML = '<div style="padding:20px;color:var(--text2);text-align:center">暂无OpenAPI配置<br><span style="font-size:0.85rem">点击上方按钮添加</span></div>';
            return;
        }

        panel.innerHTML = d.data.map(config => `
            <div class="mcp-item ${currentOpenAPIConfigEdit === config.api_model_id ? 'active' : ''}" onclick="selectOpenAPIConfig('${escapeHtml(config.api_model_id)}')">
                <div class="mcp-item-content">
                    <div class="mcp-item-name">${escapeHtml(config.api_model_id)}</div>
                    <div class="mcp-item-detail">
                        模型: ${escapeHtml(config.model_name || config.internal_model_key)} · 
                        角色: ${escapeHtml(config.persona_name || '默认')} · 
                        ${config.use_system_prompt ? '启用系统提示词' : '关闭系统提示词'}
                    </div>
                </div>
            </div>
        `).join('');
    } catch (e) {
        showToast('加载失败: ' + e.message, 'error');
    }
}

function showAddOpenAPIConfig() {
    currentOpenAPIConfigEdit = null;
    document.getElementById('openAPIDetailTitle').textContent = '添加OpenAPI配置';
    document.getElementById('openAPIModelIdInput').value = '';
    document.getElementById('openAPIModelIdInput').disabled = false;
    document.getElementById('openAPIInternalModelSelect').value = '';
    document.getElementById('openAPIPersonaSelect').value = '';
    document.getElementById('openAPIUseSystemPrompt').checked = false;

    // 加载模型和角色卡列表
    loadOpenAPIModelOptions();
    loadOpenAPIPersonaOptions();

    document.getElementById('detail-openapi').classList.add('active');
}

async function loadOpenAPIModelOptions() {
    try {
        const r = await fetch('/nex/models');
        const d = await r.json();
        const select = document.getElementById('openAPIInternalModelSelect');

        const chatModels = d.data.models.filter(m => m.model_type !== 'embedding');
        select.innerHTML = '<option value="">选择内部模型</option>' +
            chatModels.map(m => `<option value="${m.key}">${escapeHtml(m.name)} (${escapeHtml(m.provider_name)})</option>`).join('');
    } catch (e) {
        console.error('加载模型失败', e);
    }
}

async function loadOpenAPIPersonaOptions() {
    try {
        const r = await fetch('/nex/personas');
        const d = await r.json();
        const select = document.getElementById('openAPIPersonaSelect');

        select.innerHTML = '<option value="">默认（无角色卡）</option>' +
            (d.data || []).map(p => `<option value="${p.id}">${escapeHtml(p.name)}</option>`).join('');
    } catch (e) {
        console.error('加载角色卡失败', e);
    }
}

async function selectOpenAPIConfig(apiModelId) {
    currentOpenAPIConfigEdit = apiModelId;

    try {
        const r = await fetch('/nex/openapi/configs');
        const d = await r.json();
        const config = d.data.find(c => c.api_model_id === apiModelId);

        if (!config) {
            showAlert('配置不存在', '错误', 'error');
            return;
        }

        document.getElementById('openAPIDetailTitle').textContent = '编辑OpenAPI配置';
        document.getElementById('openAPIModelIdInput').value = config.api_model_id;
        document.getElementById('openAPIModelIdInput').disabled = true;
        document.getElementById('openAPIInternalModelSelect').value = config.internal_model_key || '';
        document.getElementById('openAPIPersonaSelect').value = config.persona_id || '';
        document.getElementById('openAPIUseSystemPrompt').checked = config.use_system_prompt === 1;

        // 加载选项
        await loadOpenAPIModelOptions();
        await loadOpenAPIPersonaOptions();

        // 重新设置选中值（因为异步加载）
        document.getElementById('openAPIInternalModelSelect').value = config.internal_model_key || '';
        document.getElementById('openAPIPersonaSelect').value = config.persona_id || '';

        document.getElementById('detail-openapi').classList.add('active');
        await loadOpenAPIConfigsPanel();
    } catch (e) {
        showToast('加载失败: ' + e.message, 'error');
    }
}

async function saveOpenAPIConfig() {
    const apiModelId = document.getElementById('openAPIModelIdInput').value.trim();
    const internalModelKey = document.getElementById('openAPIInternalModelSelect').value;
    const personaId = document.getElementById('openAPIPersonaSelect').value;
    const useSystemPrompt = document.getElementById('openAPIUseSystemPrompt').checked;

    if (!apiModelId || !internalModelKey) {
        showAlert('请填写API模型ID和选择内部模型', '提示', 'warning');
        return;
    }

    try {
        if (currentOpenAPIConfigEdit) {
            // 更新
            await fetch(`/nex/openapi/configs/${currentOpenAPIConfigEdit}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    internal_model_key: internalModelKey,
                    persona_id: personaId ? parseInt(personaId) : null,
                    use_system_prompt: useSystemPrompt
                })
            });
        } else {
            // 创建
            await fetch('/nex/openapi/configs', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    api_model_id: apiModelId,
                    internal_model_key: internalModelKey,
                    persona_id: personaId ? parseInt(personaId) : null,
                    use_system_prompt: useSystemPrompt
                })
            });
        }

        showToast('保存成功', 'success');
        closeOpenAPIDetail();
    } catch (e) {
        showToast('保存失败: ' + e.message, 'error');
    }
}

function closeOpenAPIDetail() {
    closeSettingsDetail('detail-openapi', () => {
        currentOpenAPIConfigEdit = null;
        loadOpenAPIConfigsPanel();
    });
}

async function deleteOpenAPIConfig() {
    if (!currentOpenAPIConfigEdit) return;

    showConfirm('删除配置', '确定要删除这个OpenAPI配置吗？', async function () {
        try {
            await fetch(`/nex/openapi/configs/${currentOpenAPIConfigEdit}`, { method: 'DELETE' });
            showToast('删除成功', 'success');
            closeOpenAPIDetail();
        } catch (e) {
            showToast('删除失败: ' + e.message, 'error');
        }
    });
}