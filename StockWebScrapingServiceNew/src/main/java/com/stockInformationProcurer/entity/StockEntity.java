package com.stockInformationProcurer.entity;

import lombok.Data;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Document(collection = "stockinformations")
@Data
public class StockEntity {
    @Field(name = "symbol")
    private String symbol;
    @Field(name = "date")
    private String date;
    @Field(name = "open")
    private String open;
    @Field(name = "high")
    private String high;
    @Field(name = "low")
    private String low;
    @Field(name = "close")
    private String close;
    @Field(name = "volume")
    private String volume;

    public StockEntity(String symbol, String date, String open, String high, String low, String close, String volume) {
        this.symbol = symbol;
        this.date = date;
        this.open = open;
        this.high = high;
        this.low = low;
        this.close = close;
        this.volume = volume;
    }
}
