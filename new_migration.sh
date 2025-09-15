#!/bin/bash

# Use the labels Django actually recognizes
apps=(
    "user"
    "brand"
    "category"
    "product"
    "order"
    "cart"
    "wishlist"
    "payment"
    "review"
    "ip_block"
    "fraud_api"
    "contact"
    "shipping_charge"
    "site_setting"
    "banner"
    "earning"
    "sellerSupplierBrand"
    "sellerSupplierCategory"
    "sellerSupplierProduct"
    "sellerSupplierOrder"
)

echo "🧹 Cleaning up old migrations and __pycache__..."

for app in "${apps[@]}"; do
    echo "🔸 Cleaning $app..."

    # Try both possible locations for the app folder
    if [ -d "$app" ]; then
        app_path="$app"
    elif [ -d "appForSellerSupplier/$app" ]; then
        app_path="appForSellerSupplier/$app"
    else
        echo "⚠️ Warning: Could not find folder for '$app'"
        continue
    fi

    # Clean migrations
    if [ -d "$app_path/migrations" ]; then
        find "$app_path/migrations" -type f ! -name '__init__.py' -delete
    fi

    # Clean __pycache__
    find "$app_path" -type d -name '__pycache__' -exec rm -rf {} +
done

echo "📦 Making fresh migrations..."
if ! python3 manage.py makemigrations "${apps[@]}"; then
    echo "❌ makemigrations failed. Check the errors above."
    exit 1
fi

echo "📥 Applying migrations..."
if ! python3 manage.py migrate; then
    echo "❌ migrate failed. Check the errors above."
    exit 1
fi

echo "✅ Migration reset completed successfully."
