package rs.ac.uns.ftn.siem.web.dto;

public class LogLine {
    String content;

    public LogLine(){

    }

    public LogLine(String content) {
        this.content = content;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }
}

