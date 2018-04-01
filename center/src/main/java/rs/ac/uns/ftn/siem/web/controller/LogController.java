package rs.ac.uns.ftn.siem.web.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import rs.ac.uns.ftn.siem.model.Log;
import rs.ac.uns.ftn.siem.repository.LogRepository;
import rs.ac.uns.ftn.siem.web.dto.LogLine;

import java.util.Collection;
import java.util.Collections;

@RestController
@RequestMapping(value = "/logger")
public class LogController {

    @Autowired
    LogRepository logRepository;


    @GetMapping(value = "/hello")
    public String hello(){
        return "Hello, world";
    }

    @GetMapping(value = "/all")
    public ResponseEntity<Collection<Log>> getAll(){
        return new ResponseEntity<>(this.logRepository.findAll(), HttpStatus.OK);
    }

    @PostMapping(consumes = MediaType.TEXT_PLAIN_VALUE)
    public String postLogLine(@RequestBody String logLine){
        System.out.println(String.format("We get log line: %s", logLine));
        // TODO: odraditi pametno cuvanje u bazu radi brzog pretrazivanja

        Log l = new Log();
        l.setLine(logLine);
        this.logRepository.save(l);

        return "Uspesno pristiglo";
    }
}
