---
title: "How to Redirect URLs Properly: A Simple Guide for Small Business"
seo_title: "How to Redirect URLs Properly"
short_title: "URL Redirects"
description: "Learn how to redirect URLs properly when changing links or updating your small business website to protect your search rankings and keep visitors happy."
dek: "Discover how to set up URL redirects correctly so you never lose visitors or search rankings when moving or changing pages on your website."
slug: "how-to-redirect-urls-properly"
date: 2026-11-16
updated: 2026-11-16
author: "Salman Ali Rafeeq"
category: "SEO"
tags: ["SEO", "Web Management", "Technical SEO"]
keywords: ["how to redirect URLs properly", "URL redirects for SEO", "301 redirects small business", "how to fix broken links", "redirect pages WordPress Shopify", "website redirection guide"]
draft: false
generated_by: "gemini/gemini-flash-lite-latest"
---

When you change a web page address, delete an old product, or redesign your site, visitors and search engines can easily end up on a broken page. Knowing how to redirect URLs properly ensures that people and search engines automatically land on the right place instead of hitting an error message. This website redirection guide covers everything you need to keep your traffic flowing and your search rankings intact.

## Why proper URL redirects matter for your website

Every page on your website has a specific address, and over time, these addresses often change. You might shorten a URL for readability, remove a discontinued product, or move your entire store to a new platform like [Shopify](https://www.shopify.com/) or [WordPress](https://wordpress.org/). 

When a user clicks an old link from a bookmark, a social media post, or an external website, they expect to find your content. If that page is gone without a redirect, they see a frustrating error page and leave your site immediately. 

> A broken link is a dead end that wastes your marketing efforts and frustrates potential customers.

Implementing proper URL redirects for SEO is just as important for search engines. Search engines index your pages and build trust in your content over time. When you point an old URL to a new one correctly, you pass that built-up authority and ranking power to the new page. If you ignore this step, you will lose your hard-earned search rankings whenever you update your site structure. For a broader look at technical foundations, you can also review the [Technical SEO for Small Business](../technical-seo-for-small-business/) guide.

## Understanding the main types of redirects

Not all redirects are created equal. Different status codes tell web browsers and search engines how permanent a move is. Using the wrong type can confuse search engines and hurt your visibility.

Table: Comparison of common redirect types
| Redirect Type | When to use it | SEO impact |
|---|---|---|
| **301 (Permanent)** | Moving a page permanently to a new URL | Passes almost all SEO value to the new page |
| **302 (Temporary)** | Testing a new page or short-term maintenance | Keeps SEO value on the original page |
| **Meta Refresh** | Rarely recommended; handled in browser | Slower and generally discouraged for SEO |

For almost every small business scenario—like changing a product URL or redesigning a site—you want a permanent 301 redirect. This tells search engines to drop the old address from their index and replace it with the new one. 

## How to set up redirects in WordPress and WooCommerce

If your site runs on [WordPress](https://wordpress.org/) or [WooCommerce](https://woocommerce.com/), setting up redirects is straightforward. While you can edit server configuration files like `.htaccess`, using a dedicated plugin is much safer for most business owners.

1. Log in to your WordPress dashboard and go to **Plugins > Add New**.
2. Search for a reputable redirection plugin, such as *Redirection* by John Godley, and click **Install Now** then **Activate**.
3. Navigate to **Tools > Redirection** to open the setup screen.
4. In the **Add new redirection** section, enter your old URL in the **Source URL** field.
5. Enter your new destination URL in the **Target URL** field.
6. Click **Add Redirect** to save your changes.

Whenever you update your permalink structure or delete an old service page, remember to check your redirect list to ensure there are no loops or broken paths. For more safety tips when running a WordPress site, take a look at the [How to Update WordPress Safely](../how-to-update-wordpress-safely/) guide.

## How to set up redirects in Shopify and Webflow

Hosted platforms handle server access differently, but they include built-in tools specifically for managing URL redirects for SEO. 

### Setting up redirects in Shopify
1. From your Shopify admin, go to **Online Store > Navigation**.
2. Click on **URL Redirects** near the top of the page.
3. Click **Create redirect**.
4. In the **Redirect from** field, type the old URL path.
5. In the **Redirect to** field, type the new destination URL.
6. Click **Save redirect**.

### Setting up redirects in Webflow
1. Open your Webflow Designer and go to **Site Settings**.
2. Click on the **Hosting** tab and scroll down to the **Redirection** section.
3. Enter your old path in the **Old path** field and your new path in the **Match to** field.
4. Click **Add redirection**, then publish your site to make the changes live.

Both platforms automatically handle 301 redirects, ensuring search engines update their indexes properly. If you are deciding between these tools for an online store, the [Shopify vs WooCommerce](../shopify-vs-woocommerce/) comparison offers more details.

## Common redirection mistakes to avoid

Even with good tools, it is easy to make mistakes that slow down your site or confuse search engines. Watch out for these common pitfalls:

- **Redirect chains:** Pointing URL A to URL B, and then URL B to URL C creates a chain that slows down page loading and wastes search engine crawl budget. Always point the old URL directly to the final destination.
- **Redirecting to irrelevant pages:** If you delete a specific product page, do not redirect users to your homepage. Redirect them to a similar product or your main category page so they still find what they need.
- **Ignoring internal links:** After setting up a redirect, update your internal links so they point straight to the new URL instead of relying on the redirect every time. You can learn more about this in the [Internal Linking for SEO Guide](../internal-linking-for-seo-guide/).

:::callout Tip
Test every redirect in an incognito browser window before sharing the new link on social media or in email campaigns.
:::

## Frequently asked questions {#faq data-toc-label="FAQ"}

### Will a redirect slow down my website?
A single redirect adds a tiny fraction of a second to load times, which is barely noticeable. However, long chains of multiple redirects can noticeably slow down page loading and frustrate users.

### How long should I keep a 301 redirect active?
Keep permanent redirects active for at least one year, though leaving them in place indefinitely is usually fine. This ensures that any old bookmarks or external backlinks continue to land on the correct active page.

### Can I redirect a URL to an external website?
Yes, you can point a redirect to any valid URL on the internet, including a different domain name. However, you should only do this if you completely own both websites or are rebranding your entire business.

---

If you need help setting up your site structure, fixing broken links, or improving your search visibility, you can check out my work on the [portfolio](../../#work) or [get in touch](../../#contact) to discuss your project.
