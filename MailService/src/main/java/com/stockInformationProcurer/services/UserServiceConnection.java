package com.stockInformationProcurer.services;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.stockInformationProcurer.controller.MailService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Service
public class UserServiceConnection {
    private final MailService mailService;

    @Autowired
    public UserServiceConnection(MailService mailService) {
        this.mailService = mailService;
    }

    public ResponseEntity getAllStocksForAllUsersFromUserService() {
        RestTemplate restTemplate = new RestTemplate();
        final String serviceUrl = "http://stockinformationprocurer-user-service-1:9050/getAllUserStocks";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        try {
            System.out.println(restTemplate.getForEntity(serviceUrl, String.class));
            ResponseEntity<String> response = restTemplate.getForEntity(serviceUrl, String.class);

            if (response.getStatusCode() == HttpStatus.OK) {
                String jsonResponse = response.getBody();
                System.out.println("Response: " + jsonResponse);
                return ResponseEntity.ok(jsonResponse);
            } else {
                return ResponseEntity.status(response.getStatusCode()).build();
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }


    public ResponseEntity getAllStocksForUserFromUserService(String mail, String password) {
        System.out.println(mail + " " + password);

        RestTemplate restTemplate = new RestTemplate();

        final String serviceUrl = "http://stockinformationprocurer-user-service-1:9050/getStocksForUser?mail=" + mail + "&password=" + password;

        // Erstellen Sie HTTP-Header mit JSON-Content-Type
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        try {
            System.out.println(restTemplate.getForEntity(serviceUrl, String.class));
            ResponseEntity<String> response = restTemplate.getForEntity(serviceUrl, String.class);

            if (response.getStatusCode() == HttpStatus.OK) {
                String jsonResponse = response.getBody();
                System.out.println("Response: " + jsonResponse);
                return ResponseEntity.ok(jsonResponse);
            } else {
                return ResponseEntity.status(response.getStatusCode()).build();
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    public List<String> extractStocksFromResponseForUser(String mail, String password) throws JsonProcessingException {
        ResponseEntity jsonResponse = getAllStocksForUserFromUserService(mail, password);
        String jsonResponseString = (String) jsonResponse.getBody();

        ObjectMapper objectMapper = new ObjectMapper();

        List<String> stockSymbols;

        List<Map<String, Object>> responseList = objectMapper.readValue(jsonResponseString, new TypeReference<List<Map<String, Object>>>() {
        });

        stockSymbols = new ArrayList<>();

        for (Map<String, Object> obj : responseList) {
            if (obj.containsKey("stockSymbol")) {
                String stockSymbol = (String) obj.get("stockSymbol");
                stockSymbols.add(stockSymbol);
            }
        }

        return stockSymbols;

    }
    public ResponseEntity sendMailtoAllUserSubscribers() throws JsonProcessingException {
        ResponseEntity response = getAllStocksForAllUsersFromUserService();
        String responseBody = (String) response.getBody();
        ObjectMapper objectMapper = new ObjectMapper();
        List<Map<String, Object>> responseList = objectMapper.readValue(responseBody, new TypeReference<List<Map<String, Object>>>() {
        });

        DocumentServiceConnection documentServiceConnection = new DocumentServiceConnection();
        for (Map<String, Object> obj : responseList) {
            if (obj.containsKey("stockSymbol") && obj.containsKey("mail")) {
                String stockSymbol = (String) obj.get("stockSymbol");
                String mail = (String) obj.get("mail");
                byte[] pdf = documentServiceConnection.createAndReturnPdf(stockSymbol);
                if (pdf != null) {
                    mailService.sendEmail(mail, "Stock report for " + stockSymbol, "The pdf file is attached to the mail.", pdf, stockSymbol + ".pdf");
                } else {
                    return new ResponseEntity<>("An error occured, file is empty", HttpStatus.OK);
                }
            } else {
                return new ResponseEntity<>("No mails have been sent", HttpStatus.OK);
            }
        }
        return new ResponseEntity<>("Mail have been sent", HttpStatus.OK);

    }
}
