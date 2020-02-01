// if you checked "fancy-settings" in extensionizr.com, uncomment this lines

// var settings = new Store("settings", {
//     "sample_setting": "This is how you use Store.js to remember values"
// });
const getHelpData = (hash) => {
    let location = hash.match(/#\/([A-Z0-9_\/]*);/)[1];
    if (location === 'CYCLE2021_APPLICATION/STUDENT_DEMOGRAPHICS/1') {
        return Promise.resolve([
            {
                id: 'student_firstName',
                description: 'It\'s your name :/',
            },
            {
                id: 'student_middleInit',
                description: 'middle initial pls (optional)',
            },
            {
                id: 'student_lastName',
                description: 'ur last name',
            },
            {
                id: 'student_dob',
                description: 'when u were born',
                link: 'https://www.shutterfly.com/ideas/wp-content/uploads/2016/08/50-happy-birthday-quotes-thumb.jpg'
            },
        ]);
    }

    return Promise.resolve([]);
}

//example of using a message handler from the inject scripts
chrome.runtime.onMessage.addListener( (request, sender, sendResponse) => {
    debugger;
    switch (request.type) {
        case 'PAGE_CHANGE':
            getHelpData(request.payload)
                .then((helpData) => sendResponse({ helpData }));
            break;
        default:
            sendResponse();
            break;
    };
});
