package rs.ac.uns.ftn.siem;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ImportResource;
import org.springframework.data.mongodb.core.MongoTemplate;

@SpringBootApplication
@ImportResource("/configuration/udp-config.xml")
public class SiemApplication {

	public static void main(String[] args) {
		SpringApplication.run(SiemApplication.class, args);
	}
}
