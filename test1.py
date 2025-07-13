from flask import Flask, render_template_string, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

FRESHDESK_API_KEY = "gYzoEaF1pREcMlNji6"
FRESHDESK_DOMAIN = "netcore"

# Use actual Dev Ops group ID
DEV_OPS_GROUP_ID = 17000124233

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Freshdesk Dev Ops Tickets</title>
</head>
<body>
    <h2>Dev Ops Tickets</h2>

    <input type="text" id="searchInput" placeholder="Search by subject..." onkeyup="filterTickets()" />
    <button onclick="fetchTickets()">Load Tickets</button>

    <ul id="tickets"></ul>

    <!-- Hidden ticket data store -->
    <div id="ticketData" style="display:none;"></div>

    <script>
        // Fetch and store ticket list
        function fetchTickets() {
            fetch('/tickets')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('ticketData').textContent = JSON.stringify(data);
                    // Do not render tickets yet — wait for search
                    document.getElementById('tickets').innerHTML = '<li>Tickets loaded. Please search to display results.</li>';
                });
        }

        // Filter and render only matching tickets
        function filterTickets() {
            const searchValue = document.getElementById('searchInput').value.toLowerCase();
            const rawData = document.getElementById('ticketData').textContent;
            const tickets = JSON.parse(rawData || "[]");

            // Filter tickets that match subject
            const filtered = tickets.filter(ticket =>
                ticket.subject && ticket.subject.toLowerCase().includes(searchValue)
            );

            renderTickets(filtered);
        }

        // Render filtered ticket list
        function renderTickets(tickets) {
            const ul = document.getElementById('tickets');
            ul.innerHTML = ''; // Clear old list

            if (tickets.length === 0) {
                const li = document.createElement('li');
                li.textContent = 'No tickets found.';
                ul.appendChild(li);
                return;
            }

            tickets.forEach(ticket => {
                const li = document.createElement('li');
                li.textContent = `#${ticket.id}: ${ticket.subject}`;
                ul.appendChild(li);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/tickets')
def get_tickets():
    all_tickets = []
    page = 1
    per_page = 100

    while True:
        url = (
            f"https://{FRESHDESK_DOMAIN}.freshdesk.com/api/v2/tickets"
            f"?page={page}&per_page={per_page}&order_by=created_at&order_type=desc"
        )
        print("Requesting:", url)
        response = requests.get(url, auth=HTTPBasicAuth(FRESHDESK_API_KEY, "X"))

        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            return jsonify([]), response.status_code

        tickets = response.json()
        if not tickets:
            break

        # 🔍 Filter on group_id manually in Python
        filtered = [t for t in tickets if t.get("group_id") == DEV_OPS_GROUP_ID]
        all_tickets.extend(filtered)

        page += 1

    return jsonify(all_tickets)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
