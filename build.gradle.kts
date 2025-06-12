plugins {
    id("java")
    alias(libs.plugins.shadow)
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