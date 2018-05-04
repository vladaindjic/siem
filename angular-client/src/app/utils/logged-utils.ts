export class LoggedUtils {
    static getId() {
        if (this.isEmpty()) {
            return null;
        }
        return JSON.parse(localStorage.getItem('loggedUser')).LoginResponseDTO.Id._text;
    }

    static getToken() {
        if (this.isEmpty()) {
            return '';
        }
        console.log(JSON.parse(localStorage.getItem('loggedUser')));
        return JSON.parse(localStorage.getItem('loggedUser')).LoginResponseDTO.Token._text;
    }

    static getRole() {
        if (this.isEmpty()) {
            return null;
        }
        return JSON.parse(localStorage.getItem('loggedUser')).LoginResponseDTO.Role._text;
    }

    static clearLocalStorage() {
        localStorage.clear();
    }

    static isEmpty() {
        return localStorage.getItem('loggedUser') === null;
    }

    static getUsername() {
        return JSON.parse(localStorage.getItem('loggedUser')).LoginResponseDTO.Username._text;
    }

    static getUser() {
        return JSON.parse(localStorage.getItem('loggedUser')).LoginResponseDTO;
    }

    static getLoggedUser() {
        return localStorage.getItem('loggedUser');

    }

}
