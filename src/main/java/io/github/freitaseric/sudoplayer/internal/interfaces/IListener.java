package io.github.freitaseric.sudoplayer.internal.interfaces;

import discord4j.core.event.domain.Event;
import reactor.core.publisher.Mono;

public interface IListener<T extends Event>{
    Class<T> getEventClass();
    Mono<Void> execute(T event);
}
