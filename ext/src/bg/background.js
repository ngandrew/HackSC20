// if you checked "fancy-settings" in extensionizr.com, uncomment this lines

// var settings = new Store("settings", {
//     "sample_setting": "This is how you use Store.js to remember values"
// });
const getHelpData = (hash) => {
    let location = hash.match(/#\/CYCLE2021_APPLICATION\/([A-Z0-9_\/]*);/);
    if (location && location.length > 1) {
        return fetch(`https://fluent-plate-266907.appspot.com/api/helpData?location=${location[1]}`)
            .then(res => res.json())
            .then(({ data }) => data);
    }

    return Promise.resolve([]);
}

//example of using a message handler from the inject scripts
chrome.runtime.onMessage.addListener( (request, sender, sendResponse) => {
    switch (request.type) {
        case 'PAGE_CHANGE':
            getHelpData(request.payload)
                .then(helpData => sendResponse({ helpData }));
            break;
        default:
            sendResponse();
            break;
    };
    return true;
});
