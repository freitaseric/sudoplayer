package io.github.freitaseric.sudoplayer.internal.managers;

import discord4j.core.GatewayDiscordClient;
import discord4j.core.event.domain.Event;
import io.github.freitaseric.sudoplayer.SudoPlayerBot;
import io.github.freitaseric.sudoplayer.internal.interfaces.IListener;
import io.github.freitaseric.sudoplayer.utils.ClassLoader;

import java.util.HashMap;

public class ListenerManager {
    private static HashMap<Class<Event>, IListener<Event>> events;

    private final GatewayDiscordClient gatewayDiscordClient;

    public ListenerManager(GatewayDiscordClient gatewayDiscordClient) {
        this.gatewayDiscordClient = gatewayDiscordClient;
    }

    public void registerEventListeners() {
        for (IListener<Event> event : events.values()) {
            gatewayDiscordClient.on(event.getEventClass(), event::execute).subscribe();
        }
    }

    public void loadEvents() {
        events = ClassLoader.loadClasses("io.github.freitaseric.sudoplayer.app.listeners", "getEventClass", IListener.class);
        SudoPlayerBot.logger.info("Loaded {} events", events.size());
    }
}
