package com.stockInformationProcurer;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.InetAddress;
import java.net.MalformedURLException;
import java.net.URL;

@SpringBootApplication
public class Main {
    public static void main(String[] args) throws IOException {
        SpringApplication.run(Main.class, args);
        System.out.println("Version 2.0");
//        System.out.println("http://172.20.0.8:8080/");
//        System.out.println(sendGetRequest("http://172.20.0.8:8080/"));
//        System.out.println();
//        System.out.println("http://172.20.0.8:8080/auth/realms/stock-information-procurer/");
//        System.out.println(sendGetRequest("http://172.20.0.8:8080/auth/realms/stock-information-procurer/"));
//        System.out.println();
//        System.out.println("http://172.20.0.8:8080/auth/realms/stock-information-procurer/protocol/openid-connect/certs");
//        System.out.println(sendGetRequest("http://172.20.0.8:8080/auth/realms/stock-information-procurer/protocol/openid-connect/certs"));
    }

    public static String sendGetRequest(String url) throws IOException {
        URL urlObj = new URL(url);
        HttpURLConnection connection = (HttpURLConnection) urlObj.openConnection();

        // Optional: Setzen Sie Anforderungsparameter oder Header, wenn erforderlich
        // connection.setRequestProperty("Header-Name", "Header-Wert");

        connection.setRequestMethod("GET");

        int responseCode = connection.getResponseCode();
        if (responseCode == HttpURLConnection.HTTP_OK) {
            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            StringBuilder response = new StringBuilder();
            String inputLine;

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();

            return response.toString();
        } else {
            throw new IOException("GET-Anfrage fehlgeschlagen. Response-Code: " + responseCode);
        }
    }
}
