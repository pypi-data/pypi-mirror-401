import os
import sys

import stripe
from dotenv import load_dotenv

load_dotenv()

stripe_key = os.getenv("STRIPE_SECRET_KEY")
price_id = os.getenv("STRIPE_PRICE_ID_PRO")

if not stripe_key:
    print("❌ STRIPE_SECRET_KEY not set")
    sys.exit(1)
if not price_id:
    print("❌ STRIPE_PRICE_ID_PRO not set")
    sys.exit(1)

print(f"Testing Stripe with Key: {stripe_key[:8]}...")
print(f"Testing Price ID: {price_id}")

stripe.api_key = stripe_key

try:
    price = stripe.Price.retrieve(price_id)
    print("✅ Price found!")
    print(f"Product: {price.product}")
    print(f"Unit Amount: {price.unit_amount}")
    print(f"Currency: {price.currency}")
except Exception as e:
    print(f"❌ Error retrieving price: {e}")
