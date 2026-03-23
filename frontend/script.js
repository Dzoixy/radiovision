console.log("JS LOADED");
let selectedFile = null;

const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const resultText = document.getElementById("result-text");
const resultImage = document.getElementById("resultImage");
const outputText = document.getElementById("outputText");
const reportBox = document.getElementById("reportBox");

let heatmapImage = null;

//click
if (dropZone) {
    dropZone.onclick = () => fileInput.click();
}

//file input
if (fileInput) {
    fileInput.onchange = (e) => {
        selectedFile = e.target.files[0];
        console.log("FILE SELECTED:", selectedFile);
        previewFile(selectedFile);
    };
}

//dragdrop
if (dropZone) {
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
}

//preview
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

//analyze
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
        const res = await fetch("http://127.0.0.1:9000/analyze", {
            method: "POST",
            body: formData
        });

        console.log("STATUS:", res.status);

        if (!res.ok) {
            const err = await res.text();
            console.error("SERVER ERROR:", err);
            throw new Error("Backend error");
        }

        const data = await res.json();
        console.log("DATA:", data);

        hideLoading();

        //result text
        if (resultText) {
            resultText.innerText = `${data.finding} (${(data.confidence * 100).toFixed(2)}%)`;
        }

        //report
        if (reportBox) {
            reportBox.innerText = data.report || "No report";
        }

        //heatmap
        heatmapImage = "http://127.0.0.1:9000" + data.heatmap_url;

        console.log("HEATMAP:", heatmapImage);

        if (resultImage) {
            resultImage.src = heatmapImage + "?t=" + Date.now();
            resultImage.style.display = "block";
        }

        //hide output text
        if (outputText) {
            outputText.style.display = "none";
        }

    } catch (err) {
        hideLoading();
        console.error("ERROR:", err);

        if (resultText) resultText.innerText = "Error";
        if (reportBox) reportBox.innerText = "Failed to analyze";
    }
}

// loading
function showLoading() {
    const el = document.getElementById("loadingOverlay");
    if (el) el.style.display = "flex";
}

function hideLoading() {
    const el = document.getElementById("loadingOverlay");
    if (el) el.style.display = "none";
}
function openModal(type) {
    const modal = document.getElementById("infoModal");
    const title = document.getElementById("modalTitle");
    const content = document.getElementById("modalContent");

    if (type === "how") {
        title.innerText = "หลักการทำงาน";
        content.innerText =
            "ระบบนี้ใช้ Deep Learning วิเคราะห์ภาพ X-ray โดยโมเดลจะตรวจจับความผิดปกติของปอด และใช้ Grad-CAM เพื่อแสดงตำแหน่งที่มีความเสี่ยง";
    }

    if (type === "guide") {
        title.innerText = "คู่มือการใช้งาน";
        content.innerText =
            "1. อัปโหลดภาพ X-ray\n2. กดปุ่มวิเคราะห์\n3. ระบบจะแสดงผลพร้อม Heatmap และรายงาน";
    }

    if (type === "about") {
        title.innerText = "ผู้จัดทำ";
        content.innerText =
            "พัฒนาโดย GenZBinary\nสาขาวิศวกรรมชีวการแพทย์\nโครงงาน AI วิเคราะห์ภาพทางการแพทย์";
    }

    modal.style.display = "flex";
}

function closeModal() {
    document.getElementById("infoModal").style.display = "none";
}