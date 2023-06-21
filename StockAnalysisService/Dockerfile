FROM maven:3-eclipse-temurin-17-alpine as mvn-build
WORKDIR /app/build
COPY src src
COPY .mvn .mvn
COPY mvnw .
COPY mvnw.cmd .
COPY pom.xml .
# RUN ./mvnw -f pom.xml clean package -DskipTests
RUN mvn -f pom.xml clean package

FROM openjdk:17-alpine
WORKDIR /app
COPY --from=mvn-build /app/build/target/*.jar ./StockAnalysisService.jar
#ENV CONTAINER_NAME=hms-ca-service \
#    PORT=8082 \
#    OPTS_ARGS=''

# CMD ["java", "-jar", "/app/tls-hms-api.jar"]
ENTRYPOINT ["java", "-jar", "/app/StockAnalysisService.jar", "${OPTS_ARGS}"]
