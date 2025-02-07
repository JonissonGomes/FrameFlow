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
      });

      const data = await response.json();
      if (response.ok) {
        document.getElementById("message").innerText =
          "Processamento concluído!";
        document.getElementById(
          "downloadLink"
        ).innerHTML = `<a href="${data.zip_url}" download>Baixar Frames ZIP</a>`;
      } else {
        document.getElementById("message").innerText = `Erro: ${data.error}`;
      }
    } catch (error) {
      document.getElementById("message").innerText = "Erro ao enviar o vídeo.";
    }
  });

  document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("fileInput");
  const submitButton = document.querySelector("button[type='submit']");

  // Esconde o botão de envio inicialmente
  submitButton.style.display = "none";

  fileInput.addEventListener("change", function () {
    if (fileInput.files.length > 0) {
      submitButton.style.display = "block"; // Mostra o botão se um arquivo for carregado
    } else {
      submitButton.style.display = "none"; // Oculta o botão se nenhum arquivo estiver selecionado
    }
  });
});

