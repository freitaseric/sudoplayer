package io.github.freitaseric.sudoplayer;

import discord4j.core.DiscordClient;
import discord4j.core.GatewayDiscordClient;
import discord4j.core.event.domain.interaction.ApplicationCommandInteractionEvent;
import discord4j.core.event.domain.interaction.ChatInputAutoCompleteEvent;
import discord4j.core.event.domain.lifecycle.ReadyEvent;
import discord4j.rest.RestClient;
import io.github.freitaseric.sudoplayer.managers.CommandManager;
import io.github.freitaseric.sudoplayer.managers.EventManager;
import io.github.freitaseric.sudoplayer.managers.PresenceManager;
import reactor.core.publisher.Mono;

public class SudoPlayerBot {
    private static final String token = System.getenv("BOT_TOKEN");

    public static void main(String[] args) {
        DiscordClient client = DiscordClient.create(token);

        GatewayDiscordClient gatewayDiscordClient = client.gateway().login().block();

        assert gatewayDiscordClient != null;
        RestClient restClient = gatewayDiscordClient.getRestClient();

        PresenceManager presenceManager = new PresenceManager(gatewayDiscordClient);
        presenceManager.startLoop();

        CommandManager commandManager = new CommandManager(restClient, restClient.getApplicationId().block());
        commandManager.loadCommands();

        EventManager eventManager = new EventManager(gatewayDiscordClient);
        eventManager.loadCommands();

        gatewayDiscordClient.on(ReadyEvent.class, event -> {
            System.out.println("Client online!");

            commandManager.registerCommands();
            return Mono.empty();
        }).subscribe();

        gatewayDiscordClient.on(ApplicationCommandInteractionEvent.class, commandManager::handleCommand).subscribe();

        gatewayDiscordClient.on(ChatInputAutoCompleteEvent.class, commandManager::handleAutocomplete).subscribe();

        eventManager.registerEvents();

        gatewayDiscordClient.onDisconnect().block();
    }
}