package rs.ac.uns.ftn.siem.web.tcp;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import rs.ac.uns.ftn.siem.model.Log;
import rs.ac.uns.ftn.siem.service.LogService;

import java.io.*;
import java.net.Socket;

public class WorkerRunnable implements Runnable{


    protected Socket clientSocket = null;
    protected LogService logService   = null;

    public WorkerRunnable(Socket clientSocket, LogService logService) {
        this.clientSocket = clientSocket;
        this.logService = logService;
    }

    public void run() {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(this.clientSocket.getInputStream()));
            String line = null;
            while ((line = in.readLine()) != null){
                System.out.println("Stiglo mi je ovo: " + line);
                ObjectMapper mapper = new ObjectMapper();
                Log newLog = mapper.readValue(line.trim(), Log.class);
                System.out.println("Napravio objekat: " + newLog.getHostname());
                this.logService.save(newLog);
            }
            in.close();
        } catch (IOException e) {
            //report exception somewhere.
            e.printStackTrace();
        }
    }
}
