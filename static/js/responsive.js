// ===== RESPONSIVE JAVASCRIPT =====

document.addEventListener('DOMContentLoaded', function() {
    // ===== MOBILE NAVIGATION =====
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            }
        });
        
        // Close menu when clicking on a link
        const navLinks = navMenu.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            });
        });
    }
    
    // ===== DROPDOWN MENUS =====
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        if (toggle && menu) {
            // Desktop hover
            dropdown.addEventListener('mouseenter', function() {
                menu.style.opacity = '1';
                menu.style.visibility = 'visible';
                menu.style.transform = 'translateY(0)';
            });
            
            dropdown.addEventListener('mouseleave', function() {
                menu.style.opacity = '0';
                menu.style.visibility = 'hidden';
                menu.style.transform = 'translateY(-10px)';
            });
            
            // Mobile click
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Close other dropdowns
                dropdowns.forEach(otherDropdown => {
                    if (otherDropdown !== dropdown) {
                        const otherMenu = otherDropdown.querySelector('.dropdown-menu');
                        if (otherMenu) {
                            otherMenu.style.opacity = '0';
                            otherMenu.style.visibility = 'hidden';
                            otherMenu.style.transform = 'translateY(-10px)';
                        }
                    }
                });
                
                // Toggle current dropdown
                const isVisible = menu.style.opacity === '1';
                menu.style.opacity = isVisible ? '0' : '1';
                menu.style.visibility = isVisible ? 'hidden' : 'visible';
                menu.style.transform = isVisible ? 'translateY(-10px)' : 'translateY(0)';
            });
        }
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            dropdowns.forEach(dropdown => {
                const menu = dropdown.querySelector('.dropdown-menu');
                if (menu) {
                    menu.style.opacity = '0';
                    menu.style.visibility = 'hidden';
                    menu.style.transform = 'translateY(-10px)';
                }
            });
        }
    });
    
    // ===== RESPONSIVE GRID LAYOUT =====
    function updateEditorLayout() {
        const editorContainer = document.querySelector('.editor-container');
        if (!editorContainer) return;
        
        const width = window.innerWidth;
        
        if (width <= 768) {
            // Mobile: Stack vertically
            editorContainer.style.gridTemplateColumns = '1fr';
            editorContainer.style.gridTemplateRows = 'auto auto auto';
            editorContainer.style.height = 'auto';
            
            // Reorder elements
            const sidebar = editorContainer.querySelector('.sidebar');
            const editor = editorContainer.querySelector('.editor-panel');
            const pdf = editorContainer.querySelector('.pdf-panel');
            
            if (sidebar) sidebar.style.order = '1';
            if (editor) editor.style.order = '2';
            if (pdf) pdf.style.order = '3';
        } else if (width <= 1024) {
            // Tablet: Smaller sidebar and PDF
            editorContainer.style.gridTemplateColumns = '250px 1fr 350px';
            editorContainer.style.gridTemplateRows = '1fr';
            editorContainer.style.height = 'calc(100vh - 120px)';
            
            // Reset order
            const sidebar = editorContainer.querySelector('.sidebar');
            const editor = editorContainer.querySelector('.editor-panel');
            const pdf = editorContainer.querySelector('.pdf-panel');
            
            if (sidebar) sidebar.style.order = '0';
            if (editor) editor.style.order = '0';
            if (pdf) pdf.style.order = '0';
        } else {
            // Desktop: Full layout
            editorContainer.style.gridTemplateColumns = '300px 1fr 400px';
            editorContainer.style.gridTemplateRows = '1fr';
            editorContainer.style.height = 'calc(100vh - 120px)';
            
            // Reset order
            const sidebar = editorContainer.querySelector('.sidebar');
            const editor = editorContainer.querySelector('.editor-panel');
            const pdf = editorContainer.querySelector('.pdf-panel');
            
            if (sidebar) sidebar.style.order = '0';
            if (editor) editor.style.order = '0';
            if (pdf) pdf.style.order = '0';
        }
    }
    
    // Update layout on resize
    window.addEventListener('resize', updateEditorLayout);
    updateEditorLayout(); // Initial call
    
    // ===== TOUCH GESTURES FOR MOBILE =====
    let touchStartX = 0;
    let touchStartY = 0;
    
    document.addEventListener('touchstart', function(e) {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
    });
    
    document.addEventListener('touchend', function(e) {
        if (!touchStartX || !touchStartY) return;
        
        const touchEndX = e.changedTouches[0].clientX;
        const touchEndY = e.changedTouches[0].clientY;
        
        const diffX = touchStartX - touchEndX;
        const diffY = touchStartY - touchEndY;
        
        // Swipe left to close mobile menu
        if (Math.abs(diffX) > Math.abs(diffY) && diffX > 50) {
            if (navMenu && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            }
        }
        
        touchStartX = 0;
        touchStartY = 0;
    });
    
    // ===== MODAL MANAGEMENT =====
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        const closeBtn = modal.querySelector('.modal-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                modal.classList.remove('active');
            });
        }
        
        // Close on backdrop click
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
    });
    
    // ===== ALERT MANAGEMENT =====
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        const closeBtn = alert.querySelector('.alert-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                alert.style.animation = 'slideOut 0.3s ease forwards';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            });
        }
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.style.animation = 'slideOut 0.3s ease forwards';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            }
        }, 5000);
    });
    
    // ===== SCROLL TO TOP BUTTON =====
    const scrollToTopBtn = document.createElement('button');
    scrollToTopBtn.innerHTML = '↑';
    scrollToTopBtn.className = 'scroll-to-top';
    scrollToTopBtn.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        font-size: 20px;
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 1000;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    `;
    
    document.body.appendChild(scrollToTopBtn);
    
    scrollToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollToTopBtn.style.opacity = '1';
            scrollToTopBtn.style.visibility = 'visible';
        } else {
            scrollToTopBtn.style.opacity = '0';
            scrollToTopBtn.style.visibility = 'hidden';
        }
    });
    
    // ===== PERFORMANCE OPTIMIZATION =====
    // Debounce resize events
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(updateEditorLayout, 250);
    });
    
    // ===== ACCESSIBILITY IMPROVEMENTS =====
    // Keyboard navigation for dropdowns
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            // Close all dropdowns and mobile menu
            dropdowns.forEach(dropdown => {
                const menu = dropdown.querySelector('.dropdown-menu');
                if (menu) {
                    menu.style.opacity = '0';
                    menu.style.visibility = 'hidden';
                    menu.style.transform = 'translateY(-10px)';
                }
            });
            
            if (navMenu) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            }
        }
    });
    
    // Focus management for modals
    modals.forEach(modal => {
        modal.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                modal.classList.remove('active');
            }
        });
    });
});

// ===== UTILITY FUNCTIONS =====
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        // Focus first input
        const firstInput = modal.querySelector('input, textarea, select');
        if (firstInput) {
            setTimeout(() => firstInput.focus(), 100);
        }
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="alert-close" onclick="this.parentElement.remove()">&times;</button>
    `;
    
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.insertBefore(alert, mainContent.firstChild);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.style.animation = 'slideOut 0.3s ease forwards';
                setTimeout(() => alert.remove(), 300);
            }
        }, 5000);
    }
}

// ===== CSS ANIMATIONS =====
const responsiveStyle = document.createElement('style');
responsiveStyle.textContent = `
    @keyframes slideOut {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-20px);
        }
    }
    
    .scroll-to-top:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
`;
document.head.appendChild(responsiveStyle);
