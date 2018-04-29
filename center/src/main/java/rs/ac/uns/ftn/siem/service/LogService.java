package rs.ac.uns.ftn.siem.service;

import rs.ac.uns.ftn.siem.model.Log;

import java.util.Collection;

public interface LogService {
    Log save(Log log);
    Collection<Log> findAll();
    Collection<Log> search(String query);
}
