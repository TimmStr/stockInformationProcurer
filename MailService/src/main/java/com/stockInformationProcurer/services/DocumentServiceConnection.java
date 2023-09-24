package com.stockInformationProcurer.services;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

public class DocumentServiceConnection {
    public byte[] createAndReturnPdf(String ticker) {

        RestTemplate restTemplate = new RestTemplate();
        String mail = "admin@admin.com";
        String password = "admin";
        final String serviceUrl = "http://stockinformationprocurer-document-service-1:9010/createPdf?ticker=" + ticker +"&mail="+mail+"&password="+password;

        // Erstellen Sie HTTP-Header mit JSON-Content-Type
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        try {
            ResponseEntity<byte[]> response = restTemplate.getForEntity(serviceUrl, byte[].class);

            if (response.getStatusCode() == HttpStatus.OK) {
                byte[] pdf = response.getBody();
                System.out.println("Response: " + pdf);
                return pdf;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }
}
