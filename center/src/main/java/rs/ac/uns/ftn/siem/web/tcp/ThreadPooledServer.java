package rs.ac.uns.ftn.siem.web.tcp;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import rs.ac.uns.ftn.siem.service.LogService;

import javax.net.ssl.*;
import java.io.FileInputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.io.IOException;
import java.security.KeyStore;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

@Component
public class ThreadPooledServer implements Runnable{
    @Autowired
    LogService logService;


    protected int          serverPort   = 55555;
    protected ServerSocket serverSocket = null;
    protected boolean      isStopped    = false;
    protected Thread       runningThread= null;
    protected ExecutorService threadPool =
            Executors.newFixedThreadPool(10);


    @Value("${key-store-path}")
    private String keyStore;

    @Value("${server.ssl.key-store-password}")
    private String keyStorePassword;

    @Value("${trust-store-path}")
    private String trustStore;

    @Value("${server.ssl.trust-store-password}")
    private String trustStorePassword;




    public ThreadPooledServer(){
    }

    public ThreadPooledServer(int port){
        this.serverPort = port;
    }

    public void run(){
        synchronized(this){
            this.runningThread = Thread.currentThread();
        }
        try {
            openServerSocket();
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException("Cannot open server socket");
        }
        while(! isStopped()){
            Socket clientSocket = null;
            try {
                clientSocket = this.serverSocket.accept();
            } catch (IOException e) {
                if(isStopped()) {
                    System.out.println("Server Stopped.") ;
                    break;
                }
                throw new RuntimeException(
                        "Error accepting client connection", e);
            }
            this.threadPool.execute(
                    new WorkerRunnable(clientSocket, this.logService));
        }
        this.threadPool.shutdown();
        System.out.println("Server Stopped.") ;
    }


    private synchronized boolean isStopped() {
        return this.isStopped;
    }

    public synchronized void stop(){
        this.isStopped = true;
        try {
            this.serverSocket.close();
        } catch (IOException e) {
            throw new RuntimeException("Error closing server", e);
        }
    }

    private void openServerSocket() throws Exception{
        try {
            KeyStore ks = KeyStore.getInstance("PKCS12");
            ks.load(new FileInputStream(keyStore), keyStorePassword.toCharArray());

            KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
            kmf.init(ks, "siem".toCharArray());

            KeyStore ts = KeyStore.getInstance("JKS");
            ts.load(new FileInputStream(trustStore), trustStorePassword.toCharArray());

            TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
            tmf.init(ts);


            SSLContext sc = SSLContext.getInstance("TLSv1.2");
            sc.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);

            SSLServerSocketFactory ssf = sc.getServerSocketFactory();
            this.serverSocket = ssf.createServerSocket(this.serverPort);


            System.out.println("Uspesno sam ga kreirao na portu: " + serverPort);
        } catch (IOException e) {
            throw new RuntimeException("Cannot open port 8080", e);
        }
    }

    public static void main(String args[]){
        ThreadPooledServer server = new ThreadPooledServer(55555);
        new Thread(server).start();

        try {
            Thread.sleep(100 * 1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("Stopping Server");
        server.stop();
    }
}
