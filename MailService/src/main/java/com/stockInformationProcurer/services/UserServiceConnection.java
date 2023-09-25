/**
 * The `UserServiceConnection` class is responsible for connecting to the UserService and retrieving
 * user information, including subscribed stocks, and sending reports to users.
 */
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

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Map;

@Service
public class UserServiceConnection {
    private final MailService mailService;

    @Autowired
    public UserServiceConnection(MailService mailService) {
        this.mailService = mailService;
    }

    /**
     * Retrieves a list of subscribed stocks for all users from the UserService.
     *
     * @return A ResponseEntity containing the JSON response with user stock information
     *         if successful, or an error response if there is an issue with the request.
     */
    public ResponseEntity getAllStocksForAllUsersFromUserService() {
        RestTemplate restTemplate = new RestTemplate();
        final String serviceUrl = "http://stockinformationprocurer-user-service-1:9050/getAllUserStocks";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        try {
            ResponseEntity<String> response = restTemplate.getForEntity(serviceUrl, String.class);

            if (response.getStatusCode() == HttpStatus.OK) {
                String jsonResponse = response.getBody();
                return ResponseEntity.ok(jsonResponse);
            } else {
                return ResponseEntity.status(response.getStatusCode()).build();
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    /**
     * Sends emails with stock reports to all user subscribers based on retrieved stock information.
     *
     * @return A ResponseEntity with a success message if emails are sent successfully,
     *         or an error message if there is an issue with sending emails or processing data.
     * @throws JsonProcessingException If there is an issue with JSON processing.
     */
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

                LocalDate end_date = java.time.LocalDate.now();
                LocalDate start_date = end_date.minusDays(8);
                DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd-MM-yyyy");

                byte[] pdf = documentServiceConnection.createAndReturnPdfForTimeFrame(stockSymbol, start_date.format(formatter), end_date.format(formatter));
                if (pdf != null) {
                    mailService.sendEmail(mail, "Stock report for " + stockSymbol, "The pdf file is attached to the mail.", pdf, stockSymbol + ".pdf");
                } else {
                    return new ResponseEntity<>("An error occured, file is empty", HttpStatus.OK);
                }
            } else {
                return new ResponseEntity<>("No mails have been sent", HttpStatus.OK);
            }
        }
        return new ResponseEntity<>("Mails have been sent", HttpStatus.OK);

    }
}
