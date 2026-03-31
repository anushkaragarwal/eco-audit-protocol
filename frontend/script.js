function startAudit() {
    window.location.href = "dashboard.html";
}

function updateStatus(score) {
    let status = "";

    if (score >= 70) status = "🟢 Green Company";
    else if (score >= 50) status = "🟡 Moderate Risk";
    else status = "🔴 High Risk";

    document.getElementById("status").innerText = status;
}

function getScore() {
    let company = document.getElementById("company").value;

    document.getElementById("loading").style.display = "block";

    fetch(`http://127.0.0.1:5000/get_score/${company}`)
    .then(res => res.json())
    .then(data => {
        document.getElementById("loading").style.display = "none";

        let score = data.true_esg_score;

        document.getElementById("score").innerText = "ESG Score: " + score;
        document.getElementById("progress").style.width = score + "%";

        updateStatus(score);
    });
}

function detect() {
    let company = document.getElementById("company").value;

    fetch(`http://127.0.0.1:5000/detect_event/${company}`)
    .then(res => res.json())
    .then(data => {

        let score = data.new_score;

        document.getElementById("score").innerText = "ESG Score: " + score;
        document.getElementById("progress").style.width = score + "%";

        updateStatus(score);

        let interest = score < 60 ? 10 : 5;

        document.getElementById("interest").innerText =
            "Interest Rate: " + interest;

        document.getElementById("reason").innerText = data.event;

        if (score < 60) {
            alert("🚨 Environmental Violation Detected!");
        }
    });
}
