import promptSync from 'prompt-sync';

export default class Entry {
    static reciveText(msg: string): string {
        let prompt = promptSync();
        let text = prompt(`${msg} `)
        return text
    }
}