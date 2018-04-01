package rs.ac.uns.ftn.siem.model;

import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;

public class Log {

    @Id
    private String id;
    private String line;

    public Log() {
    }

    public Log(String id, String line) {
        this.id = id;
        this.line = line;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getLine() {
        return line;
    }

    public void setLine(String line) {
        this.line = line;
    }
}
