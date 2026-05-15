document.addEventListener("DOMContentLoaded", function () {
    // Toasts
    document.querySelectorAll(".toast-message").forEach(function (el) {
        var tags = el.dataset.tags || "info";
        var bg = { success: "bg-success", error: "bg-danger", warning: "bg-warning text-dark", info: "bg-info text-dark" };
        var toast = document.createElement("div");
        toast.className = "toast align-items-center text-white border-0 " + (bg[tags] || bg.info);
        toast.setAttribute("role", "alert");
        toast.setAttribute("aria-live", "assertive");
        toast.setAttribute("aria-atomic", "true");
        toast.innerHTML = '<div class="d-flex"><div class="toast-body">' + el.textContent + '</div><button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button></div>';
        document.getElementById("toast-container").appendChild(toast);
        new bootstrap.Toast(toast, { delay: 4000 }).show();
        el.remove();
    });

    // Modal confirmation
    document.querySelectorAll("[data-confirm]").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
            if (!confirm(btn.dataset.confirm || "¿Estás seguro?")) {
                e.preventDefault();
            }
        });
    });

    // Tooltips
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
        new bootstrap.Tooltip(el);
    });

    // Dark mode toggle
    var darkToggle = document.getElementById("darkModeToggle");
    if (darkToggle) {
        var saved = localStorage.getItem("theme") || "light";
        document.documentElement.setAttribute("data-bs-theme", saved);
        updateDarkIcon(saved);

        darkToggle.addEventListener("click", function () {
            var current = document.documentElement.getAttribute("data-bs-theme");
            var next = current === "dark" ? "light" : "dark";
            document.documentElement.setAttribute("data-bs-theme", next);
            localStorage.setItem("theme", next);
            updateDarkIcon(next);
        });
    }

    function updateDarkIcon(theme) {
        var icon = darkToggle.querySelector("i");
        if (icon) {
            icon.className = theme === "dark" ? "bi bi-sun fs-5" : "bi bi-moon-stars fs-5";
        }
    }

    // Auto-submit on select change (for filter forms)
    document.querySelectorAll("[data-auto-submit]").forEach(function (el) {
        el.addEventListener("change", function () {
            el.closest("form").submit();
        });
    });
});
