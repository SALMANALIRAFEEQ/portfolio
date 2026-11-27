---
title: "How to Fix WordPress Not Sending Emails: A Simple Guide"
seo_title: "Fix WordPress Not Sending Emails"
short_title: "Fix WordPress Emails"
description: "Learn how to fix WordPress not sending emails from your contact forms and orders using a reliable SMTP setup. Follow this easy step-by-step guide."
dek: "Missed leads and unreceived order receipts usually come down to default server mail settings. Here is how I fix WordPress email delivery using free SMTP."
slug: "fix-wordpress-not-sending-emails"
date: 2026-11-27
updated: 2026-11-27
author: "Salman Ali Rafeeq"
category: "Web Development"
tags: ["WordPress", "Email", "Web Development", "Troubleshooting"]
keywords: ["fix WordPress not sending emails", "WordPress form not sending email", "WordPress SMTP setup", "WordPress email delivery issues", "WP Mail SMTP tutorial"]
draft: false
generated_by: "gemini/gemini-flash-latest"
---

Few things are more frustrating than discovering your contact forms have been silently failing for days or weeks. When potential clients reach out and receive total silence in return, you lose real business before you even know they contacted you. Learning how to fix WordPress not sending emails is one of the most critical maintenance steps you can take for your website.

Whether your site fails to send password reset links, WooCommerce order updates, or contact form alerts, the underlying issue is almost always the same. In this guide, I will walk you through why this happens and how to solve it permanently using a reliable email setup.

## Why your WordPress site stops sending emails

When someone fills out a form on your site, WordPress processes the submission and attempts to send a notification message. In a fresh installation, WordPress tries to send these messages directly from your web server using an internal function.

The core problem is that WordPress does not check whether the message actually landed in an inbox. It simply triggers the request and marks the job as complete on its end. If the message gets rejected along the way, WordPress gives you no warning or error message on your dashboard.

This creates persistent WordPress email delivery issues that go unnoticed until a customer complains or you notice a sudden drop in incoming leads. Common warning signs include:

- A WordPress form not sending email notifications to the site administrator after submission.
- Visitors reporting that they never received automated confirmation or welcome emails.
- WooCommerce store notifications missing for new orders or inventory alerts.
- Admin password reset emails never arriving in your inbox or spam folder.

If your forms are completely broken rather than just missing notifications, you may want to review your general setup or check how other platforms handle them, such as how you might [set up Webflow forms without losing leads](../how-to-set-up-webflow-forms/) or clean up your site code.

## Why default PHP mail fails on modern hosting

By default, WordPress uses a built-in server script called the PHP `mail()` function to send notification messages. While this method worked fine in the early days of the web, modern email security standards have made it practically obsolete.

When you send an email through default PHP mail, the message leaves your web server without proper authentication headers. Modern email providers like Gmail, Yahoo, and Microsoft Outlook scan every incoming email for digital signatures that verify the sender is legitimate. Because raw server mail lacks these signatures, receiving mail servers view it with extreme suspicion.

Furthermore, if you host your site on shared hosting, hundreds of websites share the same server IP address. If another site on that server sends spam, major email providers block the entire server address. Even when choosing solid [web hosting for small business](../choose-web-hosting-for-small-business/), many quality hosting companies intentionally disable or severely restrict PHP mail to keep their servers off global blacklists.

Table: Comparing default PHP mail with dedicated SMTP
| Feature | Default PHP mail() | Dedicated SMTP Service |
|---|---|---|
| Sender authentication | None (often flagged as spoofing) | Verified with SPF and DKIM signatures |
| Delivery success rate | Low (often goes directly to spam or blocked) | High (routes through trusted email IPs) |
| Error tracking | None (fails silently inside WordPress) | Detailed delivery logs and error reporting |
| Server load | Handled entirely by your web host | Offloaded to a dedicated external service |

> Sending emails directly from your web server is like mailing a letter with no return address and no postage stamp; most receiving servers simply drop it in the trash.

## Step 1: Install a dedicated SMTP plugin

To fix WordPress not sending emails once and for all, you need to replace default PHP mail with SMTP (Simple Mail Transfer Protocol). SMTP is the universal standard used by regular email clients to authenticate and route outgoing mail safely.

