export class LoggedUtils {

    static getToken() {
        if (this.isEmpty()) {
            return '';
        }
        console.log(JSON.parse(localStorage.getItem('loggedUser')));
        return JSON.parse(localStorage.getItem('loggedUser')).token._text;
    }

    static getRole() {
        if (this.isEmpty()) {
            return null;
        }
        console.log(JSON.parse(localStorage.getItem('loggedUser')));
        if (JSON.parse(localStorage.getItem('loggedUser')).user.is_superuser) {
            return '[ADMIN]'
        } else if (!JSON.parse(localStorage.getItem('loggedUser')).user.is_superuser) {
            return '[OPERATOR]'
        }
        return null;

    }

    static clearLocalStorage() {
        localStorage.clear();
    }

    static isEmpty() {
        return localStorage.getItem('loggedUser') === null;
    }

    static getUsername() {
        return JSON.parse(localStorage.getItem('loggedUser')).user.username._text;
    }

    static getUser() {
        return JSON.parse(localStorage.getItem('loggedUser'));
    }

    static getLoggedUser() {
        return localStorage.getItem('loggedUser');

    }

}
