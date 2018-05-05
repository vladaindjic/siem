package rs.ac.uns.ftn.siem.config;

import com.mongodb.*;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;
import rs.ac.uns.ftn.siem.repository.LogRepository;
import org.springframework.beans.factory.annotation.Value;

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

    @Value("${spring.data.mongodb.host}")
    private String host;

    @Value("${spring.data.mongodb.port}")
    private int port;

    @Value("${spring.data.mongodb.database}")
    private String database;

    @Value("${spring.data.mongodb.username}")
    private String username;

    @Value("${spring.data.mongodb.password}")
    private String password;

    @Value("${spring.data.mongodb.repositories.enabled}")
    private boolean enabled;

    @Bean
    public MongoClient mongoClient() {
        System.setProperty("javax.net.ssl.trustStore", "src/main/resources/siem_truststore");
        System.setProperty("javax.net.ssl.trustStorePassword", "siem123");

        System.setProperty("javax.net.ssl.keyStore", "src/main/resources/siem.p12");
        System.setProperty("javax.net.ssl.keyStorePassword", "siem");

        MongoClientURI uri = new MongoClientURI("mongodb://" + username + ":" + password +
                "@" + host + ":" + port + "/?authSource=" + database + "&ssl=" + enabled);
        return new MongoClient(uri);
    }

    @Bean
    public MongoTemplate mongoTemplate() {
        return new MongoTemplate(mongoClient(), "log-mongo");
    }

}
