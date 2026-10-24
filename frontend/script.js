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

pdfInput.addEventListener("change", () => {
    if (!pdfInput.files || pdfInput.files.length === 0) {
        fileName.textContent = "No file selected";
    } else if (pdfInput.files.length === 1) {
        fileName.textContent = pdfInput.files[0].name;
    } else {
        fileName.textContent = `${pdfInput.files.length} PDFs selected (${Array.from(pdfInput.files).map(f => f.name).join(", ")})`;
    }
});

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
// PDF UPLOAD & SESSION CATALOG
// =========================

const uploadBtn =
    document.getElementById("upload-btn");

const uploadStatus =
    document.getElementById("upload-status");

const uploadedPapersList =
    document.getElementById("uploaded-papers-list");

const paperCountBadge =
    document.getElementById("paper-count-badge");

async function refreshUploadedPapers() {
    if (!uploadedPapersList) return;

    try {
        const response = await fetch("/documents", { headers: sessionHeaders() });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Could not load indexed papers.");
        }

        const docs = data.documents || [];

        if (paperCountBadge) {
            paperCountBadge.textContent = `${docs.length} ${docs.length === 1 ? 'paper' : 'papers'}`;
        }

        uploadedPapersList.innerHTML = "";

        if (docs.length === 0) {
            uploadedPapersList.innerHTML = '<div class="empty-papers-msg">No papers indexed yet in this session. Upload a PDF to begin.</div>';
            return;
        }

        docs.forEach(documentInfo => {
            const row = document.createElement("div");
            row.className = "uploaded-paper-row";

            const name = document.createElement("span");
            name.className = "uploaded-paper-name";
            name.textContent = `📄 ${documentInfo.file_name}`;

            const count = document.createElement("span");
            count.className = "uploaded-paper-count";
            count.textContent = `${documentInfo.chunks_indexed} chunks`;

            row.append(name, count);
            uploadedPapersList.appendChild(row);
        });
    } catch (error) {
        uploadedPapersList.innerHTML = '<div class="empty-papers-msg">Could not load the indexed paper list.</div>';
    }
}

refreshUploadedPapers();

uploadBtn.addEventListener("click", async () => {
    if (!pdfInput.files || pdfInput.files.length === 0) {
        uploadStatus.innerHTML = '<span style="color:#dc2626;">Please select at least one PDF first.</span>';
        return;
    }

    const files = Array.from(pdfInput.files);
    uploadBtn.disabled = true;

    let successful = 0;
    let failed = [];

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const stepPrefix = files.length > 1 ? `[${i + 1}/${files.length}] ` : "";
        uploadBtn.textContent = files.length > 1 ? `Uploading (${i + 1}/${files.length})...` : "Uploading...";
        uploadStatus.innerHTML = `Indexing <strong>${file.name}</strong> ${stepPrefix}...`;

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("/upload", {
                method: "POST",
                headers: sessionHeaders(),
                body: formData
            });

            const responseText = await response.text();
            let data;
            try {
                data = JSON.parse(responseText);
            } catch {
                throw new Error(`Upload failed (HTTP ${response.status}). Check server logs.`);
            }

            if (!response.ok) {
                throw new Error(data.detail || "Upload failed");
            }

            successful++;
            await refreshUploadedPapers();
        } catch (err) {
            failed.push(`${file.name}: ${err.message}`);
        }
    }

    uploadBtn.disabled = false;
    uploadBtn.textContent = "Upload PDF";
    pdfInput.value = "";
    fileName.textContent = "No file selected";

    if (failed.length === 0) {
        uploadStatus.innerHTML = `<span style="color:var(--accent); font-weight: 500;">✓ Indexed ${successful} ${successful === 1 ? 'paper' : 'papers'} successfully.</span>`;
    } else if (successful > 0) {
        uploadStatus.innerHTML = `<span style="color:#dc2626;">Indexed ${successful} paper(s). Failed: ${failed.join("; ")}</span>`;
    } else {
        uploadStatus.innerHTML = `<span style="color:#dc2626;">${failed.join("; ")}</span>`;
    }

    await refreshUploadedPapers();
});

// =========================
// SESSION RESET
// =========================

const resetSessionBtn = document.getElementById("reset-session-btn");

if (resetSessionBtn) {
    resetSessionBtn.addEventListener("click", async () => {
        const confirmed = confirm(
            "Start a new session? This will clear all uploaded papers and answers for this session."
        );
        if (!confirmed) return;

        try {
            resetSessionBtn.disabled = true;
            await fetch("/session/reset", {
                method: "POST",
                headers: sessionHeaders()
            });
        } catch (e) {
            console.warn("Session reset request failed:", e);
        } finally {
            researchSessionId = crypto.randomUUID();
            sessionStorage.setItem(SESSION_STORAGE_KEY, researchSessionId);

            pdfInput.value = "";
            fileName.textContent = "No file selected";
            uploadStatus.textContent = "New session started with empty workspace.";

            const questionInput = document.getElementById("question-input");
            if (questionInput) questionInput.value = "";

            const answerBox = document.getElementById("answer-box");
            if (answerBox) {
                answerBox.innerHTML = '<p class="placeholder">Your answer will appear here.</p>';
            }

            const sourcesBox = document.getElementById("sources-box");
            if (sourcesBox) {
                sourcesBox.innerHTML = 'Sources will appear here.';
            }

            await refreshUploadedPapers();
            resetSessionBtn.disabled = false;
        }
    });
}

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