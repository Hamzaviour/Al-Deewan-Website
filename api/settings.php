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

$dataFile = __DIR__ . '/../data/settings.json';

// GET: Return current settings
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (file_exists($dataFile)) {
        echo file_get_contents($dataFile);
    } else {
        echo json_encode(["status" => "empty"]);
    }
    exit;
}

// POST: Save updated settings
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $rawInput = file_get_contents('php://input');
    $data = json_decode($rawInput, true);

    if (!is_array($data)) {
        http_response_code(400);
        echo json_encode(["success" => false, "error" => "Invalid JSON payload"]);
        exit;
    }

    // Authentication check
    $authPasscode = $_SERVER['HTTP_X_ADMIN_PASSCODE'] ?? ($data['adminPasscode'] ?? '');
    
    // Check passcode against data/settings.json or default 'deewan2026'
    $validPasscode = 'deewan2026';
    if (file_exists($dataFile)) {
        $currSettings = json_decode(file_get_contents($dataFile), true);
        if (!empty($currSettings['adminPassword'])) {
            $validPasscode = $currSettings['adminPassword'];
        }
    }

    if ($authPasscode !== $validPasscode && $authPasscode !== 'deewan2026') {
        http_response_code(401);
        echo json_encode(["success" => false, "error" => "Unauthorized: Invalid admin passcode"]);
        exit;
    }

    // Remove adminPasscode before saving
    unset($data['adminPasscode']);

    // Merge with existing settings
    $merged = [];
    if (file_exists($dataFile)) {
        $existing = json_decode(file_get_contents($dataFile), true);
        if (is_array($existing)) {
            $merged = $existing;
        }
    }

    foreach ($data as $key => $val) {
        $merged[$key] = $val;
    }

    if (!is_dir(dirname($dataFile))) {
        mkdir(dirname($dataFile), 0755, true);
    }

    file_put_contents($dataFile, json_encode($merged, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    echo json_encode(["success" => true, "message" => "Settings successfully saved to server", "data" => $merged]);
    exit;
}
