package rs.ac.uns.ftn.siem.web.controller;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import rs.ac.uns.ftn.siem.web.dto.LogLine;

@RestController
@RequestMapping(value = "/logger")
public class LogController {

    @GetMapping
    public String hello(){
        return "Hello, world";
    }

    @PostMapping(consumes = MediaType.TEXT_PLAIN_VALUE)
    public String postLogLine(@RequestBody String logLine){
        System.out.println(String.format("We get log line: %s", logLine));
        // TODO: odraditi pametno cuvanje u bazu radi brzog pretrazivanja
        return "Uspesno pristiglo";
    }
}
