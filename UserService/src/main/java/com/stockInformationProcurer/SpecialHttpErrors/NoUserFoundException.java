package com.stockInformationProcurer.SpecialHttpErrors;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.NO_CONTENT)
public class NoUserFoundException extends RuntimeException {
    public NoUserFoundException() {
        super("User nicht vorhanden");
    }
}