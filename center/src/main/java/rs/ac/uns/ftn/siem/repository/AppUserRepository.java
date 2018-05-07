package rs.ac.uns.ftn.siem.repository;


import org.springframework.data.jpa.repository.JpaRepository;
import rs.ac.uns.ftn.siem.model.AppUser;

public interface AppUserRepository extends JpaRepository<AppUser,Long> {
    AppUser findByUsername(String username);

}
