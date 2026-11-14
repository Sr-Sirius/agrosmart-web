(() => {
    const toggle = document.querySelector('.nav-toggle');
    const nav = document.querySelector('.site-nav');

    if (toggle && nav) {
        toggle.addEventListener('click', () => {
            const isOpen = toggle.getAttribute('aria-expanded') === 'true';
            toggle.setAttribute('aria-expanded', String(!isOpen));
            nav.classList.toggle('is-open', !isOpen);
        });
    }

    // Submenús: se abren con clic (útil en pantallas táctiles y en el menú móvil).
    const groups = document.querySelectorAll('.nav-group');
    groups.forEach((group) => {
        const button = group.querySelector('.nav-group-toggle');
        if (!button) return;
        button.addEventListener('click', (event) => {
            event.stopPropagation();
            const willOpen = !group.classList.contains('is-open');
            groups.forEach((other) => {
                other.classList.remove('is-open');
                const otherButton = other.querySelector('.nav-group-toggle');
                if (otherButton) otherButton.setAttribute('aria-expanded', 'false');
            });
            group.classList.toggle('is-open', willOpen);
            button.setAttribute('aria-expanded', String(willOpen));
        });
    });

    document.addEventListener('click', () => {
        groups.forEach((group) => {
            group.classList.remove('is-open');
            const button = group.querySelector('.nav-group-toggle');
            if (button) button.setAttribute('aria-expanded', 'false');
        });
    });

    document.addEventListener('keydown', (event) => {
        if (event.key !== 'Escape') return;
        groups.forEach((group) => group.classList.remove('is-open'));
    });
})();
