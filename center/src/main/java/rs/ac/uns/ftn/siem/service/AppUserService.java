package rs.ac.uns.ftn.siem.service;

import rs.ac.uns.ftn.siem.model.AppUser;

import java.util.List;

public interface AppUserService {

	void verifyAccount(Long id);

	List<AppUser> getAllUsers();
}
