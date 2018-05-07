package rs.ac.uns.ftn.siem.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import rs.ac.uns.ftn.siem.model.AppUser;
import rs.ac.uns.ftn.siem.repository.AppUserRepository;
import rs.ac.uns.ftn.siem.web.dto.SecurityUser;

@Service
public class UserServiceDetailsImpl implements UserDetailsService {
	@Autowired
	private AppUserRepository userRepository;

	@Override
	public UserDetails loadUserByUsername(String username) {
		AppUser user = this.userRepository.findByUsername(username);
		if (user == null) {
			throw new UsernameNotFoundException(String.format("No user found with username '%s'.", username));
		} else {
			return new SecurityUser(user);
		}
	}
}
