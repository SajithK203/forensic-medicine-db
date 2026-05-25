// main.js — Forensic Medicine DB

document.addEventListener('DOMContentLoaded', function () {

    // ── 1. Auto-dismiss alerts after 5 seconds ──────────────────────────────
    document.querySelectorAll('.alert').forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(function () { alert.remove(); }, 500);
        }, 5000);
    });

    // ── 2. Active nav highlight via URL ────────────────────────────────────
    const path = window.location.pathname;
    document.querySelectorAll('.nav-item').forEach(function (link) {
        const href = link.getAttribute('href');
        if (href && path.startsWith(href) && href !== '/') {
            link.classList.add('active');
        }
    });

    // ── 3. Confirm before form submissions with data-confirm attribute ─────
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            if (!confirm(el.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

    // ── 4. Auto-calculate age from date_of_birth ──────────────────────────
    const dobField = document.getElementById('id_date_of_birth');
    const ageField = document.getElementById('id_age');
    if (dobField && ageField) {
        dobField.addEventListener('change', function () {
            const dob = new Date(this.value);
            if (!isNaN(dob)) {
                const today = new Date();
                let age = today.getFullYear() - dob.getFullYear();
                const m = today.getMonth() - dob.getMonth();
                if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) age--;
                ageField.value = age;
            }
        });
    }

    // ── 5. Table row click to navigate ────────────────────────────────────
    document.querySelectorAll('tr[data-href]').forEach(function (row) {
        row.style.cursor = 'pointer';
        row.addEventListener('click', function () {
            window.location = row.dataset.href;
        });
    });

});
