package rs.ac.uns.ftn.siem.service.impl;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import rs.ac.uns.ftn.siem.model.AppUser;
import rs.ac.uns.ftn.siem.repository.AppUserRepository;
import rs.ac.uns.ftn.siem.service.AppUserService;


@Service
public class AppUserServiceImpl implements AppUserService {
    @Autowired
    private AppUserRepository appUserRepository;

    @Override
    public List<AppUser> getAllUsers() {
        return this.appUserRepository.findAll();
    }

    @Override
    public void verifyAccount(Long id) {
       
    }

}
