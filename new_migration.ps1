
# List of apps in correct dependency order
$apps = @(
    "brand",
    "category",
    "product",
    "user",
    "order",
    "cart",
    "wishlist",
    "payment",
    "review",
    "ip_block",
    "fraud_api",
    "contact",
    "shipping_charge",
    "site_setting",
    "banner",
    "earning"
)

Write-Host "Cleaning up old migrations and __pycache__..."

foreach ($app in $apps) {
    Write-Host "Cleaning $app..."

    $migrationsPath = Join-Path $app "migrations"

    # Delete migration files except __init__.py
    if (Test-Path $migrationsPath) {
        Get-ChildItem -Path $migrationsPath -File | Where-Object { $_.Name -ne "__init__.py" } | Remove-Item -Force
    }

    # Delete all __pycache__ directories under this app
    Get-ChildItem -Path $app -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
}

Write-Host "Making fresh migrations..."
python manage.py makemigrations $apps

Write-Host "Applying migrations..."
python manage.py migrate

Write-Host "✅ Migration reset completed successfully."
