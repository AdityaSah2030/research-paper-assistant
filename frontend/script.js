// A tab-scoped session survives refreshes but is new in a new browser tab/session.
const SESSION_STORAGE_KEY = "researchai_session_id";
let researchSessionId = sessionStorage.getItem(SESSION_STORAGE_KEY);
if (!researchSessionId) {
    researchSessionId = crypto.randomUUID();
    sessionStorage.setItem(SESSION_STORAGE_KEY, researchSessionId);
}

function sessionHeaders(extra = {}) {
    return { ...extra, "X-Session-ID": researchSessionId };
}

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

            const icon =
                mobileMenuBtn.querySelector(
                    "i"
                );

            if (
                navLinks.classList.contains(
                    "active"
                )
            ) {

                icon.classList.remove(
                    "fa-bars"
                );

                icon.classList.add(
                    "fa-times"
                );

            } else {

                icon.classList.remove(
                    "fa-times"
                );

                icon.classList.add(
                    "fa-bars"
                );
            }
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
    }
);

// =========================
// PDF UPLOAD
// =========================

const uploadBtn =
    document.getElementById("upload-btn");

const uploadStatus =
    document.getElementById("upload-status");

const uploadedPapersList =
    document.getElementById("uploaded-papers-list");

async function refreshUploadedPapers() {
    if (!uploadedPapersList) return;

    try {
        const response = await fetch("/documents", { headers: sessionHeaders() });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Could not load indexed papers.");
        }

        uploadedPapersList.innerHTML = "";

        if (!data.documents || data.documents.length === 0) {
            uploadedPapersList.textContent = "No papers indexed yet.";
            return;
        }

        data.documents.forEach(documentInfo => {
            const row = document.createElement("div");
            row.className = "uploaded-paper-row";

            const name = document.createElement("span");
            name.className = "uploaded-paper-name";
            name.textContent = documentInfo.file_name;

            const count = document.createElement("span");
            count.className = "uploaded-paper-count";
            count.textContent = `${documentInfo.chunks_indexed} chunks`;

            row.append(name, count);
            uploadedPapersList.appendChild(row);
        });
    } catch (error) {
        uploadedPapersList.textContent = "Could not load the indexed paper list.";
    }
}

refreshUploadedPapers();

uploadBtn.addEventListener(
    "click",
    async () => {

        if (
            !pdfInput.files ||
            pdfInput.files.length === 0
        ) {

            uploadStatus.textContent =
                "Please select a PDF first.";

            return;
        }

        const file =
            pdfInput.files[0];

        const formData =
            new FormData();

        formData.append(
            "file",
            file
        );

        try {

            uploadBtn.disabled = true;

            uploadBtn.textContent =
                "Uploading...";

            uploadStatus.innerHTML = `
                Indexing PDF...
            `;

            const response =
                await fetch(
                    "/upload",
                    {
                        method: "POST",
                        headers: sessionHeaders(),
                        body: formData
                    }
                );

            const responseText = await response.text();
            let data;

            try {
                data = JSON.parse(responseText);
            } catch {
                throw new Error(
                    `Upload failed (HTTP ${response.status}). Check server logs.`
                );
            }

            if (!response.ok) {
                throw new Error(data.detail || "Upload failed");
            }

            uploadStatus.textContent =
                `Indexed ${data.file_name} • ${data.chunks_indexed} chunks created`;

            await refreshUploadedPapers();

        } catch (error) {

            uploadStatus.innerHTML = `
                <span style="color:#dc2626;">
                    ${error.message}
                </span>
            `;

        } finally {

            uploadBtn.disabled = false;

            uploadBtn.textContent =
                "Upload PDF";
        }
    }
);

// =========================
// ASK QUESTION
// =========================

const askBtn =
    document.getElementById("ask-btn");

const questionInput =
    document.getElementById("question-input");

const answerOutput =
    document.getElementById("answer-output");

const sourcesOutput =
    document.getElementById("sources-output");

const answerBox =
    document.getElementById(
        "answer-box"
    );

const sourcesBox =
    document.getElementById(
        "sources-box"
    );

const copyBtn =
document.getElementById(
    "copy-answer-btn"
);

function formatAnswer(text) {

    let formatted = text;

    formatted = formatted.replace(
        /Summary:/g,
        "<strong>Summary:</strong>"
    );

    formatted = formatted.replace(
        /Key Findings:/g,
        "<strong>Key Findings:</strong>"
    );

    formatted = formatted.replace(
        /Conclusion:/g,
        "<strong>Conclusion:</strong>"
    );

    formatted = formatted.replace(
        /\n/g,
        "<br>"
    );

    return formatted;
}

askBtn.addEventListener(
    "click",
    async () => {

        const question =
            questionInput.value.trim();

        if (!question) {

            answerOutput.innerHTML =
                "<p>Please enter a question.</p>";

            return;
        }

        try {

            askBtn.disabled = true;

            askBtn.textContent =
                "Thinking...";

            answerBox.innerHTML = `
                <p class="placeholder">
                    Generating answer...
                </p>
            `;

            sourcesBox.innerHTML = `
                Searching sources...
            `;

            const response =
                await fetch(
                    "/ask",
                    {
                        method: "POST",

                        headers: sessionHeaders({
                            "Content-Type": "application/json"
                        }),

                        body: JSON.stringify({
                            question: question
                        })
                    }
                );

            const responseText = await response.text();
            let data;

            try {
                data = JSON.parse(responseText);
            } catch {
                throw new Error(
                    `Question failed (HTTP ${response.status}). Check server logs.`
                );
            }

            if (!response.ok) {
                throw new Error(data.detail || "Request failed");
            }

            answerBox.innerHTML = `
                <div class="answer-content">
                    ${formatAnswer(data.answer)}
                </div>
            `;

            copyBtn.onclick =
                async () => {

                    await navigator.clipboard.writeText(
                        data.answer
                    );

                    copyBtn.textContent =
                        "Copied!";

                    setTimeout(() => {

                        copyBtn.textContent =
                            "Copy";

                    }, 1500);
                };

            sourcesBox.innerHTML = "";

            (data.sources || []).forEach(source => {
                const sourceDiv = document.createElement("div");
                sourceDiv.className = "source-item";

                const pageLabel = source.page_number
                    ? ` • Page ${source.page_number}`
                    : " • Page number unavailable";

                sourceDiv.textContent =
                    `📄 ${source.source || "Unknown document"}${pageLabel} • Chunk ${source.chunk_id ?? "?"}`;

                sourcesBox.appendChild(sourceDiv);
            });

            if (!data.sources || data.sources.length === 0) {
                sourcesBox.textContent = "No supporting passages were retrieved.";
            }

        } catch (error) {

            answerBox.innerHTML = `
                <p class="placeholder">
                    ${error.message}
                </p>
            `;

            sourcesBox.innerHTML = `
                Sources will appear here.
            `;

        } finally {

            askBtn.disabled = false;

            askBtn.textContent =
                "Ask Question";
        }
    }
);