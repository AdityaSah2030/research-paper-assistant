// =========================
// THEME TOGGLE
// =========================

const themeToggle =
    document.getElementById("theme-toggle");

const html =
    document.documentElement;

function updateThemeIcon(theme) {

    const icon =
        themeToggle.querySelector("i");

    if (theme === "dark") {

        icon.classList.remove("fa-moon");
        icon.classList.add("fa-sun");

    } else {

        icon.classList.remove("fa-sun");
        icon.classList.add("fa-moon");
    }
}

const savedTheme =
    localStorage.getItem("theme");

if (savedTheme) {

    html.setAttribute(
        "data-theme",
        savedTheme
    );

    updateThemeIcon(savedTheme);

} else {

    html.setAttribute(
        "data-theme",
        "light"
    );

    updateThemeIcon("light");
}

themeToggle.addEventListener(
    "click",
    () => {

        const currentTheme =
            html.getAttribute("data-theme");

        const newTheme =
            currentTheme === "dark"
                ? "light"
                : "dark";

        html.setAttribute(
            "data-theme",
            newTheme
        );

        localStorage.setItem(
            "theme",
            newTheme
        );

        updateThemeIcon(newTheme);
    }
);

// =========================
// CUSTOM FILE INPUT
// =========================

const pdfInput =
    document.getElementById("pdf-file");

const fileName =
    document.getElementById("file-name");

pdfInput.addEventListener(
    "change",
    () => {

        if (
            pdfInput.files.length > 0
        ) {

            fileName.textContent =
                pdfInput.files[0].name;

        } else {

            fileName.textContent =
                "No file selected";
        }
    }
);

// =========================
// BACK TO TOP
// =========================

const backToTop =
    document.querySelector(
        ".back-to-top"
    );

if (backToTop) {

    backToTop.addEventListener(
        "click",
        () => {

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        }
    );
}

// =========================
// MOBILE MENU
// =========================

const mobileMenuBtn =
    document.querySelector(
        ".mobile-menu-btn"
    );

const navLinks =
    document.querySelector(
        ".nav-links"
    );

if (
    mobileMenuBtn &&
    navLinks
) {

    mobileMenuBtn.addEventListener(
        "click",
        () => {

            navLinks.classList.toggle(
                "active"
            );
        }
    );
}

// =========================
// CLOSE MOBILE MENU
// =========================

document
    .querySelectorAll(".nav-links a")
    .forEach(link => {

        link.addEventListener(
            "click",
            () => {

                navLinks.classList.remove(
                    "active"
                );
            }
        );
    });