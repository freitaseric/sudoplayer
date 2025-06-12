package io.github.freitaseric.sudoplayer.internal.managers;

import discord4j.core.event.domain.interaction.ButtonInteractionEvent;
import discord4j.core.event.domain.interaction.ModalSubmitInteractionEvent;
import discord4j.core.event.domain.interaction.SelectMenuInteractionEvent;
import io.github.freitaseric.sudoplayer.SudoPlayerBot;
import io.github.freitaseric.sudoplayer.internal.interfaces.IResponder;
import io.github.freitaseric.sudoplayer.utils.ClassLoader;
import reactor.core.publisher.Mono;

import java.util.HashMap;

public class ResponderManager {
    private static HashMap<String, IResponder<ButtonInteractionEvent>> buttonResponders;

    private static HashMap<String, IResponder<SelectMenuInteractionEvent>> selectMenuResponders;

    private static HashMap<String, IResponder<ModalSubmitInteractionEvent>> modalResponders;

    public Mono<Void> handleButtonResponder(ButtonInteractionEvent event) {
        IResponder<ButtonInteractionEvent> responder = buttonResponders.get(event.getCustomId());
        return responder.execute(event);
    }

    public Mono<Void> handleSelectMenuResponder(SelectMenuInteractionEvent event) {
        IResponder<SelectMenuInteractionEvent> responder = selectMenuResponders.get(event.getCustomId());
        return responder.execute(event);
    }

    public Mono<Void> handleModalResponder(ModalSubmitInteractionEvent event) {
        IResponder<ModalSubmitInteractionEvent> responder = modalResponders.get(event.getCustomId());
        return responder.execute(event);
    }

    public void loadResponders() {
        buttonResponders = ClassLoader.loadClasses("io.github.freitaseric.sudoplayer.app.responders.buttons", "getCustomId", IResponder.class);
        SudoPlayerBot.logger.info("Loaded {} button responders", buttonResponders.size());
        selectMenuResponders = ClassLoader.loadClasses("io.github.freitaseric.sudoplayer.app.responders.selects", "getCustomId", IResponder.class);
        SudoPlayerBot.logger.info("Loaded {} select menu responders", selectMenuResponders.size());
        modalResponders = ClassLoader.loadClasses("io.github.freitaseric.sudoplayer.app.responders.modals", "getCustomId", IResponder.class);
        SudoPlayerBot.logger.info("Loaded {} modal responders", modalResponders.size());
    }
}
