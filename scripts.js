function generateSchedule() {
    let hardSubjects = document.getElementById("hardSubjects").value.split(",").map(s => s.trim());
    let intermediateSubjects = document.getElementById("intermediateSubjects").value.split(",").map(s => s.trim());
    let easySubjects = document.getElementById("easySubjects").value.split(",").map(s => s.trim());
    let studyHours = parseInt(document.getElementById("studyHours").value);
    let deadline = new Date(document.getElementById("deadline").value);

    let today = new Date();
    let schedule = [];

    let allSubjects = [...hardSubjects, ...intermediateSubjects, ...easySubjects].filter(sub => sub !== "");

    let timeSlots = [
        "9:00 AM - 11:00 AM",
        "11:30 AM - 1:30 PM",
        "2:30 PM - 4:30 PM",
        "5:00 PM - 7:00 PM",
        "7:30 PM - 9:30 PM"
    ];

    let slotsPerDay = Math.min(studyHours, timeSlots.length); // Limit slots per day
    let durationPerSlot = studyHours / slotsPerDay; // Divide total study hours

    while (today <= deadline) {
        let dateStr = today.toDateString();
        let dayStr = today.toLocaleDateString("en-US", { weekday: "long" });

        let subjectIndex = 0; 

        for (let i = 0; i < slotsPerDay && subjectIndex < allSubjects.length; i++) {
            let subject = allSubjects[subjectIndex]; 
            let startTime = timeSlots[i].split(" - ")[0];
            let endTime = new Date(new Date(`2023-01-01 ${startTime}`).getTime() + durationPerSlot * 60 * 60 * 1000);
            let formattedEndTime = endTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });

            schedule.push({
                date: dateStr,
                day: dayStr,
                timeSlot: `${startTime} - ${formattedEndTime}`, // Correct time calculation
                subject: subject,
                duration: `${durationPerSlot.toFixed(1)} hours`
            });

            subjectIndex++;
            if (subjectIndex >= allSubjects.length) {
                subjectIndex = 0;
            }
        }

        today.setDate(today.getDate() + 1);
    }

    let tableBody = document.querySelector("#studyPlanTable tbody");
    tableBody.innerHTML = ""; // ✅ Fixed: Now correctly selecting table body

    schedule.forEach((entry, index) => {
        let row = tableBody.insertRow();

        if (index === 0 || schedule[index - 1].date !== entry.date) {
            let dateCell = row.insertCell();
            dateCell.rowSpan = schedule.filter(e => e.date === entry.date).length;
            dateCell.innerHTML = `<strong>${entry.date}</strong>`;

            let dayCell = row.insertCell();
            dayCell.rowSpan = dateCell.rowSpan;
            dayCell.innerHTML = entry.day;
        }

        row.insertCell().innerHTML = entry.timeSlot;
        row.insertCell().innerHTML = `<strong>${entry.subject}</strong>`;
        row.insertCell().innerHTML = entry.duration;
    });
}
