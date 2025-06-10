package io.github.freitaseric.sudoplayer.managers;

import discord4j.core.event.domain.interaction.ApplicationCommandInteractionEvent;
import discord4j.core.event.domain.interaction.ChatInputAutoCompleteEvent;
import discord4j.rest.RestClient;
import io.github.classgraph.ClassGraph;
import io.github.classgraph.ClassInfo;
import io.github.classgraph.ClassInfoList;
import io.github.classgraph.ScanResult;
import io.github.freitaseric.sudoplayer.interfaces.ICommand;
import reactor.core.publisher.Mono;

import java.util.HashMap;

public class CommandManager {
    private static final HashMap<String, ICommand<ApplicationCommandInteractionEvent>> commands = new HashMap<>();

    private final RestClient restClient;
    private final Long applicationId;

    public CommandManager(RestClient restClient, Long applicationId) {
        this.restClient = restClient;
        this.applicationId = applicationId;
    }

    public void registerCommands() {
        restClient.getApplicationService().bulkOverwriteGlobalApplicationCommand(applicationId, commands.values().stream().map(ICommand::getRequest).toList()).subscribe();
    }

    @SuppressWarnings("unchecked")
    public void loadCommands() {
        try (ScanResult scanResult = new ClassGraph().enableAllInfo().acceptPackages("io.github.freitaseric.sudoplayer.commands").scan()) {
            ClassInfoList commandClasses = scanResult.getClassesImplementing(ICommand.class);

            for (ClassInfo classInfo : commandClasses) {
                try {
                    ICommand<ApplicationCommandInteractionEvent> instance = (ICommand<ApplicationCommandInteractionEvent>) classInfo.loadClass().getDeclaredConstructor().newInstance();

                    commands.put(instance.getRequest().name(), instance);
                } catch (Exception e) {
                    System.err.println("Falha ao carregar o comando da classe: " + classInfo.getName());
                }
            }
        } catch (Exception e) {
            System.err.println("Falha ao escanear o classpath em busca de comandos.");
        }
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
