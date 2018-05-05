package rs.ac.uns.ftn.siem;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ImportResource;
import rs.ac.uns.ftn.siem.sysql.SysqlParserAdapter;

@SpringBootApplication
@ImportResource("/configuration/udp-config.xml")
public class SiemApplication {
    @Bean
    SysqlParserAdapter getSysqlParserAdapter() {
        return new SysqlParserAdapter();
    }

    public static void main(String[] args) {
        SpringApplication.run(SiemApplication.class, args);
    }
}
