package io.github.freitaseric.sudoplayer.internal.interfaces;

import discord4j.core.event.domain.interaction.ComponentInteractionEvent;
import reactor.core.publisher.Mono;

public interface IResponder<T extends ComponentInteractionEvent> {
    String getCustomId();

    Mono<Void> execute(T event);
}
