document
  .getElementById("uploadForm")
  .addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById("fileInput");
    const interval = document.getElementById("intervalInput").value;
    const frameCount = document.getElementById("frameCountInput").value;

    if (!fileInput.files.length) {
      alert("Por favor, selecione um arquivo de vídeo.");
      return;
    }

    formData.append("file", fileInput.files[0]);
    formData.append("interval", interval);
    formData.append("frame_count", frameCount);

    document.getElementById("message").innerText = "Enviando vídeo...";

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
        mode: "cors",
      });

      if (!response.ok) {
        const errorData = await response.json();
        document.getElementById(
          "message"
        ).innerText = `Erro: ${errorData.error}`;
        return;
      }

      const data = await response.json();

      if (data.zip_url) {
        document.getElementById("message").innerText =
          "Processamento concluído!";

        const downloadLink = document.getElementById("downloadLink");

        downloadLink.classList.remove("hidden");

        downloadLink.href = `http://localhost:5000${data.zip_url}`;
      } else {
        document.getElementById("message").innerText =
          "Erro: URL do arquivo ZIP não encontrada.";
      }
    } catch (error) {
      console.error("Erro ao enviar o vídeo:", error);
      document.getElementById("message").innerText = "Erro ao enviar o vídeo.";
    }
  });

document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("fileInput");
  const submitButton = document.querySelector("button[type='submit']");
  const videoPreview = document.getElementById("videoPreview");

  submitButton.style.display = "none";

  const downloadLink = document.getElementById("downloadLink");
  if (downloadLink) {
    downloadLink.classList.add("hidden");
  }

  fileInput.addEventListener("change", function () {
    if (fileInput.files.length > 0) {
      submitButton.style.display = "block";

      const videoFile = fileInput.files[0];
      const videoURL = URL.createObjectURL(videoFile);
      videoPreview.src = videoURL;
      videoPreview.classList.remove("hidden");
    } else {
      submitButton.style.display = "none";

      videoPreview.classList.add("hidden");
    }
  });
});
