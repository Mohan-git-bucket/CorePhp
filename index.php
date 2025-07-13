<?php
$api_key = "gYzoEaF1pREcMlNji6";
$domain = "netcore.freshdesk.com";

$search_query = isset($_GET['q']) ? trim($_GET['q']) : '';

$url = "https://$domain/api/v2/tickets?page=1&per_page=100";

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_USERPWD, "$api_key:X");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

$tickets = [];
if ($http_code === 200) {
    $tickets = json_decode($response, true);
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Freshdesk Ticket Search</title>
</head>
<body>
    <h2>Freshdesk Ticket Search</h2>
    <form method="get">
        <input type="text" name="q" placeholder="Enter keyword..." value="<?php echo htmlspecialchars($search_query); ?>" required>
        <button type="submit">Search</button>
    </form>

    <?php if ($search_query !== ""): ?>
        <h3>Results for "<?php echo htmlspecialchars($search_query); ?>"</h3>
        <?php
$found = false;
foreach ($tickets as $ticket) {
    if (isset($ticket['subject'])) {
        $subject = strtolower($ticket['subject']);
        $all_words_found = true;
        foreach (explode(' ', strtolower($search_query)) as $word) {
            if (strpos($subject, $word) === false) {
                $all_words_found = false;
                break;
            }
        }
        if ($all_words_found) {
            echo "<strong>#{$ticket['id']} - {$ticket['subject']}</strong><br>";
            $found = true;
        }
    }
}
if (!$found) {
    echo "No matching tickets found.";
}
        ?>
    <?php endif; ?>
</body>
</html>
