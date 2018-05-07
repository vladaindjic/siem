package rs.ac.uns.ftn.siem.web.dto;

public class AuthenticationResponseDto {

    private String token;
    private Long id;
    private String email;
    private String role;
    private Boolean enabled;
    private String username;

    public AuthenticationResponseDto(String token, Long id, String email, String role, Boolean enabled, String username
    ) {
        super();
        this.token = token;
        this.id = id;
        this.email = email;
        this.role = role;
        this.enabled = enabled;
        this.username = username;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public Boolean getEnabled() {
        return enabled;
    }

    public void setEnabled(Boolean enabled) {
        this.enabled = enabled;
    }

    public AuthenticationResponseDto() {
        super();
    }

}
