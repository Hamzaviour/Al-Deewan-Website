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
$bannersDir = __DIR__ . '/../assets/images/banners';

// Dynamically create data & upload directories if missing (preserves live data on deployment)
foreach ([$dataDir, $uploadDir, $bannersDir] as $dir) {
    if (!is_dir($dir)) {
        @mkdir($dir, 0755, true);
    }
}

$dataFile = $dataDir . '/settings.json';
$exampleFile = $dataDir . '/settings.json.example';

// Helper to extract base64 images to file and unify mobile & desktop image URLs
function processHeroSlidesClean(&$settingsObj, $uploadDir, $bannersDir) {
    $modified = false;
    if (!empty($settingsObj['heroSlides']) && is_array($settingsObj['heroSlides'])) {
        foreach ($settingsObj['heroSlides'] as &$slide) {
            if (is_array($slide)) {
                $img = !empty($slide['image']) ? $slide['image'] : (!empty($slide['mobileImage']) ? $slide['mobileImage'] : 'assets/images/banners/hero_slide_3.jpg');
                if (strpos($img, 'data:image/') === 0) {
                    if (preg_match('/^data:image\/(\w+);base64,(.+)$/s', $img, $matches)) {
                        $ext = strtolower($matches[1]);
                        if ($ext === 'jpeg') $ext = 'jpg';
                        $imgData = base64_decode($matches[2]);
                        if ($imgData !== false) {
                            $slideId = !empty($slide['id']) ? $slide['id'] : uniqid();
                            $fileName = 'hero_slide_' . $slideId . '.' . $ext;
                            $saved = false;
                            if (is_dir($bannersDir) && @file_put_contents($bannersDir . '/' . $fileName, $imgData, LOCK_EX)) {
                                $img = 'assets/images/banners/' . $fileName;
                                $saved = true;
                            } elseif (@file_put_contents($uploadDir . '/' . $fileName, $imgData, LOCK_EX)) {
                                $img = 'uploads/' . $fileName;
                                $saved = true;
                            }
                            if ($saved) {
                                $modified = true;
                            }
                        }
                    }
                }
                $slide['image'] = $img;
                $slide['mobileImage'] = $img;
            }
        }
        unset($slide);
    }
    return $modified;
}

// GET: Return current settings
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (file_exists($dataFile)) {
        $raw = file_get_contents($dataFile);
        $curr = json_decode($raw, true);
        if (is_array($curr)) {
            $changed = processHeroSlidesClean($curr, $uploadDir, $bannersDir);
            if ($changed) {
                $cleanJson = json_encode($curr, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
                @file_put_contents($dataFile, $cleanJson, LOCK_EX);
                @file_put_contents($exampleFile, $cleanJson, LOCK_EX);
            }
            echo json_encode($curr, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
            exit;
        }
        echo $raw;
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

    // Automatically convert any base64 slide images to files and unify mobileImage & image
    processHeroSlidesClean($merged, $uploadDir, $bannersDir);

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

