package rs.ac.uns.ftn.siem.web.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.web.bind.annotation.*;
import rs.ac.uns.ftn.siem.model.AppUser;
import rs.ac.uns.ftn.siem.security.TokenUtils;
import rs.ac.uns.ftn.siem.service.AppUserService;
import rs.ac.uns.ftn.siem.web.dto.AuthenticationRequestDto;
import rs.ac.uns.ftn.siem.web.dto.AuthenticationResponseDto;
import rs.ac.uns.ftn.siem.web.dto.SecurityUser;

import java.util.List;

@RestController
@RequestMapping("/users")
@CrossOrigin
public class AppUserController {
    //TO-DO OVDE GLEDAJ
    @Value("${siem.token.header}")
    private String tokenHeader;

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private TokenUtils tokenUtils;

    @Autowired
    private UserDetailsService userDetailsService;

    @Autowired
    private AppUserService appUserService;

    @PostMapping(value = "/login")
    public ResponseEntity<?> authenticationRequest(@RequestBody AuthenticationRequestDto authenticationRequest) {
        // Perform the authentication
        Authentication authentication = null;
        UsernamePasswordAuthenticationToken t = new UsernamePasswordAuthenticationToken(
                authenticationRequest.getUsername(), authenticationRequest.getPassword());

        try {
            authentication = this.authenticationManager.authenticate(t);
        } catch (AuthenticationException e) {
            return new ResponseEntity<>(e.getMessage(), HttpStatus.NOT_FOUND);
        }
        SecurityContextHolder.getContext().setAuthentication(authentication);
        // Reload password post-authentication so we can generate token
        UserDetails userDetails = this.userDetailsService.loadUserByUsername(authenticationRequest.getUsername());
        SecurityUser su = (SecurityUser) userDetails;
        String token = this.tokenUtils.generateToken(userDetails);
        // Return the token
        AuthenticationResponseDto authResponse = new AuthenticationResponseDto(token, su.getId(), su.getEmail(),
                su.getAuthorities().toString(), su.isEnabled(), su.getUsername());
        return new ResponseEntity<>(authResponse, HttpStatus.OK);
    }

    @PutMapping(value = "/{id}/verify")
    public ResponseEntity<?> verifyAccount(@PathVariable Long id) {
        this.appUserService.verifyAccount(id);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @GetMapping
    public List<AppUser> getUsers() {
        return appUserService.getAllUsers();
    }

}
