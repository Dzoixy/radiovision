console.log("JS LOADED ✅");

let selectedFile = null;

const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");

const resultText = document.getElementById("result-text");
const resultImage = document.getElementById("resultImage");
const outputText = document.getElementById("outputText");

let originalImage = null;
let heatmapImage = null;

// ======================
// CLICK
// ======================
dropZone.onclick = () => fileInput.click();

// ======================
// FILE SELECT
// ======================
fileInput.onchange = (e) => {
    selectedFile = e.target.files[0];
    console.log("FILE SELECTED:", selectedFile);
    previewFile(selectedFile);
};

// ======================
// DRAG & DROP
// ======================
dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.style.borderColor = "#c68e3d";
});

dropZone.addEventListener("dragleave", () => {
    dropZone.style.borderColor = "#262626";
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();

    const files = e.dataTransfer.files;

    if (files.length > 0) {
        selectedFile = files[0];
        console.log("FILE DROPPED:", selectedFile);
        previewFile(selectedFile);
    }

    dropZone.style.borderColor = "#262626";
});

// ======================
// PREVIEW
// ======================
function previewFile(file) {
    if (!file) return;

    const reader = new FileReader();

    reader.onload = () => {
        const textBox = document.getElementById("dropText");
        if (textBox) textBox.style.display = "none";

        let img = document.getElementById("previewImg");

        if (!img) {
            img = document.createElement("img");
            img.id = "previewImg";
            img.style.maxWidth = "100%";
            img.style.maxHeight = "100%";
            img.style.objectFit = "contain";
            img.style.borderRadius = "10px";

            dropZone.appendChild(img);
        }

        img.src = reader.result;
    };

    reader.readAsDataURL(file);
}

// ======================
// ANALYZE
// ======================
async function analyze() {

    console.log("CLICK ANALYZE 🚀");

    if (!selectedFile) {
        alert("กรุณาอัปโหลดภาพก่อน");
        return;
    }

    showLoading();

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("preset", "standard");

    try {
        console.log("FETCHING...");

        const res = await fetch("http://127.0.0.1:9000/analyze", {
            method: "POST",
            body: formData
        });

        console.log("RESPONSE STATUS:", res.status);

        if (!res.ok) {
            const err = await res.text();
            console.error("SERVER ERROR:", err);
            throw new Error("Backend error");
        }

        const data = await res.json();
        console.log("DATA:", data);

        hideLoading();

        // ======================
        // RESULT TEXT
        // ======================
        resultText.innerText = `${data.finding} (${(data.confidence * 100).toFixed(2)}%)`;

        // ======================
        // IMAGE URL
        // ======================
        originalImage = "http://127.0.0.1:9000" + data.original_url;
        heatmapImage = "http://127.0.0.1:9000" + data.heatmap_url;

        console.log("HEATMAP URL:", heatmapImage);

        // ======================
        // SHOW IMAGE (กัน cache + error)
        // ======================
        resultImage.onload = () => {
            console.log("IMAGE LOADED ✅");
        };

        resultImage.onerror = () => {
            console.error("IMAGE LOAD FAIL ❌");
            console.log("FAILED URL:", resultImage.src);
        };

        resultImage.src = heatmapImage + "?t=" + new Date().getTime();
        resultImage.style.display = "block";

        // ซ่อน text
        if (outputText) outputText.style.display = "none";

    } catch (err) {
        hideLoading();
        resultText.innerText = "Error";
        console.error("FULL ERROR:", err);
    }
}

// ======================
// LOADING
// ======================
function showLoading() {
    document.getElementById("loadingOverlay").style.display = "flex";
}

function hideLoading() {
    document.getElementById("loadingOverlay").style.display = "none";
}

// ======================
// HOVER SWITCH
// ======================
resultImage.onmouseenter = () => {
    if (heatmapImage) {
        resultImage.src = heatmapImage + "?t=" + new Date().getTime();
    }
};

resultImage.onmouseleave = () => {
    if (originalImage) {
        resultImage.src = originalImage + "?t=" + new Date().getTime();
    }
};