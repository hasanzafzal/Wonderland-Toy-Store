# Promo Code Feature Documentation

## Overview
The Wonderland Toy Store now includes a discount code feature that allows customers to apply promo codes during checkout to receive discounts on their orders.

## Current Valid Promo Codes

### H&Hoff15
- **Discount**: 15% off
- **How to Use**: Enter `H&Hoff15` in the promo code field during checkout and click "Apply"

## Implementation Details

### Database Changes
The `Order` model has been extended with three new columns:
- `promo_code` (String, nullable): Stores the promo code used for the order
- `discount_percentage` (Float): The discount percentage applied (e.g., 15)
- `discount_amount` (Float): The actual dollar amount discounted from the order

### Frontend Features

#### Checkout Page (`app/templates/checkout.html`)
- **Promo Code Section**: New input field to enter promo codes
- **Apply Button**: Validates and applies the promo code in real-time using JavaScript
- **Real-time Discount Calculation**: The order total updates immediately when a valid promo code is applied
- **Success/Error Messages**: User-friendly feedback for valid and invalid promo codes
- **Discount Display**: Shows the discount percentage and amount in the order total sidebar

#### Orders Page (`app/templates/orders.html`)
- **Promo Code Display**: Shows the applied promo code and discount percentage for orders that used one
- **Discount Highlight**: Displays the discount amount with a green background for easy visibility

### Backend Features

#### Promo Code Validation (`app/routes.py`)
Both checkout endpoints (`checkout` and `payment_card` routes) validate promo codes:
1. Converts input to uppercase for case-insensitive matching
2. Checks against valid promo codes dictionary
3. Calculates discount on per-item basis to handle multiple cart items correctly
4. Applies discount to total_price before storing in the database
5. Stores discount details in the order for reference

#### Discount Calculation
- Discount is calculated on the item subtotal (price × quantity)
- Tax is applied to the original subtotal (before discount)
- Final total = (Subtotal - Discount) + Tax

### Data Storage
When an order is placed with a promo code:
- `order.promo_code` = "H&HOFF15"
- `order.discount_percentage` = 15
- `order.discount_amount` = calculated discount in dollars
- `order.total_price` = price after discount

## Adding New Promo Codes

To add new promo codes, edit the `checkout()` function in `/app/routes.py`:

```python
# Validate promo code and calculate discount
promo_discount_percent = 0
if promo_code:
    # Valid promo codes
    valid_promo_codes = {
        'H&Hoff15': 15,
        'SUMMER20': 20,  # Add new promo codes here
        'WELCOME10': 10
    }
```

Also update the JavaScript in `/app/templates/checkout.html`:

```javascript
const VALID_PROMO_CODES = {
    'H&Hoff15': 15,
    'SUMMER20': 20,
    'WELCOME10': 10
};
```

## Testing the Feature

### Manual Testing

1. **Apply Valid Promo Code**:
   - Go to checkout
   - Enter "H&Hoff15" in the promo code field
   - Click "Apply"
   - Verify success message appears
   - Verify discount is calculated correctly
   - Complete checkout

2. **Apply Invalid Promo Code**:
   - Go to checkout
   - Enter an invalid code (e.g., "INVALID123")
   - Click "Apply"
   - Verify error message appears

3. **View Discounted Order**:
   - Go to "My Orders"
   - Find the order with promo code applied
   - Verify promo code, discount percentage, and discount amount are displayed

### Database Schema
```sql
-- New columns added to orders table:
ALTER TABLE orders ADD COLUMN promo_code VARCHAR(50);
ALTER TABLE orders ADD COLUMN discount_percentage FLOAT DEFAULT 0;
ALTER TABLE orders ADD COLUMN discount_amount FLOAT DEFAULT 0;
```

## Security Considerations

- Promo codes are validated server-side (in routes.py), not just client-side
- Case-insensitive matching prevents users from bypassing validation
- Discount is calculated for each item individually to prevent abuse with multiple quantities
- Order history maintains accurate discount records for auditing

## Future Enhancements

Possible improvements:
- Expiration dates for promo codes
- Usage limits per code or per user
- Promo codes with specific categories or products
- Dynamic promo code management via admin dashboard
- Promo code analytics (usage count, revenue impact)
- Tiered discounts based on cart value
