package rs.ac.uns.ftn.siem.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;

import javax.persistence.*;
import javax.validation.constraints.Size;



@Entity
@Table(name = "app_user")
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
public class AppUser {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    protected Long id;

    @Column(name = "username", unique = true, nullable = false)
    @Size(min = 3)
    protected String username;

    @JsonIgnore
    @Column(name = "password", nullable = false)
    @Size(min = 3)
    protected String password;

    @Column(name = "email", unique = true, nullable = false)
    protected String email;

    @Column(name = "verified")
    protected Boolean verified;

    @Column(name = "role", nullable = false)
    @Enumerated(EnumType.STRING)
    protected UserRole role;

    public AppUser() {
    }

    public AppUser(Long id, String username, String password, String email, String firstname, String lastname,
                   UserRole role, Boolean verified) {
        this.id = id;
        this.username = username;
        this.password = password;
        this.email = email;
        this.role = role;
        this.verified = verified;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Boolean getVerified() {
        return verified;
    }

    public void setVerified(Boolean verified) {
        this.verified = verified;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    @JsonProperty
    public void setPassword(String password) {
        this.password = password;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public UserRole getRole() {
        return role;
    }

    public void setRole(UserRole role) {
        this.role = role;
    }

    @Override
    public String toString() {
        return "AppUser [id=" + id + ", username=" + username + ", password=" + password + ", email=" + email
                + ", verified=" + verified + ", role=" + role
                + "]";
    }

}