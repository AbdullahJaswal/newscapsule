# syntax=docker/dockerfile:1
FROM gradle:8.9-jdk22-alpine AS build

WORKDIR /backend

COPY gradlew .
COPY gradle gradle
COPY build.gradle.kts .
COPY settings.gradle.kts .
COPY src src

RUN chmod +x gradlew
RUN ./gradlew build

FROM openjdk:22-jdk-slim-buster

WORKDIR /backend

COPY --from=build /backend/build/libs/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
