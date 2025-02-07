from app import create_app

# Criação do app Flask
app = create_app()

if __name__ == "__main__":
    # Rodando o servidor Flask
    app.run(host="0.0.0.0", port=5000, debug=True)
