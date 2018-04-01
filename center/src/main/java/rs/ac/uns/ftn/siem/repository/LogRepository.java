package rs.ac.uns.ftn.siem.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import rs.ac.uns.ftn.siem.model.Log;

public interface LogRepository extends MongoRepository<Log, Long> {
}
