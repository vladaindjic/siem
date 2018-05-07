package rs.ac.uns.ftn.siem.security;

import java.io.UnsupportedEncodingException;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import rs.ac.uns.ftn.siem.web.dto.SecurityUser;

@Component
public class TokenUtils {

	@Value("${siem.token.secret}")
	private String secret;

	@Value("${siem.token.expiration}")
	private Long expiration;

	public String getUsernameFromToken(String token) {
		String username;
		try {
			final Claims claims = this.getClaimsFromToken(token);
			username = claims.getSubject();
		} catch (Exception e) {
			username = null;
		}
		return username;
	}

	public Date getCreatedDateFromToken(String token) {
		Date created;
		try {
			final Claims claims = this.getClaimsFromToken(token);
			created = new Date((Long) claims.get("created"));
		} catch (Exception e) {
			created = null;
		}
		return created;
	}

	public Date getExpirationDateFromToken(String token) {
		Date expiration;
		try {
			final Claims claims = this.getClaimsFromToken(token);
			expiration = claims.getExpiration();
		} catch (Exception e) {
			expiration = null;
		}
		return expiration;
	}

	private Claims getClaimsFromToken(String token) {
		Claims claims;
		try {
			claims = Jwts.parser().setSigningKey(this.secret.getBytes("UTF-8")).parseClaimsJws(token).getBody();
		} catch (Exception e) {
			claims = null;
		}
		return claims;
	}

	private Date generateCurrentDate() {
		return new Date(System.currentTimeMillis());
	}

	private Date generateExpirationDate() {
		return new Date(System.currentTimeMillis() + this.expiration * 1000);
	}

	private Boolean isTokenExpired(String token) {
		final Date expiration = this.getExpirationDateFromToken(token);
		return expiration.before(this.generateCurrentDate());
	}

	public String generateToken(UserDetails userDetails) {
		Map<String, Object> claims = new HashMap<>();
		claims.put("sub", userDetails.getUsername());
		claims.put("created", this.generateCurrentDate());
		claims.put("authority", userDetails.getAuthorities());
		return this.generateToken(claims);
	}

	private String generateToken(Map<String, Object> claims) {
		try {
			return Jwts.builder().setClaims(claims).setExpiration(this.generateExpirationDate())
					.signWith(SignatureAlgorithm.HS512, this.secret.getBytes("UTF-8")).compact();
		} catch (UnsupportedEncodingException ex) {
			return Jwts.builder().setClaims(claims).setExpiration(this.generateExpirationDate())
					.signWith(SignatureAlgorithm.HS512, this.secret).compact();
		}
	}

	public Boolean validateToken(String token, UserDetails userDetails) {
		SecurityUser user = (SecurityUser) userDetails;
		final String username = this.getUsernameFromToken(token);
		return username.equals(user.getUsername()) && !this.isTokenExpired(token);
	}

}
