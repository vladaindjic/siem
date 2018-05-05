package rs.ac.uns.ftn.siem.service.impl;

import org.bson.Document;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.BasicQuery;
import org.springframework.stereotype.Service;
import rs.ac.uns.ftn.siem.model.Log;
import rs.ac.uns.ftn.siem.repository.LogRepository;
import rs.ac.uns.ftn.siem.service.LogService;
import rs.ac.uns.ftn.siem.sysql.SysqlParserAdapter;

import java.util.Collection;
import java.util.List;

@Service
public class LogServiceImpl implements LogService{

    @Autowired
    LogRepository logRepository;

    @Autowired
    SysqlParserAdapter sysqlParserAdapter;

    @Autowired
    MongoTemplate mongoTemplate;

    private static final String LOG_COLLECTION = "log";

    @Override
    public Log save(Log log) {
        System.out.println("Cuva se");
        Log l =  this.logRepository.save(log);
        System.out.println("Sacuvano: " + l.getHostname());
        return l;
    }

    @Override
    public Collection<Log> findAll() {
        return this.logRepository.findAll();
    }

    @Override
    public Collection<Log> search(String query) {
        try {
            BasicQuery basicQuery = this.sysqlParserAdapter.buildMongoQuery(query);

            List<Log> logs = mongoTemplate.find(basicQuery, Log.class, LOG_COLLECTION);
            return logs;

        }catch (Exception ex){
            ex.printStackTrace();
            return null;
        }
    }
}
