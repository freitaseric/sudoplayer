plugins {
    id("java")
}

group = "io.github.freitaseric.sudoplayer"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    implementation(libs.discord4j.core)
    implementation(libs.logback.classic)
    implementation(libs.classgraph)
}