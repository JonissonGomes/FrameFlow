document.getElementById("registerForm").addEventListener("submit", async (event) => {
    event.preventDefault();
  
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
  
    try {
      const response = await fetch("http://localhost:5000/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, email, password })
      });
  
      const data = await response.json();
      if (response.ok) {
        document.getElementById("registerMessage").innerText = "Registro realizado com sucesso!";
        setTimeout(() => {
          window.location.href = "http://localhost:8080/screens/login/login.html";
        }, 3000)
      } else {
        document.getElementById("registerMessage").innerText = `Erro: ${data.error}`;
      }
    } catch (error) {
      console.error("Erro ao registrar:", error);
      document.getElementById("registerMessage").innerText = "Erro ao registrar.";
    }
  });
  