package rs.ac.uns.ftn.siem.config;

import com.mongodb.*;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;
import rs.ac.uns.ftn.siem.repository.LogRepository;

import java.util.Arrays;

@EnableMongoRepositories(basePackageClasses = LogRepository.class)
@Configuration
public class MongoDBConfig {

//    @Bean
//    CommandLineRunner commandLineRunner(LogRepository logRepository) {
//        return strings -> {
//            logRepository.deleteAll();
//        };
//    }

    @Bean
    public MongoClient mongoClient() {
        System.setProperty("javax.net.ssl.trustStore", "/home/vi3/Faks/Bezbednost/siem/mongo-client-cert/mongodbTrustStore");
        System.setProperty("javax.net.ssl.trustStorePassword", "vladimir");

        System.setProperty("javax.net.ssl.keyStore", "/home/vi3/Faks/Bezbednost/siem/mongo-client-cert/springkeystore.jks");
        System.setProperty("javax.net.ssl.keyStorePassword", "vladimir");


        MongoClientURI uri = new MongoClientURI("mongodb://siem:siem_center123@localhost:27017/?authSource=log-mongo&ssl=true");
        return new MongoClient(uri);
    }

    @Bean
    public MongoTemplate mongoTemplate() {
        return new MongoTemplate(mongoClient(), "log-mongo");
    }

}
