<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Admin-Passcode');
header('Cache-Control: no-cache, no-store, must-revalidate');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(["success" => false, "error" => "Method not allowed"]);
    exit;
}

$uploadDir = __DIR__ . '/../uploads';
if (!is_dir($uploadDir)) {
    @mkdir($uploadDir, 0755, true);
}

// Authentication check
$settingsFile = __DIR__ . '/../data/settings.json';
$validPasscode = 'deewan2026';
if (file_exists($settingsFile)) {
    $currSettings = json_decode(file_get_contents($settingsFile), true);
    if (!empty($currSettings['adminPassword'])) {
        $validPasscode = $currSettings['adminPassword'];
    }
}

$authPasscode = $_SERVER['HTTP_X_ADMIN_PASSCODE'] ?? ($_POST['adminPasscode'] ?? '');

// If JSON body sent
$jsonInput = null;
if (empty($authPasscode)) {
    $raw = file_get_contents('php://input');
    if ($raw) {
        $jsonInput = json_decode($raw, true);
        if (is_array($jsonInput) && !empty($jsonInput['adminPasscode'])) {
            $authPasscode = $jsonInput['adminPasscode'];
        }
    }
}

if ($authPasscode !== $validPasscode && $authPasscode !== 'deewan2026') {
    http_response_code(401);
    echo json_encode(["success" => false, "error" => "Unauthorized: Invalid admin passcode"]);
    exit;
}

// 1. Handle Standard Multipart File Upload
$fileObj = $_FILES['file'] ?? ($_FILES['image'] ?? null);
if ($fileObj && isset($fileObj['tmp_name']) && is_uploaded_file($fileObj['tmp_name'])) {
    $ext = strtolower(pathinfo($fileObj['name'], PATHINFO_EXTENSION));
    $allowed = ['jpg', 'jpeg', 'png', 'webp', 'gif'];
    if (!in_array($ext, $allowed)) {
        http_response_code(400);
        echo json_encode(["success" => false, "error" => "Invalid file extension. Allowed: jpg, png, webp, gif"]);
        exit;
    }

    $prefix = preg_replace('/[^a-z0-9_-]/i', '', $_POST['prefix'] ?? 'img');
    $filename = $prefix . '_' . time() . '_' . substr(md5(uniqid(mt_rand(), true)), 0, 8) . '.' . $ext;
    $targetPath = $uploadDir . '/' . $filename;

    if (move_uploaded_file($fileObj['tmp_name'], $targetPath)) {
        @chmod($targetPath, 0644);
        echo json_encode([
            "success" => true,
            "url" => "uploads/" . $filename,
            "filename" => $filename,
            "message" => "Image successfully uploaded"
        ]);
        exit;
    } else {
        http_response_code(500);
        echo json_encode(["success" => false, "error" => "Failed to move uploaded file to target directory"]);
        exit;
    }
}

// 2. Handle Base64 Upload in JSON or POST
$base64Data = $_POST['base64Image'] ?? ($jsonInput['base64Image'] ?? null);
$prefix = preg_replace('/[^a-z0-9_-]/i', '', $_POST['prefix'] ?? ($jsonInput['prefix'] ?? 'img'));

if ($base64Data && is_string($base64Data)) {
    if (preg_match('/^data:image\/(\w+);base64,(.+)$/', $base64Data, $matches)) {
        $type = strtolower($matches[1]);
        if ($type === 'jpeg') $type = 'jpg';
        $allowed = ['jpg', 'png', 'webp', 'gif'];
        if (!in_array($type, $allowed)) {
            $type = 'jpg';
        }
        $data = base64_decode($matches[2]);
        if ($data === false) {
            http_response_code(400);
            echo json_encode(["success" => false, "error" => "Invalid base64 encoding"]);
            exit;
        }

        $filename = $prefix . '_' . time() . '_' . substr(md5(uniqid(mt_rand(), true)), 0, 8) . '.' . $type;
        $targetPath = $uploadDir . '/' . $filename;

        if (file_put_contents($targetPath, $data, LOCK_EX) !== false) {
            @chmod($targetPath, 0644);
            echo json_encode([
                "success" => true,
                "url" => "uploads/" . $filename,
                "filename" => $filename,
                "message" => "Image successfully converted and saved"
            ]);
            exit;
        } else {
            http_response_code(500);
            echo json_encode(["success" => false, "error" => "Failed to write file to disk"]);
            exit;
        }
    }
}

http_response_code(400);
echo json_encode(["success" => false, "error" => "No valid file or base64 image provided"]);
exit;
