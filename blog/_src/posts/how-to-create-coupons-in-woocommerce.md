---
title: "How to Create Coupons in WooCommerce: A Practical Guide"
seo_title: "Create Coupons in WooCommerce Guide"
short_title: "WooCommerce Coupons"
description: "Learn how to create coupons in WooCommerce to run discounts, offer free shipping, and drive online sales step by step."
dek: "I'll walk you through setting up discount codes, percentage offers, and free shipping coupons in WooCommerce without any code."
slug: "how-to-create-coupons-in-woocommerce"
date: 2026-11-26
updated: 2026-11-26
author: "Salman Ali Rafeeq"
category: "E-commerce"
tags: ["WooCommerce", "Discounts", "E-commerce", "Store Management"]
keywords: ["create coupons in woocommerce", "woocommerce discount codes", "how to add coupon in woocommerce", "woocommerce coupon settings", "woocommerce free shipping coupon", "woocommerce coupon usage limits"]
draft: false
generated_by: "gemini/gemini-3.5-flash"
---

Running promotions and discount codes is a reliable way to boost sales, clear out inventory, or reward loyal customers. When you build your store on [WordPress](https://wordpress.org/), learning how to **create coupons in WooCommerce** allows you to launch special offers without buying extra add-ons or complex plugins because the core software includes a discount system out of the box.

In this practical guide, I will walk you through enabling the discount system, creating new codes, setting spend limits, and testing your setup before launching your next store promotion.

## Enable Coupon Management in WooCommerce Settings

Before you can create your first code, you must make sure coupon functionality is turned on in your settings. On most fresh installations, WooCommerce enables coupons by default. However, if you imported sample data or adjusted your store settings earlier, the feature might be turned off.

To verify your settings:

1. Log into your WordPress admin dashboard.
2. Navigate to **WooCommerce > Settings** in the left menu.
3. Make sure you are on the **General** tab.
4. Scroll down to the **Enable coupons** section.
5. Check the box next to **Enable the use of coupon codes**.

While you are on this screen, you will also see an option called **Calculate coupon discounts sequentially**. Leave this unchecked unless you specifically want WooCommerce to apply multiple coupons one after another on the discounted subtotal rather than the original price. Click **Save changes** at the bottom of the page if you made any updates.

If you are still setting up your store, make sure you also configure your [WooCommerce payment gateways](../set-up-woocommerce-payment-gateways/) so customers can complete their purchases when applying discounts.

## How to Add a New Coupon Code in WooCommerce

Once the feature is enabled, managing your store's codes takes place inside the marketing menu. 

1. Go to **Marketing > Coupons** in your WordPress dashboard.
2. Click the **Add Coupon** button at the top of the page.
3. In the **Coupon code** box, enter the exact text customers will type at checkout (for example, `SAVE10` or `SUMMER`).
4. In the **Description** box, add a short note explaining what the coupon is for. Customers will not see this text; it is strictly for you and your staff.

:::callout Tip
Keep coupon codes simple, short, and easy to spell. Avoid confusing characters like uppercase `O` and the number `0` to prevent typos when buyers type their code at checkout.
:::

After adding the code and description, scroll down to the **Coupon data** panel beneath the text editor. This panel controls how the code behaves.

> Simple, clear coupon codes reduce checkout friction and help prevent abandoned shopping carts.

## Setting Up Discount Types and Values

The **General** tab inside the Coupon data panel controls how much money the customer saves and whether the code grants extra benefits like free delivery.

Under **Discount type**, WooCommerce gives you three core choices:

| Discount Type | How It Calculates Savings | Best Used For |
|---|---|---|
| **Percentage discount** | Deducts a set percentage from the eligible cart subtotal. | Storewide sales, seasonal events, or email sign-up incentives. |
| **Fixed cart discount** | Deducts a flat cash amount from the total cart value. | Encouraging higher cart totals by granting a fixed savings amount. |
| **Fixed product discount** | Deducts a flat cash amount from specific items only. | Clearing specific inventory or promoting individual [WooCommerce products](../how-to-add-products-in-woocommerce/). |

Enter your desired numerical value into the **Coupon amount** field. If you chose a percentage discount, entering a number like `20` applies a twenty-percent discount to eligible items. If you chose a fixed cart discount, entering `20` deducts twenty currency units (such as $20) from the order total.

### Configuring Free Shipping

If you want to grant free delivery using a promo code, check the box labeled **Allow free shipping**. 

Keep in mind that enabling this setting requires you to configure a free shipping requirement inside your store settings:

1. Navigate to **WooCommerce > Settings > Shipping**.
2. Edit the shipping zone where you offer free shipping.
3. Add or edit a **Free Shipping** method.
4. Set the requirement dropdown to **A valid free shipping coupon**.

If you need help setting up shipping zones and rates, read my guide on [WooCommerce shipping setup](../woocommerce-shipping-setup/).

Finally, set an **Expiry date** using the calendar picker if your offer has a deadline. Once the date passes, WooCommerce automatically stops accepting the code.

## Restricting Coupon Usage and Setting Limits

To protect your business profit margins, you should set clear rules regarding who can use your codes and how often they can be redeemed.

### Usage Restrictions

Click on the **Usage restriction** tab inside the Coupon data box to define basic rules:

* **Minimum spend:** The minimum subtotal required before the coupon becomes active (for example, spend at least $50).
* **Maximum spend:** The upper spending threshold beyond which the coupon cannot be used.
* **Individual use only:** Check this box if you do not want shoppers to stack this code with other promotional offers.
* **Exclude sale items:** Check this box to prevent the coupon from applying to products already listed on sale.
* **Products / Exclude products:** Search for specific items to include or exclude from the promotion.
* **Product categories / Exclude categories:** Limit the discount to whole categories (such as apparel or accessories).
* **Allowed emails:** Enter specific customer email addresses to restrict the code to those individual buyers.

### Usage Limits

Click on the **Usage limits** tab to manage how many times the code can be redeemed:

* **Usage limit per coupon:** Controls how many times the coupon can be redeemed across your entire store before it expires (for example, limiting a deal to the first 100 shoppers).
* **Limit usage to X items:** Applies fixed product discounts to a maximum number of eligible items per cart.
* **Usage limit per user:** Restricts how many times an individual logged-in customer or guest email address can use the code (usually set to `1` for single-use promotions).

:::callout Watch out
Always test combinations of restrictions. If you set a minimum spend threshold higher than your store's average item price, make sure customers can realistically hit that total with standard orders.
:::

## Testing and Troubleshooting Your Coupon Codes

After you set up a code, always test it yourself before sending promotional emails or launching advertising campaigns.

### Step-by-Step Coupon Test

1. Open a new private or incognito web browser window.
2. Visit your online store and add eligible items to your shopping cart.
3. Proceed to the cart or checkout page.
4. Type your code into the coupon field and click **Apply coupon**.
5. Verify that the order subtotal updates correctly and that shipping fees drop to zero if you configured free delivery.

If the coupon fails to apply, check these common issues:

* **Typographical errors:** Ensure the code entered matches the exact text in your admin panel.
* **Cart minimums not met:** Verify that the test cart total meets any minimum spend requirements before taxes and shipping.
* **Category exclusions:** Ensure the items in your cart belong to allowed categories.
* **Time zone settings:** Check that your WordPress time zone matches your local area so codes do not expire early.

Once your codes work reliably, you can integrate them into your marketing workflows. For instance, offering a discount code is an effective tactic when you [automate abandoned cart emails](../automate-abandoned-cart-emails/) to bring back shoppers who left without paying. You can also send welcome discounts through [email marketing automation](../email-marketing-automation-small-business/).

## Frequently asked questions {#faq data-toc-label="FAQ"}

### Can I give customers automatic discounts without them entering a code?
Core WooCommerce requires customers to type or paste a code at checkout. If you want discounts to apply automatically based on cart contents or user roles, you will need a dedicated dynamic pricing extension from the plugin repository.

### What happens if a customer uses a coupon on an order they later refund?
When you process a partial or full refund inside WooCommerce, the system calculates the refund based on the net price paid after applying the discount. The original coupon usage counter does not automatically reset for that customer unless you manually edit or delete their order.

### How do I offer free shipping on orders over a certain amount without requiring a code?
You can set up minimum order amounts directly inside your shipping zone settings (**WooCommerce > Settings > Shipping**). Edit your Free Shipping method and set the requirement dropdown to require a minimum order amount instead of a coupon code.

---

Setting up clear promotions is a key part of running a store, but keeping your site secure, fast, and properly configured requires ongoing attention. If you need help tailoring your WooCommerce settings, fixing checkout issues, or building custom store features, feel free to review my past work on my [portfolio](../../#work) or [get in touch](../../#contact) to discuss your project.
