export class LoggedUtils {

    static getToken() {
        if (this.isEmpty()) {
            return '';
        }
         return JSON.parse(sessionStorage.getItem('loggedUser')).token;
    }

    static getRole() {
        if (this.isEmpty()) {
            return null;
        }
        if (JSON.parse(sessionStorage.getItem('loggedUser')).user.is_admin) {
            return '[ADMIN]'
        } else if (JSON.parse(sessionStorage.getItem('loggedUser')).user.is_operator) {
            return '[OPERATOR]'
        } else if (JSON.parse(sessionStorage.getItem('loggedUser')).user.is_superuser) {
            return '[SUPERUSER]'
        }
        return null;

    }

    static clearLocalStorage() {
      sessionStorage.clear();
    }

    static isEmpty() {
        return sessionStorage.getItem('loggedUser') === null;
    }

    static getUsername() {
      // return JSON.parse(sessionStorage.getItem('loggedUser')).user.username._text;
      return JSON.parse(sessionStorage.getItem('loggedUser')).user.username;
    }

    static getUser() {
        return JSON.parse(sessionStorage.getItem('loggedUser'));
    }

    static getLoggedUser() {
        return sessionStorage.getItem('loggedUser');

    }

}
