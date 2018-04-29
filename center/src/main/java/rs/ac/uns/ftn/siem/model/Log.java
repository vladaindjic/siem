package rs.ac.uns.ftn.siem.model;

import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.index.CompoundIndexes;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.Date;

@Document
@CompoundIndexes({
        @CompoundIndex(def = "{'timestamp':-1, 'hostname':1}", background = true, name = "time_host_ind")
})
public class Log {

    @Id
    private String id;
    private int facility;
    private int severity;
    private int version;
    private Date timestamp;
    private String hostname;
    private String appname;
    private String procid;
    private String msgid;
    private String msg;
    private String line;

    public Log() {
    }

    public Log(String id, String line) {
        this.id = id;
        this.line = line;
    }

    public Log(String id, int facility, int severity, int version, Date timestamp, String hostname, String appname,
               String procid, String msgid, String msg, String line) {
        this.id = id;
        this.facility = facility;
        this.severity = severity;
        this.version = version;
        this.timestamp = timestamp;
        this.hostname = hostname;
        this.appname = appname;
        this.procid = procid;
        this.msgid = msgid;
        this.msg = msg;
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

    public int getFacility() {
        return facility;
    }

    public void setFacility(int facility) {
        this.facility = facility;
    }

    public int getSeverity() {
        return severity;
    }

    public void setSeverity(int severity) {
        this.severity = severity;
    }

    public int getVersion() {
        return version;
    }

    public void setVersion(int version) {
        this.version = version;
    }

    public Date getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Date timestamp) {
        this.timestamp = timestamp;
    }

    public String getHostname() {
        return hostname;
    }

    public void setHostname(String hostname) {
        this.hostname = hostname;
    }

    public String getAppname() {
        return appname;
    }

    public void setAppname(String appname) {
        this.appname = appname;
    }

    public String getProcid() {
        return procid;
    }

    public void setProcid(String procid) {
        this.procid = procid;
    }

    public String getMsgid() {
        return msgid;
    }

    public void setMsgid(String msgid) {
        this.msgid = msgid;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }
}
