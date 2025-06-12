package io.github.freitaseric.sudoplayer.services

import io.github.freitaseric.sudoplayer.constants.ApiLinks
import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.request.*
import io.ktor.serialization.kotlinx.json.*
import io.ktor.utils.io.*

object SteamService {
    private val httpClient: HttpClient = HttpClient(CIO) {
        install(ContentNegotiation) {
            json()
        }
    }

    @OptIn(InternalAPI::class)
    suspend fun getAppList(): String {
        val response = httpClient.get(ApiLinks.GET_STEAM_APPS)
        return response.rawContent.toString()
    }
}