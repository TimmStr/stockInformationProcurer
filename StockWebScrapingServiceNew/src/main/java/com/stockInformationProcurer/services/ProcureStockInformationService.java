package com.stockInformationProcurer.services;

import com.stockInformationProcurer.entity.StockEntity;
import com.stockInformationProcurer.repository.StockInformationRepository;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.json.JSONObject;

import java.util.Set;


public class ProcureStockInformationService {
    String apiKey;
    String symbol;
    StockInformationRepository stockInformationRepository;

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

    public String extractDataFromJson(String stockInformation) {

        String[] keys = {"Meta Data", "Time Series (Daily)", "2023-08-04", "1. open", "2. high", "3. low", "4. close",
                "5. volume"};
        String[] metaDataKeys = {"1. Information", "2. Symbol", "3. Last Refreshed", "4. Output Size", "5. Time Zone"};
        JSONObject jsonObject = new JSONObject(stockInformation);
        JSONObject metaDataJson = jsonObject.getJSONObject(keys[0]);
        JSONObject timeseriesJson = jsonObject.getJSONObject(keys[1]);
        Set dates = timeseriesJson.keySet();
        String symbol = metaDataJson.getString(metaDataKeys[1]);

        for (Object date : dates) {
            String date_as_string = date.toString();
            JSONObject stockInformationForDay = timeseriesJson.getJSONObject(date_as_string);
            StockEntity stockEntity = new StockEntity(symbol, date_as_string, stockInformationForDay.getString(keys[3]),
                    stockInformationForDay.getString(keys[4]), stockInformationForDay.getString(keys[5]),
                    stockInformationForDay.getString(keys[6]), stockInformationForDay.getString(keys[7]));
            stockInformationRepository.save(stockEntity);
        }
        return "Added Successful";
    }


    public void addStockInformation(StockEntity stockEntity) {
        if (this.stockInformationRepository.findBySymbol(stockEntity.getSymbol()) == null)
            this.stockInformationRepository.save(stockEntity);
    }
//    if (this.stockInformationRepository.findBySymbolAndDate(stockEntity.getSymbol(), stockEntity.getDate()) == null)
//            this.stockInformationRepository.save(stockEntity);

}
