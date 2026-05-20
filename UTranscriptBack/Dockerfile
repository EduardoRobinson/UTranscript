FROM eclipse-temurin:17-jdk-jammy

WORKDIR /app

# Copia arquivos de dependência primeiro (cache do docker)
COPY gradlew .
COPY gradle gradle
COPY build.gradle .
COPY settings.gradle .

RUN chmod +x gradlew

# Baixa dependências
RUN ./gradlew dependencies --no-daemon

# Agora copia o resto do projeto
COPY . .

# Build do projeto
RUN ./gradlew build -x test --no-daemon

EXPOSE 8080

CMD ["java","-jar","build/libs/UTranscriptBack-0.0.1-SNAPSHOT.jar"]