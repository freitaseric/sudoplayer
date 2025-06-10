package io.github.freitaseric.sudoplayer.interfaces;

import discord4j.core.event.domain.Event;
import reactor.core.publisher.Mono;

public interface IEvent <T extends Event>{
    Class<T> eventClass();
    Mono<Void> execute(T event);
}
