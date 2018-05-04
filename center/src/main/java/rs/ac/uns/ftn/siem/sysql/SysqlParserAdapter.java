package rs.ac.uns.ftn.siem.sysql;

import org.bson.Document;
import org.springframework.data.mongodb.core.query.BasicQuery;

import javax.net.ssl.SSLSocketFactory;
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
        return ((SSLSocketFactory)SSLSocketFactory.getDefault()).createSocket(ip, port);
//        return new Socket(ip, port);
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

    private String splitByEqualAndGetValue(String toSplit){
        return toSplit.split("=")[1];
    }

    public BasicQuery buildMongoQuery(String sysql) throws Exception{
        String str_mongo = this.parse(sysql);

        str_mongo = str_mongo.trim();
        String[] parts = str_mongo.split(";");
        if (parts.length < 1){
            throw new Exception("Invalid query: " + sysql);
        }
        String bson_mongo_query = parts[0];
        int limit = -1;
        int page = -1;
        String bson_sort = null;

        for (String s: parts){
            if(s.startsWith("limit")){
                limit = Integer.parseInt(this.splitByEqualAndGetValue(s));
            }else if(s.startsWith("page")){
                page = Integer.parseInt(this.splitByEqualAndGetValue(s));
            }else if(s.startsWith("sort")){
                bson_sort = this.splitByEqualAndGetValue(s);
            }
        }


//        BasicQuery basicQuery = new BasicQuery("{timestamp: {$lt: ISODate(\"2014-11-12T00:00:00+0200\")}, severity: {$gte: 10}}");
        BasicQuery basicQuery = new BasicQuery(bson_mongo_query);
        if(limit != -1 && page != -1){
            basicQuery.limit(limit);
            basicQuery.skip(page * limit);
        }

        if (bson_sort != null){
            System.out.println(bson_sort);
            basicQuery.setSortObject(Document.parse(bson_sort));
        }

        // da li imamo sort
        return basicQuery;

    }


    public static void main(String[] args) throws Exception{
        System.setProperty("javax.net.ssl.trustStore", "/home/vi3/Faks/Bezbednost/siem/mongo-client-cert/mongodbTrustStore");
        System.setProperty("javax.net.ssl.trustStorePassword", "vladimir");

        System.setProperty("javax.net.ssl.keyStore", "/home/vi3/Faks/Bezbednost/siem/mongo-client-cert/springkeystore.jks");
        System.setProperty("javax.net.ssl.keyStorePassword", "vladimir");

        SysqlParserAdapter sysqlParserAdapter = new SysqlParserAdapter();
        String s = sysqlParserAdapter.parse("before(2014-11-12) and not severity<10; page(3), limit(5), sort(hostname:asc, appname:desc)");
        System.out.println(s);

        BasicQuery basicQuery = sysqlParserAdapter.buildMongoQuery("before(2014-11-12) and not severity<10; page(3), limit(5), sort(hostname:asc, appname:desc)");
        System.out.println(basicQuery);
        String bson = "{timestamp:-1, hostname:1}";
        Document document = Document.parse(bson);
        System.out.println(document);
    }

}
