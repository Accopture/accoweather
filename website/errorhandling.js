const delay = ms => new Promise(resolve => setTimeout(resolve, ms)); 

export async function makeErrorFunction(messageContent, paragraphID) {
    const errorDOM = document.createElement('p')
    errorDOM.textContent = messageContent
    errorDOM.id = paragraphID
    if (document.getElementById(paragraphID)) {return}
    document.getElementById('error-display').appendChild(errorDOM)
    await delay(3000)
    document.getElementById(paragraphID).remove()
    return
}

export class NotFoundError extends Error {
    constructor(message) {
        super(message)
        this.name = "NotFoundError"
    }
}