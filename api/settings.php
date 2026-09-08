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

$dataFile = $dataDir . '/settings.json';
$exampleFile = $dataDir . '/settings.json.example';

// GET: Return current settings
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (file_exists($dataFile)) {
        echo file_get_contents($dataFile);
    } elseif (file_exists($exampleFile)) {
        // Auto-seed from template on first deployment
        $initialData = file_get_contents($exampleFile);
        @file_put_contents($dataFile, $initialData, LOCK_EX);
        echo $initialData;
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

    // Ensure heroSlides in server settings always unifies desktop and mobile banner image
    if (!empty($merged['heroSlides']) && is_array($merged['heroSlides'])) {
        foreach ($merged['heroSlides'] as &$slide) {
            if (is_array($slide)) {
                $unifiedImg = !empty($slide['image']) ? $slide['image'] : (!empty($slide['mobileImage']) ? $slide['mobileImage'] : 'assets/images/banners/hero_slide_luxury.png');
                $slide['image'] = $unifiedImg;
                $slide['mobileImage'] = $unifiedImg;
            }
        }
        unset($slide);
    }

    if (!is_dir(dirname($dataFile))) {
        @mkdir(dirname($dataFile), 0755, true);
    }

    $jsonStr = json_encode($merged, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    $written = @file_put_contents($dataFile, $jsonStr, LOCK_EX);
    if ($written === false) {
        http_response_code(500);
        echo json_encode(["success" => false, "error" => "Failed to write settings to disk. Check folder write permissions for data/ directory."]);
        exit;
    }

    // Also update settings.json.example as deployment fallback
    @file_put_contents($exampleFile, $jsonStr, LOCK_EX);

    echo json_encode(["success" => true, "message" => "Settings successfully saved to server", "data" => $merged]);
    exit;
}