Instead of writing custom server configurations, the easiest way to handle this transition is with a dedicated plugin. The most popular option is WP Mail SMTP, though alternatives like Post SMTP work similarly.

Here is a quick WP Mail SMTP tutorial walkthrough to get started:

1. Log in to your WordPress dashboard.
2. Go to **Plugins > Add New**.
3. Search for **WP Mail SMTP** in the search bar.
4. Click **Install Now**, then click **Activate**.

Once activated, you will see a new menu item labeled **WP Mail SMTP** in your WordPress sidebar. Open the settings page to begin your WordPress SMTP setup.

:::callout Watch out
Make sure your "From Email" address in the plugin settings matches the domain of your website (such as `hello@yourdomain.com`). Using a personal `@gmail.com` address while sending from a custom domain often triggers automated spam filters.
:::

## Step 2: Connect a reliable email service provider

An SMTP plugin is simply the connector; it still needs a trusted mail service to actually deliver your emails. You have two main routes for this: using your business mailbox (like Google Workspace or Microsoft 365) or using a dedicated transactional email service.

For most business websites, I recommend a transactional email service such as [SendGrid](https://sendgrid.com/) or [Brevo](https://www.brevo.com/). These platforms are built specifically to send automated website notifications reliably, and most offer free tiers that cover standard small business volume.

Here is how to connect a transactional service:

1. **Create an account** on your chosen service provider (for example, Brevo or SendGrid).
2. **Add and verify your sender domain.** The service will ask you to add authentication records (called SPF and DKIM) to your domain DNS settings. This step proves to email providers that your website has permission to send emails from your domain name.
3. **Generate an API key.** Look for the API settings in your email provider's dashboard and create a new key. An API key is simply a secure password that lets WordPress talk to your email service without exposing your primary account credentials.
4. **Select the mailer in WordPress.** In the WP Mail SMTP settings page on your site, select your email provider from the list of mailers.
5. **Paste your API key** into the designated field and click **Save Settings**.

Using an API connection is significantly more secure and reliable than traditional SMTP port and password setups, because it avoids firewall blocks that some web hosts place on standard email ports.

## Step 3: Send a test email and verify delivery

Once your provider is connected, you must confirm that outgoing messages are routing properly. Never assume the connection works without sending a verified test.

Inside WP Mail SMTP, navigate to the **Tools** tab at the top of the settings page and click on **Email Test**:

1. Enter an email address you have active access to in the **Send To** field.
2. Leave the HTML toggle turned on.
3. Click **Send Email**.

If your setup is correct, you will see a success message on the screen, and the test email will appear in your inbox within a few seconds. If the test fails, the plugin provides a clear log detailing exactly what went wrong—such as an invalid API key or missing DNS verification.

Finally, visit your live website as a regular visitor and submit a test entry through every contact form. If you manage an online store, make sure automated notices function properly as part of your broader [WooCommerce order management](../woocommerce-order-management-guide/) routine. Once those form submissions arrive cleanly in your inbox, your email issues are resolved.

Taking the time to implement proper email authentication protects your website's communication and ensures you never miss a client enquiry. If you need assistance configuring your site infrastructure or want to review my technical projects, feel free to explore [my work](../../#work) or [get in touch](../../#contact) directly.

## Frequently asked questions {#faq data-toc-label="FAQ"}

### Can I just use my personal Gmail account with an SMTP plugin?
While plugins offer a Gmail connector, Google limits daily automated sending and frequently blocks connections if it suspects automated activity. Using a custom domain email paired with a dedicated transactional service like Brevo or SendGrid is far more reliable for business sites.

### Why do my WordPress emails still go to the spam folder after setting up SMTP?
This usually means your domain lacks proper DNS authentication records like SPF and DKIM. Adding these text records at your domain registrar proves your emails are legitimate and stops providers like Google and Yahoo from treating them as junk.

### Do I have to pay for a transactional email service?
Most small websites do not need to pay anything upfront. Providers like Brevo and SendGrid have generous free tiers that easily handle standard contact form alerts and basic store notifications for small businesses.
