package rs.ac.uns.ftn.siem.web.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import rs.ac.uns.ftn.siem.model.Log;
import rs.ac.uns.ftn.siem.repository.LogRepository;
import rs.ac.uns.ftn.siem.service.LogService;
import rs.ac.uns.ftn.siem.web.dto.LogLine;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;

@RestController
@RequestMapping(value = "/logger")
public class LogController {

    @Autowired
    LogService logService;

    @GetMapping(value = "/hello")
    public String hello(){
        return "Hello, world";
    }

    @GetMapping(value = "/all")
    public ResponseEntity<Collection<Log>> getAll(){
        return new ResponseEntity<>(this.logService.findAll(), HttpStatus.OK);
    }

    @GetMapping
    public ResponseEntity<Collection<Log>> search(@RequestParam(value = "query") String query){
        System.out.println("Ajde majmunski kontroleru");
        return new ResponseEntity<>(this.logService.search(query), HttpStatus.OK);
    }

    @PostMapping(consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Log> postLogLine(@RequestBody Log log){
        // TODO: odraditi pametno cuvanje u bazu radi brzog pretrazivanja
        return new ResponseEntity<Log>(this.logService.save(log), HttpStatus.CREATED);
    }
}
