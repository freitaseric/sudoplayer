package io.github.freitaseric.sudoplayer.internal.managers;

import discord4j.core.GatewayDiscordClient;
import discord4j.core.object.presence.ClientActivity;
import discord4j.core.object.presence.ClientPresence;
import reactor.core.publisher.Flux;

import java.time.Duration;
import java.util.List;
import java.util.Random;

public class PresenceManager {
    private static final Random RANDOM = new Random();
    private static final List<ClientActivity> activities = List.of(ClientActivity.watching("ProtonDB"), ClientActivity.listening("SteamDB"), ClientActivity.playing("Borderlands 3"), ClientActivity.competing("to be a pro player"), ClientActivity.playing("Hollow Knight"));

    private final GatewayDiscordClient gatewayDiscordClient;

    public PresenceManager(GatewayDiscordClient gatewayDiscordClient) {
        this.gatewayDiscordClient = gatewayDiscordClient;
    }

    public void startLoop() {
        Flux.interval(Duration.ofMinutes(5L)).flatMap(tick -> {
            int randomIndex = RANDOM.nextInt(activities.size());
            ClientActivity newActivity = activities.get(randomIndex);

            return gatewayDiscordClient.updatePresence(ClientPresence.online(newActivity));
        }).subscribe();
    }
}
