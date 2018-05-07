package rs.ac.uns.ftn.siem.web.dto;

import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.AuthorityUtils;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import rs.ac.uns.ftn.siem.model.AppUser;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

public class SecurityUser implements UserDetails {

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    private Long id;
    private String password;
    private String email;
    private Collection<? extends GrantedAuthority> role;
    private Boolean enabled;
    private String username;

    public SecurityUser() {
        super();
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public SecurityUser(AppUser user) {
        this.username = user.getUsername();
        this.id = user.getId();
        this.email = user.getEmail();
        this.password = user.getPassword();
        this.role = AuthorityUtils.commaSeparatedStringToAuthorityList(user.getRole().toString());
        this.enabled = user.getVerified();
    }

    @Override
    public String getUsername() {
        return this.username;
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return enabled;
    }

    @Override
    public String getPassword() {
        return this.password;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        List<GrantedAuthority> authoritiess = new ArrayList<>();
        if (this.role.toString().equals("[ADMIN]"))
            authoritiess.add(new SimpleGrantedAuthority("ADMIN"));
        else if (this.role.toString().equals("[OPERATOR]"))
            authoritiess.add(new SimpleGrantedAuthority("OPERATOR"));
        return authoritiess;
    }

}
