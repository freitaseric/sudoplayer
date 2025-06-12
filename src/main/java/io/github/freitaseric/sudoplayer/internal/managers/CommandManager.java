package io.github.freitaseric.sudoplayer.internal.managers;

import discord4j.core.event.domain.interaction.ApplicationCommandInteractionEvent;
import discord4j.core.event.domain.interaction.ChatInputAutoCompleteEvent;
import discord4j.rest.RestClient;
import io.github.freitaseric.sudoplayer.SudoPlayerBot;
import io.github.freitaseric.sudoplayer.internal.interfaces.ICommand;
import io.github.freitaseric.sudoplayer.utils.ClassLoader;
import reactor.core.publisher.Mono;

import java.util.HashMap;

public class CommandManager {
    private static HashMap<String, ICommand<ApplicationCommandInteractionEvent>> commands;

    private final RestClient restClient;
    private final Long applicationId;

    public CommandManager(RestClient restClient, Long applicationId) {
        this.restClient = restClient;
        this.applicationId = applicationId;
    }

    public void registerCommands() {
        restClient.getApplicationService().bulkOverwriteGlobalApplicationCommand(applicationId, commands.values().stream().map(ICommand::getRequest).toList()).subscribe();
    }

    public void loadCommands() {
        commands = ClassLoader.loadClasses("io.github.freitaseric.sudoplayer.app.commands", "getName", ICommand.class);
        SudoPlayerBot.logger.info("Loaded {} commands", commands.size());
    }

    public Mono<Void> handleCommand(ApplicationCommandInteractionEvent event) {
        ICommand<ApplicationCommandInteractionEvent> command = commands.get(event.getCommandName());

        return command.execute(event);
    }

    public Mono<Void> handleAutocomplete(ChatInputAutoCompleteEvent event) {
        ICommand<ApplicationCommandInteractionEvent> command = commands.get(event.getCommandName());

        return command.autoComplete(event);
    }
}
