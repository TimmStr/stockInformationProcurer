package com.stockInformationProcurer.controller;

import com.stockInformationProcurer.services.ProcureStockInformationService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class StockWebScrapingServiceController {


    @RequestMapping(value = "/get")
    public ResponseEntity welcome() {
        return new ResponseEntity<>("Stock Analysis Service Controller works", HttpStatus.OK);
    }

    @RequestMapping(value = "/getStockInformation")
    public ResponseEntity getStockInformation() {
        ProcureStockInformationService procureStockInformationService = new ProcureStockInformationService("demo", "MSFT");
        procureStockInformationService.extractDataFromJson(procureStockInformationService.getStockInformation());
        return new ResponseEntity<>(procureStockInformationService.getStockInformation(), HttpStatus.OK);
    }

}
