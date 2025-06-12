package io.github.freitaseric.sudoplayer.app.commands;

import discord4j.core.event.domain.interaction.ChatInputAutoCompleteEvent;
import discord4j.core.event.domain.interaction.ChatInputInteractionEvent;
import discord4j.core.object.command.ApplicationCommandInteractionOption;
import discord4j.core.object.command.ApplicationCommandInteractionOptionValue;
import discord4j.core.object.command.ApplicationCommandOption;
import discord4j.discordjson.json.ApplicationCommandOptionData;
import discord4j.discordjson.json.ApplicationCommandRequest;
import io.github.freitaseric.sudoplayer.internal.interfaces.ICommand;
import io.github.freitaseric.sudoplayer.services.SteamService;
import reactor.core.publisher.Mono;

import java.util.Optional;

public class GameCommand implements ICommand<ChatInputInteractionEvent> {
    @Override
    public ApplicationCommandRequest getRequest() {
        return ApplicationCommandRequest.builder()
                .name("jogo")
                .description("Veja informações sobre um jogo da Steam.")
                .options(ApplicationCommandOptionData.builder()
                                .name("nome")
                                .description("Informe o nome do jogo que deseja pesquisar.")
                                .autocomplete(true)
                                .type(ApplicationCommandOption.Type.STRING.getValue())
                                .build(),
                        ApplicationCommandOptionData.builder()
                                .name("appid")
                                .description("Informe o id do aplicativo na Steam.")
                                .type(ApplicationCommandOption.Type.INTEGER.getValue())
                                .build()
                ).build();
    }

    @Override
    public Mono<Void> execute(ChatInputInteractionEvent event) {
        return null;
    }

    @Override
    public Mono<Void> autoComplete(ChatInputAutoCompleteEvent event) {
        Optional<String> name = event.getOption("name")
                .flatMap(ApplicationCommandInteractionOption::getValue)
                .map(ApplicationCommandInteractionOptionValue::asString);
        Optional<Long> appId = event.getOption("appid")
                .flatMap(ApplicationCommandInteractionOption::getValue)
                .map(ApplicationCommandInteractionOptionValue::asLong);

        return Mono.empty();
    }
}
