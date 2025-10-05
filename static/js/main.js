// JavaScript principal para DocCollab

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips do Bootstrap (se disponível)
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Validação de formulários
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Validação de confirmação de senha
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    
    if (password && confirmPassword) {
        function validatePassword() {
            if (password.value !== confirmPassword.value) {
                confirmPassword.setCustomValidity('As senhas não coincidem');
            } else {
                confirmPassword.setCustomValidity('');
            }
        }
        
        password.addEventListener('change', validatePassword);
        confirmPassword.addEventListener('keyup', validatePassword);
    }

    // Auto-dismiss alerts
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            if (typeof bootstrap !== 'undefined') {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } else {
                // Fallback: remover alert manualmente
                alert.style.display = 'none';
            }
        });
    }, 5000);
});
