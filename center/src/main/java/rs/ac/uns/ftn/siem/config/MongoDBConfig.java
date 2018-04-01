package rs.ac.uns.ftn.siem.config;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
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

}
