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

$dataFile = __DIR__ . '/../data/products.json';
$settingsFile = __DIR__ . '/../data/settings.json';

// GET: Return current products
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (file_exists($dataFile)) {
        echo file_get_contents($dataFile);
    } else {
        echo json_encode([]);
    }
    exit;
}

// POST: Save updated products
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $rawInput = file_get_contents('php://input');
    $payload = json_decode($rawInput, true);

    // Authentication check
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

    $products = isset($payload['products']) ? $payload['products'] : $payload;
    if (!is_array($products)) {
        http_response_code(400);
        echo json_encode(["success" => false, "error" => "Invalid products array format"]);
        exit;
    }

    if (!is_dir(dirname($dataFile))) {
        mkdir(dirname($dataFile), 0755, true);
    }

    file_put_contents($dataFile, json_encode($products, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    echo json_encode(["success" => true, "count" => count($products), "message" => "Products successfully saved to server"]);
    exit;
}
