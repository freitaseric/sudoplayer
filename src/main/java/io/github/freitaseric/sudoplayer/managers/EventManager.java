package io.github.freitaseric.sudoplayer.managers;

import discord4j.core.GatewayDiscordClient;
import discord4j.core.event.domain.Event;
import io.github.classgraph.ClassGraph;
import io.github.classgraph.ClassInfo;
import io.github.classgraph.ClassInfoList;
import io.github.classgraph.ScanResult;
import io.github.freitaseric.sudoplayer.interfaces.IEvent;

import java.util.HashMap;

public class EventManager {
    private static final HashMap<Class<Event>, IEvent<Event>> events = new HashMap<>();

    private final GatewayDiscordClient gatewayDiscordClient;

    public EventManager(GatewayDiscordClient gatewayDiscordClient) {
        this.gatewayDiscordClient = gatewayDiscordClient;
    }

    public void registerEvents() {
        for (IEvent<Event> event : events.values()) {
            gatewayDiscordClient.on(event.eventClass(), event::execute).subscribe();
        }
    }

    @SuppressWarnings("unchecked")
    public void loadCommands() {
        try (ScanResult scanResult = new ClassGraph().enableAllInfo().acceptPackages("io.github.freitaseric.sudoplayer.events").scan()) {
            ClassInfoList eventClasses = scanResult.getClassesImplementing(IEvent.class);

            for (ClassInfo classInfo : eventClasses) {
                try {
                    IEvent<Event> instance = (IEvent<Event>) classInfo.loadClass().getDeclaredConstructor().newInstance();

                    events.put(instance.eventClass(), instance);
                } catch (Exception e) {
                    System.err.println("Falha ao carregar o comando da classe: " + classInfo.getName());
                }
            }
        } catch (Exception e) {
            System.err.println("Falha ao escanear o classpath em busca de comandos.");
        }
    }
}
