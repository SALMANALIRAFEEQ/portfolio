---
title: "How to Set Up Google Search Console: A Simple Guide"
seo_title: "How to Set Up Google Search Console"
short_title: "Google Search Console Setup"
description: "Learn how to set up Google Search Console for your website. Step-by-step instructions to verify your site, submit a sitemap, and track your search performance."
dek: "I will show you step-by-step how to set up Google Search Console to monitor your website traffic, fix indexing errors, and improve your search rankings."
slug: "how-to-set-up-google-search-console"
date: 2026-11-18
updated: 2026-11-18
author: "Salman Ali Rafeeq"
category: "SEO"
tags: ["SEO", "Google Search Console", "Google", "Indexing"]
keywords: ["how to set up google search console", "google search console setup", "verify website google search console", "submit sitemap google search console", "google search console beginner guide"]
draft: false
generated_by: "gemini/gemini-3.5-flash"
---

If you want your business website to attract organic search traffic, learning how to set up Google Search Console is one of the most effective technical steps you can take. Google Search Console is a free tool provided directly by Google that shows how your site performs in search results, which pages are indexed, and what technical errors might be holding back your rankings.

Whether you run an online store built on [Shopify](https://www.shopify.com/) or a company website managed on [WordPress](https://wordpress.org/), this guide takes you through the setup process step by step. You will learn how to select a property type, verify site ownership, and submit your XML sitemap.

## Why your business website needs Google Search Console

Many small business owners rely solely on Google Analytics to track site traffic. While analytics is essential for understanding visitor behavior, it only tells half the story. 

Google Search Console tells you what happens before a visitor reaches your site. It shows the exact keywords people typed into Google, how often your listings appeared in search results, and how many people clicked through to your pages. Reading this data helps you refine your content without guessing.

Search Console also serves as a direct communication channel between Google and your site. If your website experiences indexing errors or security warnings, Google notifies you inside the dashboard. Fixing these issues early helps protect your search traffic and supports your [technical SEO strategy](../technical-seo-for-small-business/).

:::callout Key takeaway
Google Analytics shows what visitors do after arriving on your site, while Google Search Console shows how searchers find your site in Google search results before clicking.
:::

## Step 1: Choose your property type

To begin, visit the Google Search Console website and sign in using the primary Google account associated with your business. I recommend using the same account you use for Google Analytics so that connecting the two tools later is straightforward.

Once logged in, you will be prompted to select a property type: **Domain** or **URL Prefix**.

Table: Google Search Console Property Types
| Feature | Domain Property | URL Prefix Property |
|---|---|---|
| Coverage | All subdomains (`www`, `blog`) and protocols (`http`, `https`) | Only the exact URL protocol and path entered |
| Verification Method | DNS TXT record via domain registrar | HTML tag, HTML file, GA4, GTM, or DNS |
| Best Used For | Complete site tracking across all domain variations | Quick setup when you do not have DNS access |

A **Domain property** is usually the best choice because it tracks everything under your domain name, including subdomains and both `http://` and `https://` versions. However, it requires adding a record to your domain's DNS settings.

If you cannot access your domain registrar (such as Namecheap or GoDaddy), choosing a **URL Prefix property** lets you verify ownership using simpler methods like adding an HTML meta tag or using an existing plugin.

## Step 2: Verify website ownership

Before Google displays search data for a domain, you must prove that you own or manage the website. The verification method depends on the property type you selected.

### Method A: DNS TXT record (Domain property)
1. Select the **Domain** property option and enter your main domain (for example, `yourbusiness.com`).
2. Copy the TXT verification record string provided by Google. It usually starts with `google-site-verification=`.
3. Log in to your domain registrar or web host where your DNS records are managed.
4. Add a new DNS record with the type set to **TXT**, set the host name to `@` (or leave it blank, depending on your provider), and paste the code into the value field.
5. Save the record, return to Search Console, and click **Verify**.

DNS changes can take anywhere from a few minutes to a few hours to update across the internet. If verification does not succeed immediately, wait a short while and try clicking verify again.

### Method B: HTML tag (URL prefix property)
If you chose the **URL Prefix** option, enter your full URL (for example, `https://yourbusiness.com`). The HTML tag method is usually the simplest approach for small business sites.

1. Select **HTML tag** from the list of verification options.
2. Copy the meta tag snippet provided by Google:

```html
<meta name="google-site-verification" content="your_unique_verification_code" />
```

3. Paste this code into the `<head>` section of your site's template:
   - **On WordPress:** Paste the code using your SEO plugin settings or a custom header plugin.
   - **On Shopify:** Go to **Online Store > Themes**, click **Edit code**, open `theme.liquid`, and paste the code directly under the `<head>` tag.
   - **On Webflow:** Open **Project Settings**, go to **Custom Code**, and paste the snippet into the **Head Code** field.
4. Return to Search Console and click **Verify**.

If you already set up tracking using my guide on [how to set up Google Analytics 4](../how-to-set-up-google-analytics-4/), you can also select the **Google Analytics** option under URL Prefix to verify ownership instantly.

## Step 3: Submit your XML sitemap

Once your site is verified, your next task is to submit an XML sitemap so Google knows which pages to crawl and index.

An XML sitemap is a structured file that lists all the important pages, blog posts, and products on your site. Most platforms build this file automatically:

- **WordPress:** If you use an SEO plugin like Yoast SEO or Rank Math, your sitemap URL is usually `https://yourbusiness.com/sitemap_index.xml`.
- **Shopify:** Shopify creates a sitemap automatically at `https://yourbusiness.com/sitemap.xml`.
- **Webflow:** Turn on automatic sitemaps in Project Settings under the SEO tab to generate `https://yourbusiness.com/sitemap.xml`.

To submit your sitemap:

1. Click **Sitemaps** under the *Indexing* section in the left navigation sidebar.
2. Under **Add a new sitemap**, enter the end path of your sitemap URL (for example, `sitemap.xml` or `sitemap_index.xml`).
3. Click **Submit**.

> Submitting an XML sitemap does not guarantee instant rankings, but it helps search engine bots discover your new content much faster.

After submitting, Search Console will display a status message. It should read "Success" in green text once Google finishes fetching the file. If you make major site updates later, such as after following a guide on [how to migrate a WordPress site](../how-to-migrate-a-wordpress-site/), checking this tab ensures Google reads your updated structure.

## Core Search Console reports to monitor

Once setup is complete, data begins accumulating within 24 to 48 hours. Reviewing these reports monthly keeps your site technical setup healthy.

### 1. Performance report
The Performance report shows how your site appears in search results over time:
- **Total Clicks:** How many times searchers clicked through to your site.
- **Total Impressions:** How many times a link to your site appeared in search results.
- **Average CTR (Click-Through Rate):** The percentage of impressions that generated a click.
- **Average Position:** The average search ranking position of your URLs.

Below the chart, review the exact queries people typed to find your site. This data is useful when working through an [on-page SEO checklist](../on-page-seo-checklist/) or refining your product pages.

:::callout Tip
Filter your Performance report by individual pages to find pages with high impressions but low clicks. Updating title tags or [writing a better meta description](../how-to-write-a-meta-description/) can help increase click-through rates.
:::

### 2. Page indexing report
Located under the **Indexing** section, this report lists which pages Google indexed and which pages were skipped.

Not all exclusions are errors. Admin pages and checkout screens should remain unindexed. However, if product pages show errors like "404 Not Found" or "Server Error (5xx)", you need to resolve them. If you changed URL paths recently, setting up proper redirects following my guide on [how to redirect URLs properly](../how-to-redirect-urls-properly/) fixes broken indexing entries.

### 3. URL inspection tool
The search bar at the top of Search Console is the URL Inspection tool. Paste any URL from your site to see its indexing status. When you publish a new article or launch a product, paste the URL here and click **Request Indexing** to prompt Google to crawl the page promptly.

## Frequently asked questions {#faq data-toc-label="FAQ"}

### How long does it take for Google Search Console to show data?
It usually takes 24 to 48 hours after verifying website ownership for initial search data to appear. Search Console only collects performance data from the day your property is verified, so past search query history before setup will not be available.

### Is Google Search Console completely free to use?
Yes, Google Search Console is a completely free tool provided directly by Google for website owners. There are no paid tiers, subscriptions, or hidden charges required to access any of its features or reports.

### What is the difference between Google Search Console and Google Analytics?
Google Search Console tracks search engine visibility, keyword rankings, and technical indexing issues before users click. Google Analytics measures visitor behavior, conversions, and traffic sources after visitors land on your site.

***

Setting up Search Console is one of the most practical steps you can take to keep your site visible to potential clients and customers. If you encounter technical verification issues or need help resolving indexing errors on your site, take a look at my past work on my [portfolio](../../#work) or [get in touch](../../#contact) to discuss getting your website properly configured.
