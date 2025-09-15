# # reset-django.ps1
# Write-Host "🗑 Step 0: Deleting SQLite database..."
# Remove-Item "$PSScriptRoot\db.sqlite3" -Force -ErrorAction SilentlyContinue

# Write-Host "🗑 Step 1: Deleting all __pycache__ folders..."
# Get-ChildItem -Path $PSScriptRoot -Recurse -Directory -Filter "__pycache__" | ForEach-Object {
#     Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
# }

# Write-Host "🗑 Step 2: Deleting all migrations folders..."
# Get-ChildItem -Path $PSScriptRoot -Recurse -Directory -Filter "migrations" | ForEach-Object {
#     # Keep __init__.py if you want
#     Remove-Item "$($_.FullName)\*" -Recurse -Force -ErrorAction SilentlyContinue
# }

# Write-Host "⚙️ Step 3: Running makemigrations for all apps..."
# $apps = @("user", "banner","user", "category","brand","product", "order", "cart","payment","review","contact", "earning", "fraud_api", "ip_block",   "shipping_charge", "site_setting", "smtp_mail", "wishlist","appForSellerSupplier/sellerSupplierBrand","appForSellerSupplier/sellerSupplierCateogory", "appForSellerSupplier/sellerSupplierOrder", "apForSellerSupplierProduct" )

# foreach ($app in $apps) {
#     Write-Host "  -> makemigrations $app"
#     python manage.py makemigrations $app
# }

# Write-Host "⚙️ Step 4: Applying migrations..."
# python manage.py migrate

# Write-Host "👤 Step 5: (Optional) Create a superuser..."
# # Uncomment next line if you always want a fresh superuser
# # python manage.py createsuperuser

# Write-Host "✅ Done! Fresh DB + migrations ready."



# reset-django.ps1
Write-Host "🗑 Step 0: Deleting SQLite database..."
Remove-Item "$PSScriptRoot\db.sqlite3" -Force -ErrorAction SilentlyContinue

Write-Host "🗑 Step 1: Deleting all __pycache__ folders..."
Get-ChildItem -Path $PSScriptRoot -Recurse -Directory -Filter "__pycache__" | ForEach-Object {
    Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "🗑 Step 2: Cleaning migrations folders..."
Get-ChildItem -Path $PSScriptRoot -Recurse -Directory -Filter "migrations" | ForEach-Object {
    # Keep only __init__.py in each migrations folder
    Get-ChildItem $_.FullName -Exclude "__init__.py" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "⚙️ Step 3: Running makemigrations for all apps..."
# Fixed app list - removed duplicates and corrected typos
$apps = @(
    "user", "banner", "category", "brand", "product", "order", "cart", 
    "payment", "review", "contact", "earning", "fraud_api", "ip_block", 
    "shipping_charge", "site_setting", "smtp_mail", "wishlist","order_tracking_link",
    "sellerSupplierBrand", 
    "sellerSupplierCategory", 
    "sellerSupplierOrder", 
    "sellerSupplierProduct",
    "seller_supplier_order_unique"
)

foreach ($app in $apps) {
    Write-Host "  -> makemigrations $app"
    python manage.py makemigrations $app
}

Write-Host "⚙️ Step 4: Applying migrations..."
python manage.py migrate
