

const SESSION_KEY = 'rag_session_id';


function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
        const r = (Math.random() * 16) | 0;
        const v = c === 'x' ? r : (r & 0x3) | 0x8;
        return v.toString(16);
    });
}


export function getSessionId() {
    let id = localStorage.getItem(SESSION_KEY);
    if (!id) {
        id = generateUUID();
        localStorage.setItem(SESSION_KEY, id);
    }
    return id;
}


export function setSessionId(id) {
    localStorage.setItem(SESSION_KEY, id);
}


export function createNewSession() {
    const id = generateUUID();
    localStorage.setItem(SESSION_KEY, id);
    return id;
}


function parseUTCDate(isoString) {
    if (!isoString) return new Date();
    // SQLite returns "YYYY-MM-DD HH:MM:SS" without timezone.
    // We must append 'Z' so JavaScript treats it as UTC.
    let safeString = isoString;
    if (!isoString.includes('T') && !isoString.endsWith('Z') && !isoString.includes('+')) {
        safeString = isoString.replace(' ', 'T') + 'Z';
    } else if (isoString.includes('T') && !isoString.endsWith('Z') && !isoString.includes('+')) {
        safeString = isoString + 'Z';
    }
    return new Date(safeString);
}


export function formatTime(isoString) {
    if (!isoString) return '';
    try {
        const date = parseUTCDate(isoString);
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true,
        });
    } catch {
        return '';
    }
}


export function formatFullTime(isoString) {
    if (!isoString) return '';
    try {
        const date = parseUTCDate(isoString);
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true,
        });
    } catch {
        return '';
    }
}

