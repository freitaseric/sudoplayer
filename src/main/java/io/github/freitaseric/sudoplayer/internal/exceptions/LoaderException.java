package io.github.freitaseric.sudoplayer.internal.exceptions;

public class LoaderException extends RuntimeException {
    public LoaderException(String message) { super(message); }

    public LoaderException(String message, Throwable cause) { super(message, cause); }
}
