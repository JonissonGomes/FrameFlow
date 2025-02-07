# FrameFlow - Extração de Quadros de Vídeos

O **FrameFlow** é um aplicativo que permite a extração de quadros de vídeos em intervalos regulares e os compacta em um arquivo ZIP. Ideal para análise de vídeos, geração de thumbnails ou qualquer cenário que precise processar e extrair conteúdo visual de arquivos de vídeo.

## Funcionalidades
- **Extração de Quadros**: Extrai quadros de um vídeo em intervalos de 20 segundos.
- **Salvamento de Quadros**: Cada quadro extraído é salvo como um arquivo JPEG.
- **Compactação de Quadros**: Todos os quadros extraídos são compactados em um único arquivo ZIP para fácil manuseio e transferência.
- Interface Web: Interface simples para o upload de vídeos e interação com o backend.


## Arquitetura
- **Frontend**: Interface simples para o upload de vídeos.
- **Backend**: Flask API que lida com a extração dos quadros e a compactação em um arquivo ZIP.
- **Docker**: A aplicação é empacotada e executada usando Docker para facilitar o setup e a execução do ambiente de desenvolvimento e produção.
Estrutura de Pastas

```bash
.
├── backend
│   ├── app
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── video_processing.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── run.py
├── frontend
│   ├── app.js
│   ├── Dockerfile
│   ├── indext.html
│   └── style.css
├── docker-compose.yml
└── README.md

```
## Pré-requisitos
Antes de executar o projeto, você deve ter o Docker instalado na sua máquina. Caso ainda não tenha o Docker, você pode instalá-lo seguindo as instruções da documentação oficial.

### Rodando o Projeto com Docker
Clone o repositório pertencente ao projeto:

```bash
git clone https://github.com/JonissonGomes/FrameFlow
cd FrameFlow
```

## Construa os containers do Docker:

```bash
docker-compose build
```

## Inicie os containers:

```bash
docker-compose up
```

> A aplicação iniciará o backend e o front end da aplicação.
> O backend estará disponível em: http://localhost:5000
> O frontend estará disponível em http://localhost:8080

## Como Usar a Interface Web
Você pode acessar a interface web utilizando a seguinte URL http://localhost:8080.

1. Escolha o arquivo de vídeo em seu computador.
2. Clique em enviar vídeo e aguarde o vídeo processado.

*Os frames serão extraidos em intervalos de 20 segundos e após a extração, os quadros serão compactados em um arquivo ZIP, que você poderá baixa-los.*

# Arquitetura Backend
O Flask é utilizado para criar uma API REST que gerencia a lógica de extração e compactação dos quadros.

Docker é usado para containerizar tanto o frontend quanto o backend, garantindo que todos os requisitos estejam isolados e a aplicação seja fácil de rodar em qualquer ambiente.

## Como Funciona
Upload de Vídeo: O frontend permite que o usuário envie um vídeo.
Processamento de Vídeo: O backend usa a biblioteca opencv-python para abrir o vídeo e extrair quadros a cada 20 segundos.
Compactação: Os quadros são salvos como arquivos JPEG e compactados em um arquivo ZIP.
Download do ZIP: O arquivo ZIP contendo os quadros extraídos é disponibilizado para o usuário baixar.

## Como Modificar o Código
O código do backend está localizado na pasta backend/app/.
O código do frontend (interface simples) está na pasta frontend/.
Se precisar ajustar o intervalo de extração ou outro comportamento, altere o código no arquivo backend/app/video_processing.py.

## Tecnologias Utilizadas
**Flask**: Para criar a API backend.
**OpenCV**: Para processar os vídeos e extrair os quadros.
**Docker**: Para containerizar a aplicação.
**HTML/CSS/JavaScript**: Para a interface web.

## Contribuindo
Se você deseja contribuir com este projeto, siga os seguintes passos:

1. Realize o fork do repositório.

2. Crie uma branch com a sua feature (git checkout -b feature/nome-da-feature).

3. Faça commit das suas alterações (git commit -m 'Adicionando nova feature').

4. Push na sua branch (git push origin feature/nome-da-feature).

5. Abra um Pull Request.

---
>Licença
>Este projeto está licenciado sob a MIT License.