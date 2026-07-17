const imageInput = document.getElementById("image");
const preview = document.getElementById("preview");

imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if (file) {
        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";
    }

});
document.getElementById("uploadForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    document.getElementById("loading").style.display = "block";
document.getElementById("result").textContent = "";

    const fileInput = document.getElementById("image");

    if (fileInput.files.length === 0) {
        alert("Please choose an image");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const uploadResponse = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    const uploadResult = await uploadResponse.json();

    const analyzeResponse = await fetch(
        `/analyze?filename=${encodeURIComponent(uploadResult.filename)}`
    );

    const analyzeResult = await analyzeResponse.json();
    document.getElementById("loading").style.display = "none";

    const cleanResult = analyzeResult.analysis
    .replace(/\*\*/g, "")
    .replace(/^#+\s*/gm, "");

const formattedResult = cleanResult
    .replace(/Species Name:/g, "<b>🐠 Species Name:</b>")
    .replace(/Scientific Name:/g, "<b>🔬 Scientific Name:</b>")
    .replace(/Habitat:/g, "<b>🌊 Habitat:</b>")
    .replace(/Diet:/g, "<b>🍽 Diet:</b>")
    .replace(/Conservation Status:/g, "<b>🛡 Conservation Status:</b>")
    .replace(/Interesting Facts:/g, "<b>⭐ Interesting Facts:</b>")
    .replace(/\n/g, "<br>");

document.getElementById("result").innerHTML = formattedResult;
});