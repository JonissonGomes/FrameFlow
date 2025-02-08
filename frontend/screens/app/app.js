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

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
        mode: "cors",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        document.getElementById(
          "message"
        ).innerText = `Erro: ${errorData.error}`;
        return;
      }

      const data = await response.json();

      if (data.video_id) {
        window.currentVideoId = data.video_id;

        const statusContainer = document.getElementById("statusContainer");
        statusContainer.classList.remove("hidden");

        startStatusPolling();
      } else {
        document.getElementById("message").innerText =
          "Erro: video_id não retornado.";
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

  document.getElementById("refreshStatus").addEventListener("click", () => {
    fetchVideoStatus();
  });
});

async function fetchVideoStatus() {
  if (!window.currentVideoId) return;

  try {
    const response = await fetch(
      `http://localhost:5000/video_status/${window.currentVideoId}`,
      {
        method: "GET",
        mode: "cors",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      console.log("Erro retornado:", errorData);
      document.getElementById("status").innerText = `Erro: ${
        errorData.error || "Token inválido ou expirado"
      }`;
      return;
    }

    const videoStatus = await response.json();
    document.getElementById(
      "status"
    ).innerText = `${videoStatus.status}`;

    if (videoStatus.status === "Concluído") {
      clearInterval(window.statusPollingInterval);
      const downloadLink = document.getElementById("downloadLink");
      downloadLink.classList.remove("hidden");
      downloadLink.href = `http://localhost:5000${videoStatus.zip_url}`;
    }
  } catch (error) {
    console.error("Erro ao buscar status:", error);
    document.getElementById("status").innerText = "Erro ao buscar status.";
  }
}

function startStatusPolling() {
  fetchVideoStatus();
  window.statusPollingInterval = setInterval(fetchVideoStatus, 5000);
}
