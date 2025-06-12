package io.github.freitaseric.sudoplayer;

import discord4j.core.DiscordClient;
import discord4j.core.GatewayDiscordClient;
import discord4j.core.event.domain.interaction.*;
import discord4j.rest.RestClient;
import io.github.freitaseric.sudoplayer.internal.managers.CommandManager;
import io.github.freitaseric.sudoplayer.internal.managers.ListenerManager;
import io.github.freitaseric.sudoplayer.internal.managers.PresenceManager;
import io.github.freitaseric.sudoplayer.internal.managers.ResponderManager;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SudoPlayerBot {
    private static final String token = System.getenv("BOT_TOKEN");
    public static final Logger logger = LoggerFactory.getLogger(SudoPlayerBot.class);

    public static void main(String[] args) {
        DiscordClient client = DiscordClient.create(token);

        GatewayDiscordClient gatewayDiscordClient = client.gateway().login().block();

        assert gatewayDiscordClient != null;
        RestClient restClient = gatewayDiscordClient.getRestClient();

        PresenceManager presenceManager = new PresenceManager(gatewayDiscordClient);
        presenceManager.startLoop();

        CommandManager commandManager = new CommandManager(restClient, restClient.getApplicationId().block());
        commandManager.loadCommands();
        commandManager.registerCommands();

        ListenerManager listenerManager = new ListenerManager(gatewayDiscordClient);
        listenerManager.loadEvents();

        ResponderManager responderManager = new ResponderManager();
        responderManager.loadResponders();

        gatewayDiscordClient.on(ApplicationCommandInteractionEvent.class, commandManager::handleCommand).subscribe();

        gatewayDiscordClient.on(ChatInputAutoCompleteEvent.class, commandManager::handleAutocomplete).subscribe();

        gatewayDiscordClient.on(ButtonInteractionEvent.class, responderManager::handleButtonResponder).subscribe();
        gatewayDiscordClient.on(SelectMenuInteractionEvent.class, responderManager::handleSelectMenuResponder).subscribe();
        gatewayDiscordClient.on(ModalSubmitInteractionEvent.class, responderManager::handleModalResponder).subscribe();

        listenerManager.registerEventListeners();

        gatewayDiscordClient.onDisconnect().block();
    }
}