package rs.ac.uns.ftn.siem.web;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.integration.annotation.ServiceActivator;
import rs.ac.uns.ftn.siem.model.Log;
import rs.ac.uns.ftn.siem.repository.LogRepository;

public class UDPConsumer {
    @Autowired
    LogRepository logRepository;

    @ServiceActivator
    public void consume(byte[] message){
        System.out.println("Kako jebeno nikad ne dolaziiiiiiiiiiiis!!!");
        String logLine = new String(message);

//        Log l = new Log();
//        l.setLine(logLine);
//        this.logRepository.save(l);


        System.out.println(logLine);
    }

}
