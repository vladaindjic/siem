package rs.ac.uns.ftn.siem.config;

import com.mongodb.MongoClient;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;
import rs.ac.uns.ftn.siem.repository.LogRepository;

@EnableMongoRepositories(basePackageClasses = LogRepository.class)
@Configuration
public class MongoDBConfig {

    @Bean
    CommandLineRunner commandLineRunner(LogRepository logRepository) {
        return strings -> {
            logRepository.deleteAll();
        };
    }

    @Bean
    public MongoClient mongoClient() {
        return new MongoClient("localhost", 27017);
    }

    @Bean
    public MongoTemplate mongoTemplate() {
        return new MongoTemplate(mongoClient(), "log-mongo");
    }

}
