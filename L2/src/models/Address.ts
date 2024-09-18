export default class Address {
    country: string;
    state: string;
    city: string;
    street: string;
    number: number;

    constructor(street: string, number: number, city: string, state: string, country: string) {
        this.street = street;
        this.number = number;
        this.city = city;
        this.state = state;
        this.country = country;
    }
}