const getDateText = last => {
    if(last == null) return `No downtime recorded`
    const startTimestamp = new Date(last[0]);  // Convert the first timestamp to Date
    const endTimestamp = new Date(last[1]);    // Convert the second timestamp to Date

    const timeDiff = endTimestamp - startTimestamp; // Difference in milliseconds
    const totalMinutes = Math.round(timeDiff / 60000); // Convert milliseconds to minutes

    const hours = Math.floor(totalMinutes / 60);  // Full hours
    const minutes = totalMinutes % 60;  // Remaining minutes after full hours
    return last[0] === "1970-01-01T00:00:00.000Z"
        ? "No downtime recorded"
        : last[1] === "1970-01-01T00:00:00.000Z"
            ? `Since ${startTimestamp.toUTCString()}`
            : hours > 0
                ? `Last downtime ended ${endTimestamp.toUTCString()} (lasted ${hours} hours ${minutes} minutes)`
                : `Last downtime ended ${endTimestamp.toUTCString()} (lasted ${minutes} minutes)`;
}
const getStatusText = status => status
    ? "good"
    : "bad";

function update(){
    (async () => {
        const response = await fetch('/api/check');
        const data = await response.json();

        const statusMap = data.status;
        const timeMap = data.times;

        for (const checkEl of document.querySelectorAll('.check')) {
            const { service } = checkEl.dataset;

            if (!statusMap.hasOwnProperty(service)) {
                checkEl.classList.remove('good', 'bad');
                checkEl.classList.add('unknown');
                checkEl.innerText = 'Service status not in API';
                continue;
            }
            const isGood = statusMap[service];

            checkEl.classList.remove('good', 'bad');
            checkEl.classList.add(isGood ? 'good' : 'bad');



            if (!timeMap.hasOwnProperty(service)) {
                checkEl.innerText = 'Downtimes not in API!';
                continue;
            }



            checkEl.innerText = getDateText(timeMap[service]);
        }
    })();
}

update();
setInterval(update, 300000); //Refresh every 5 minutes