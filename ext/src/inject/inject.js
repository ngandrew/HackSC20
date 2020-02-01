var oldHash = window.location.hash;
const updateHelpData = () => {
	if (window.location.hash !== oldHash) {
		oldHash = window.location.hash;
		chrome.extension.sendMessage({
			type: 'PAGE_CHANGE',
			payload: window.location.hash,
		}, response => {
			response.helpData.forEach(({
				id,
				description,
				link,
			}) => {
				if ($(`#${id}_help`).length !== 1) {
					return;
				}

				if (link) {
					description += '\n\nClick the ? to see more information.';
					$(`#${id}_help`).attr('href', link).attr('target', '_blank');
				}

				$(`#${id}_help`).replaceWith($(`#${id}_help`).clone());
				$(`#${id}_help`).attr('title', description);
			});
			$(document).tooltip();
		});
	}
}

chrome.runtime.sendMessage({}, response => {
	var readyStateCheckInterval = setInterval(() => {
		if (document.readyState === "complete") {
			clearInterval(readyStateCheckInterval);
			console.log(window.location);
		}
	}, 10);
	var titleCheckInterval = setInterval(updateHelpData, 10);
});
