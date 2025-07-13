from flask import Flask, request, jsonify,render_template_string
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

FRESHDESK_DOMAIN = "netcore.freshdesk.com"
API_KEY = "gYzoEaF1pREcMlNji6"

HTML = """
<!DOCTYPE html>
<html>
    <title>Freshdesk Dev Ops Tickets</title>
</head>
<body>
<h2>Search Freshdesk Tickets</h2>
<input type="text" id="searchBox" placeholder="Search Freshdesk tickets">
<button onclick="searchTickets()">Search</button>
<div id="results"></div>
<script>
    function searchTickets() {
    const query = document.getElementById("searchBox").value;
    fetch('/search?query=' + encodeURIComponent(query))
        .then(res => res.json())
        .then(data => {
            let html = '';
            data.results.forEach(ticket => {
                html += `<p><b>${ticket.subject}</b> (#${ticket.id})</p>`;
            });
            document.getElementById("results").innerHTML = html;
        });
}
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/search')
def search():
    user_query = request.args.get("query")
    if not user_query:
        return jsonify({"error": "Query parameter is missing."}), 400

    # Construct the Freshdesk search API URL
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/search/tickets?query=\"{user_query}\""

    try:
        response = requests.get(url, auth=HTTPBasicAuth(API_KEY, "X"))

        if response.status_code == 200:
            return jsonify({"results": response.json().get("results", [])})
        else:
            return jsonify({"error": response.json(), "status": response.status_code}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=8001, debug=True)

