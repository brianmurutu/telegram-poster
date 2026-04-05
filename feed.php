<?php
// feed.php — Custom RSS Feed for techdaily.buzz
// Place this file in the ROOT of your website (same folder as index.php and .env)
// No credentials are hardcoded — reads from your existing CMS .env file

header('Content-Type: application/rss+xml; charset=UTF-8');

// ── Read DB credentials from .env ────────────────────────────
function get_env(string $key): string {
    $env_path = __DIR__ . '/.env';
    if (!file_exists($env_path)) return '';
    $lines = file($env_path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    foreach ($lines as $line) {
        if (strpos(trim($line), '#') === 0) continue;
        $parts = explode('=', $line, 2);
        if (count($parts) < 2) continue;
        [$k, $v] = $parts;
        if (trim($k) === $key) return trim($v, " \t\n\r\0\x0B\"'");
    }
    return '';
}

$host = get_env('DB_HOST') ?: 'localhost';
$db   = get_env('DB_DATABASE');
$user = get_env('DB_USERNAME');
$pass = get_env('DB_PASSWORD');

try {
    $pdo = new PDO("mysql:host=$host;dbname=$db;charset=utf8mb4", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    // Never expose the real error to the public
    die('<?xml version="1.0"?><error>Feed temporarily unavailable.</error>');
}

// ── Fetch latest 20 published posts ─────────────────────────
$stmt = $pdo->query("
    SELECT id, name, description, updated_at
    FROM posts
    WHERE status = 'published'
    ORDER BY updated_at DESC
    LIMIT 20
");
$posts = $stmt->fetchAll(PDO::FETCH_ASSOC);

// ── Generate URL slug from post name ─────────────────────────
function make_slug(string $name): string {
    $slug = strtolower($name);
    $slug = preg_replace('/[^a-z0-9\s-]/', '', $slug);
    $slug = preg_replace('/[\s-]+/', '-', $slug);
    $slug = trim($slug, '-');
    return $slug;
}

$base = 'https://techdaily.buzz';
?>
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>TechDaily Buzz</title>
    <link><?= $base ?></link>
    <description>Your Daily Pulse on Every Tech Domain</description>
    <language>en-us</language>
    <lastBuildDate><?= date(DATE_RSS) ?></lastBuildDate>
    <atom:link href="<?= $base ?>/feed.php" rel="self" type="application/rss+xml"/>

    <?php foreach ($posts as $post):
        $slug = make_slug($post['name']);
        $link = $base . '/' . $slug;
    ?>
    <item>
      <title><?= htmlspecialchars($post['name'], ENT_XML1, 'UTF-8') ?></title>
      <link><?= htmlspecialchars($link, ENT_XML1, 'UTF-8') ?></link>
      <description><?= htmlspecialchars($post['description'], ENT_XML1, 'UTF-8') ?></description>
      <pubDate><?= date(DATE_RSS, strtotime($post['updated_at'])) ?></pubDate>
      <guid isPermaLink="true"><?= htmlspecialchars($link, ENT_XML1, 'UTF-8') ?></guid>
    </item>
    <?php endforeach; ?>

  </channel>
</rss>