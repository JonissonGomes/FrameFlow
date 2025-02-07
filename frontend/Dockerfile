# Usa a imagem do Nginx como base para servir o frontend
FROM nginx:alpine

# Define o diretório de trabalho dentro do container
WORKDIR /usr/share/nginx/html

# Remove os arquivos padrão do Nginx
RUN rm -rf ./*

# Copia os arquivos do frontend para o container
COPY . .

# Expõe a porta 80 para acesso ao frontend
EXPOSE 80

# Comando para manter o Nginx rodando
CMD ["nginx", "-g", "daemon off;"]
