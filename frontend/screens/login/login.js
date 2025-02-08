document
  .getElementById("loginForm")
  .addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
      const response = await fetch("http://localhost:5000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();
      if (response.ok) {
        localStorage.setItem("access_token", data.access_token);
        document.getElementById("loginMessage").innerText =
          "Login realizado com sucesso!";
        window.location.href = "http://localhost:8080/screens/app/index.html";
      } else {
        document.getElementById(
          "loginMessage"
        ).innerText = `Os dados informados estão incorretos.`;
      }
    } catch (error) {
      console.error("Erro ao realizar login:", error);
      document.getElementById("loginMessage").innerText =
        "Erro ao realizar login.";
    }
  });
