// auto-dismiss alerts after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.4s';
            setTimeout(function () { alert.remove(); }, 400);
        }, 4000);
    });

    // highlight active nav link
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(function (link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // confirm delete forms
    document.querySelectorAll('.confirm-delete').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            if (!confirm('Are you sure? This cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
});
