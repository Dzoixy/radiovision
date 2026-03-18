const fileInput = document.getElementById("fileInput");

function triggerUpload() {
  fileInput.click();
}

fileInput.addEventListener("change", async () => {
  const file = fileInput.files[0];
  if (!file) return;

  const purpose = document.getElementById("purpose").value;
  const preset = document.getElementById("preset").value;

  const formData = new FormData();
  formData.append("file", file);
  formData.append("purpose", purpose);
  formData.append("preset", preset);

  try {
    // call FastAPI
    const res = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    // update UI
    document.getElementById("resultImage").src =
      "http://127.0.0.1:8000" + data.image_url;

    document.getElementById("finding").innerText =
      "Finding: " + data.finding;

    document.getElementById("confidence").innerText =
      "Confidence: " + (data.confidence * 100).toFixed(2) + "%";

    document.getElementById("suggestion").innerText =
      "Suggestion: " + data.suggestion;

  } catch (err) {
    alert("Error: " + err);
  }
});