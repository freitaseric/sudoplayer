package io.github.freitaseric.sudoplayer.app.commands;

import discord4j.core.event.domain.interaction.ChatInputInteractionEvent;
import discord4j.discordjson.json.ApplicationCommandRequest;
import io.github.freitaseric.sudoplayer.internal.interfaces.ICommand;
import reactor.core.publisher.Mono;

public class PingCommand implements ICommand<ChatInputInteractionEvent> {
    @Override
    public ApplicationCommandRequest getRequest() {
        return ApplicationCommandRequest.builder().name("ping").description("Responde com pong").build();
    }

    @Override
    public Mono<Void> execute(ChatInputInteractionEvent event) {
        return event.reply("Pong!").withEphemeral(true);
    }
}
