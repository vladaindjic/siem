package rs.ac.uns.ftn.siem;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.beans.factory.config.AutowireCapableBeanFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ImportResource;
import rs.ac.uns.ftn.siem.sysql.SysqlParserAdapter;
import rs.ac.uns.ftn.siem.web.tcp.ThreadPooledServer;

@SpringBootApplication
@ImportResource("/configuration/udp-config.xml")
public class SiemApplication {

    @Bean
    SysqlParserAdapter getSysqlParserAdapter() {
        return new SysqlParserAdapter();
    }

    public static void main(String[] args) {
        ApplicationContext applicationContext = SpringApplication.run(SiemApplication.class, args);

        ThreadPooledServer server = new ThreadPooledServer(55555);
        AutowireCapableBeanFactory factory = applicationContext.getAutowireCapableBeanFactory();
        factory.autowireBean(server);
        new Thread(server).start();

    }
}
