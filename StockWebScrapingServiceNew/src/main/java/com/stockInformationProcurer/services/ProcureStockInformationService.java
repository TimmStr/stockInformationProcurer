package com.stockInformationProcurer.services;

import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

public class ProcureStockInformationService {
    String apiKey;
    String symbol;
    String apiTimeSeries = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=";

    public ProcureStockInformationService(String apiKey, String symbol) {
        this.apiKey = apiKey;
        this.symbol = symbol;
    }


    public String getStockInformation() {
        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            HttpGet request = new HttpGet(apiTimeSeries + symbol + "&apikey=" + apiKey);
            CloseableHttpResponse response = httpClient.execute(request);
            return EntityUtils.toString(response.getEntity());
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;

    }

}
