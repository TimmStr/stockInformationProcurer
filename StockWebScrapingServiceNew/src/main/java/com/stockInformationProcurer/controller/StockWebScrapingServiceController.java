package com.stockInformationProcurer.controller;

import com.stockInformationProcurer.services.ProcureStockInformationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class StockWebScrapingServiceController {
    private final ProcureStockInformationService procureStockInformationService;

    @Autowired
    public StockWebScrapingServiceController(ProcureStockInformationService procureStockInformationService) {
        this.procureStockInformationService = procureStockInformationService;
    }


    @RequestMapping(value = "/get")
    public ResponseEntity welcome() {
        return new ResponseEntity<>("Stock Analysis Service Controller works", HttpStatus.OK);
    }

    @RequestMapping(value = "/getStockInformation")
    public ResponseEntity getStockInformation() {
        String stockinformation = procureStockInformationService.getStockInformation("demo", "MSFT");
        procureStockInformationService.extractDataFromJson(stockinformation);
        return new ResponseEntity<>(stockinformation, HttpStatus.OK);
    }

}
