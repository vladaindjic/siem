package rs.ac.uns.ftn.siem.sysql;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class SysqlParserAdapter {
    private static final String ip = "localhost";
    private static final int port = 33333;

    public SysqlParserAdapter(){}

    private Socket takeSocket() throws IOException{
        return new Socket(ip, port);
    }

    private void putbackSocket(Socket socket) throws IOException{
        socket.close();
    }

    public String parse(String sysql){
        try {
            Socket socket = takeSocket();
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            out.println(sysql);
            String s = in.readLine();
            System.out.println("Response: " + s);
            putbackSocket(socket);
            return s;
        }catch (IOException e){
            e.printStackTrace();
        }

        return "";
    }


    public static void main(String[] args){
        SysqlParserAdapter sysqlParserAdapter = new SysqlParserAdapter();
        String s = sysqlParserAdapter.parse("before(2014-11-12) and not severity<10");
        System.out.println(s);
    }

}
