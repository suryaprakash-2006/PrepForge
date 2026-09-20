$BASE_URL="http://127.0.0.1:8003/api/v1"

function Register-User($email) {
    $body = @{name="Test User Planner"; email=$email; password="password123"} | ConvertTo-Json
    Invoke-RestMethod -Method POST -Uri "$BASE_URL/auth/register" -Body $body -ContentType "application/json" -ErrorAction SilentlyContinue | Out-Null
}

function Login-User($email) {
    $body = @{email=$email; password="password123"} | ConvertTo-Json
    $res = Invoke-RestMethod -Method POST -Uri "$BASE_URL/auth/login" -Body $body -ContentType "application/json"
    return $res.access_token
}

echo "1. Registering Users..."
Register-User "user_a@example.com"
Register-User "user_b@example.com"

$tokenA = Login-User "user_a@example.com"
$headersA = @{Authorization="Bearer $tokenA"}

$tokenB = Login-User "user_b@example.com"
$headersB = @{Authorization="Bearer $tokenB"}

echo "2. Initializing User A roadmap (Migration)..."
Invoke-RestMethod -Method POST -Uri "$BASE_URL/weeks/initialize" -Headers $headersA | Out-Null
Invoke-RestMethod -Method POST -Uri "$BASE_URL/weeks/initialize" -Headers $headersB | Out-Null

echo "3. User A completing task wk1_task1..."
$tasksA = Invoke-RestMethod -Method GET -Uri "$BASE_URL/tasks" -Headers $headersA
$firstTaskId = $tasksA[0].id
$body = @{completed=$true} | ConvertTo-Json
Invoke-RestMethod -Method PATCH -Uri "$BASE_URL/tasks/$firstTaskId" -Body $body -ContentType "application/json" -Headers $headersA | Out-Null

echo "4. User B checks task wk1_task1..."
$tasksB = Invoke-RestMethod -Method GET -Uri "$BASE_URL/tasks" -Headers $headersB
$firstTaskB = $tasksB[0]
echo "User B Task 1 Completed: $($firstTaskB.completed) (Expected: False)"

echo "5. Verifying DB..."
