import os
import sys

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

import stripe

from core.config import settings

# Override API Key from env if explicitly set (useful if running locally with different key)
# Otherwise uses settings default
if not stripe.api_key:
    stripe.api_key = settings.STRIPE_SECRET_KEY


def seed_stripe():
    print(f"Using Stripe Key: {stripe.api_key[:8]}...")

    products = [
        {
            "name": "Starter",
            "metadata": {"service": "epist.ai", "tier": "starter"},
            "price_amount": 1900,  # $19.00
            "currency": "usd",
            "features": ["20 Hours Transcription", "No API Access", "Email Support"],
        },
        {
            "name": "Pro",
            "metadata": {"service": "epist.ai", "tier": "pro"},
            "price_amount": 4900,  # $49.00
            "currency": "usd",
            "features": ["100 Hours Transcription", "API Access", "Priority Support", "Advanced RAG"],
        },
    ]

    results = {}

    for p_data in products:
        print(f"\nProcessing {p_data['name']}...")

        # Check if Product exists
        # Search by name first (approximate) or metadata if possible
        # Stripe search API is powerful
        try:
            search_result = stripe.Product.search(
                query=f"active:'true' AND name:'{p_data['name']}' AND metadata['service']:'epist.ai'", limit=1
            )
            product = search_result.data[0] if search_result.data else None
        except Exception:
            # Fallback to list if search fails (e.g. test mode limitations or permissions)
            print("  Search failed, falling back to list...")
            all_products = stripe.Product.list(limit=100, active=True)
            product = next((p for p in all_products.data if p.name == p_data["name"]), None)

        if product:
            print(f"  Found existing product: {product.id}")
        else:
            print("  Creating new product...")
            product = stripe.Product.create(
                name=p_data["name"],
                metadata=p_data["metadata"],
                description=f"{p_data['name']} Tier",
            )
            print(f"  Created product: {product.id}")

        # Check for Prices
        prices = stripe.Price.list(product=product.id, active=True, limit=10, type="recurring")

        price = None
        if prices.data:
            # Check if price matches amount
            for existing_price in prices.data:
                if (
                    existing_price.unit_amount == p_data["price_amount"]
                    and existing_price.currency == p_data["currency"]
                    and existing_price.recurring.interval == "month"
                ):
                    price = existing_price
                    print(f"  Found matching price: {price.id}")
                    break

        if not price:
            print("  Creating new price...")
            price = stripe.Price.create(
                product=product.id,
                unit_amount=p_data["price_amount"],
                currency=p_data["currency"],
                recurring={"interval": "month"},
                metadata={"tier": p_data["metadata"]["tier"]},
            )
            print(f"  Created price: {price.id}")

        results[p_data["name"].upper()] = price.id

    print("\n" + "=" * 50)
    print("STRIPE CONFIGURATION COMPLETE")
    print("Add these to your .env file:")
    print(f"STRIPE_PRICE_ID_STARTER={results['STARTER']}")
    print(f"STRIPE_PRICE_ID_PRO={results['PRO']}")
    print("=" * 50)


if __name__ == "__main__":
    try:
        seed_stripe()
    except Exception as e:
        print(f"Error: {e}")
