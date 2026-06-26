/* ============================================================
   BASE.JS — Calendário de Plantões
   Gerencia: dark mode, sidebar mobile, nav ativo
   ============================================================ */

(function () {
    'use strict';

    /* ── Dark Mode ── */
    const DARK_KEY = 'cp_dark_mode';

    function applyTheme(dark) {
        document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
        const label = document.getElementById('darkToggleLabel');
        const icon  = document.getElementById('darkToggleIcon');
        if (label) label.textContent = dark ? 'Modo Claro' : 'Modo Escuro';
        if (icon)  icon.textContent  = dark ? '☀️' : '🌙';
    }

    function initDarkMode() {
        const saved = localStorage.getItem(DARK_KEY);
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const isDark = saved !== null ? saved === 'true' : prefersDark;
        applyTheme(isDark);

        const btn = document.getElementById('darkModeToggle');
        if (!btn) return;

        btn.addEventListener('click', () => {
            const currentlyDark = document.documentElement.getAttribute('data-theme') === 'dark';
            const nextDark = !currentlyDark;
            applyTheme(nextDark);
            localStorage.setItem(DARK_KEY, nextDark);
        });
    }

    /* ── Sidebar Mobile ── */
    function initSidebar() {
        const menuBtn  = document.getElementById('sidebarMenuBtn');
        const sidebar  = document.getElementById('appSidebar');
        const overlay  = document.getElementById('sidebarOverlay');

        if (!menuBtn || !sidebar || !overlay) return;

        function openSidebar() {
            sidebar.classList.add('open');
            overlay.classList.add('open');
            document.body.style.overflow = 'hidden';
        }

        function closeSidebar() {
            sidebar.classList.remove('open');
            overlay.classList.remove('open');
            document.body.style.overflow = '';
        }

        menuBtn.addEventListener('click', openSidebar);
        overlay.addEventListener('click', closeSidebar);

        // Fecha ao clicar em item de nav (mobile)
        sidebar.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', () => {
                if (window.innerWidth <= 768) closeSidebar();
            });
        });
    }

    /* ── Nav Ativo ── */
    function initActiveNav() {
        const currentPath = window.location.pathname;
        document.querySelectorAll('.nav-item').forEach(link => {
            const href = link.getAttribute('href');
            // Compara a URL exata para evitar que múltiplos itens fiquem ativos
            if (href === currentPath) {
                link.classList.add('active');
            }
        });
    }

    /* ── Init ── */
    document.addEventListener('DOMContentLoaded', () => {
        initDarkMode();
        initSidebar();
        initActiveNav();
    });

})();
