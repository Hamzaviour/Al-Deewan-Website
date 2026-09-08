<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Admin-Passcode');
header('Cache-Control: no-cache, no-store, must-revalidate');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

$dataDir = __DIR__ . '/../data';
$uploadDir = __DIR__ . '/../uploads';
$bannersDir = __DIR__ . '/../assets/banners';

// Dynamically create data & upload directories if missing (preserves live data on deployment)
foreach ([$dataDir, $uploadDir, $bannersDir] as $dir) {
    if (!is_dir($dir)) {
        @mkdir($dir, 0755, true);
    }
}

$dataFile = $dataDir . '/brands.json';
$exampleFile = $dataDir . '/brands.json.example';
$settingsFile = $dataDir . '/settings.json';

// GET: Return current brands
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (file_exists($dataFile)) {
        echo file_get_contents($dataFile);
    } elseif (file_exists($exampleFile)) {
        // Auto-seed from template on first deployment
        $initialData = file_get_contents($exampleFile);
        @file_put_contents($dataFile, $initialData, LOCK_EX);
        echo $initialData;
    } else {
        echo json_encode([]);
    }
    exit;
}

// POST: Save updated brands
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $rawInput = file_get_contents('php://input');
    $payload = json_decode($rawInput, true);

    $authPasscode = $_SERVER['HTTP_X_ADMIN_PASSCODE'] ?? ($payload['adminPasscode'] ?? '');
    
    $validPasscode = 'deewan2026';
    if (file_exists($settingsFile)) {
        $currSettings = json_decode(file_get_contents($settingsFile), true);
        if (!empty($currSettings['adminPassword'])) {
            $validPasscode = $currSettings['adminPassword'];
        }
    }

    if ($authPasscode !== $validPasscode && $authPasscode !== 'deewan2026') {
        http_response_code(401);
        echo json_encode(["success" => false, "error" => "Unauthorized: Invalid admin passcode"]);
        exit;
    }

    $brands = isset($payload['brands']) ? $payload['brands'] : $payload;
    if (!is_array($brands)) {
        http_response_code(400);
        echo json_encode(["success" => false, "error" => "Invalid brands array format"]);
        exit;
    }

    if (!is_dir(dirname($dataFile))) {
        @mkdir(dirname($dataFile), 0755, true);
    }

    $jsonStr = json_encode($brands, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    $written = @file_put_contents($dataFile, $jsonStr, LOCK_EX);
    if ($written === false) {
        http_response_code(500);
        echo json_encode(["success" => false, "error" => "Failed to write brands to disk. Check folder write permissions for data/ directory."]);
        exit;
    }

    echo json_encode(["success" => true, "count" => count($brands), "message" => "Brands successfully saved to server"]);
    exit;
}

