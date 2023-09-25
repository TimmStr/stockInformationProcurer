/**
 * The `DocumentServiceConnection` class is responsible for connecting to the DocumentService
 * and requesting the generation of a PDF document for a specified time frame and stock ticker.
 */
package com.stockInformationProcurer.services;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

public class DocumentServiceConnection {

    /**
     * Creates and retrieves a PDF document for a given stock ticker and time frame by
     * making a RESTful API call to the DocumentService.
     *
     * @param ticker     The stock ticker symbol for which the PDF document is requested.
     * @param start_date The start date of the time frame for the document.
     * @param end_date   The end date of the time frame for the document.
     * @return A byte array containing the PDF document if successful, or null if there was an error.
     */
    public byte[] createAndReturnPdfForTimeFrame(String ticker, String start_date, String end_date) {
        // Create a RestTemplate instance for making HTTP requests.
        RestTemplate restTemplate = new RestTemplate();

        // Hardcoded credentials for authentication so the documents can be created for all users.
        String mail = "admin@admin.com";
        String password = "admin";

        // The URL for the DocumentService with query parameters.
        final String serviceUrl = "http://stockinformationprocurer-document-service-1:9010/createPdf?ticker=" + ticker +
                "&mail=" + mail +
                "&password=" + password +
                "&start_date=" + start_date +
                "&end_date=" + end_date;

        // Set the request headers to specify JSON content type
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        try {
            // Send an HTTP GET request to the document generation service.
            ResponseEntity<byte[]> response = restTemplate.getForEntity(serviceUrl, byte[].class);

            // Check if the response status code is OK (200).
            if (response.getStatusCode() == HttpStatus.OK) {
                return response.getBody(); // Return the generated PDF document.
            }
        } catch (Exception e) {
            e.printStackTrace(); // Handle any exceptions that occur during the request.
        }
        return null; // Return null if there was an error.
    }
}
