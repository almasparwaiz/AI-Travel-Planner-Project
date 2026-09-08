document.getElementById('travelForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = "Generating your personalized itinerary...";

    const payload = {
        name: document.getElementById('name').value,
        destination: document.getElementById('destination').value,
        days: parseInt(document.getElementById('days').value),
        budget: parseFloat(document.getElementById('budget').value),
        interests: document.getElementById('interests').value,
        travel_style: document.getElementById('travelStyle').value,
        technique: document.getElementById('technique').value
    };

    try {
        const response = await fetch('/generate-travel-plan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        resultDiv.innerHTML = `<pre>${data.plan}</pre>`;
    } catch (err) {
        resultDiv.innerHTML = "Error generating plan. Please try again.";
    }
});