package io.github.freitaseric.sudoplayer.internal.interfaces;

import discord4j.core.event.domain.interaction.ApplicationCommandInteractionEvent;
import discord4j.core.event.domain.interaction.ChatInputAutoCompleteEvent;
import discord4j.discordjson.json.ApplicationCommandRequest;
import reactor.core.publisher.Mono;

public interface ICommand<T extends ApplicationCommandInteractionEvent> {
    ApplicationCommandRequest getRequest();

    default String getName() {
        return getRequest().name();
    }

    Mono<Void> execute(T event);

    default Mono<Void> autoComplete(ChatInputAutoCompleteEvent event) {
        return Mono.empty();
    }
}
