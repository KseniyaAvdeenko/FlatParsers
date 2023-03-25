import axios from 'axios';

const API_URL = 'http://localhost:8000';

export default class FlatService {
    getFlats() {
        const url = `${API_URL}/flats/`;
        return axios.get(url).then(response => response.data)
    }
    getFlat(pk) {
        const url = `${API_URL}/flats/${pk}/`;
        return axios.get(url).then(response => response.data);
    }
}