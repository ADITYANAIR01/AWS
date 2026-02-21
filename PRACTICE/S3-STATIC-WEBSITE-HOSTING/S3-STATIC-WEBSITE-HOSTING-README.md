# S3 Static Website Hosting

## What is S3 Static Website Hosting?

**Amazon S3 (Simple Storage Service)** can host static websites directly from a bucket without requiring a traditional web server. When you enable static website hosting on an S3 bucket, AWS provides a unique endpoint URL that serves your HTML, CSS, JavaScript, and image files to anyone on the internet — as long as you configure the bucket for public read access and attach the appropriate bucket policy. This is a cost-effective, highly available, and scalable solution for hosting personal websites, single-page applications, documentation sites, landing pages, and portfolios. Unlike dynamic websites that require backend servers and databases, S3 static hosting is ideal for content that doesn't change based on user interactions or server-side processing.

---

## Lab Overview

| Resource | Name / Value |
|---|---|
| S3 Bucket | `your-unique-bucket-name` |
| Bucket Policy | Allow public `GetObject` |
| Static Website Hosting | Enabled |
| Index Document | `index.html` |
| Region | `ap-south-1` (or your preferred region) |
| Bucket Website Endpoint | `http://<bucket-name>.s3-website-<region>.amazonaws.com` |

---

## Video Demo

[![S3 Static Website Hosting – Full Demo](https://img.youtube.com/vi/klEGEw2O6q0/0.jpg)](https://youtu.be/klEGEw2O6q0)

---

## Step-by-Step Walkthrough

### Step 1 — Open AWS Console and Navigate to S3

Log in to the AWS Management Console and search for **S3** in the services search bar, then click on S3 to open the S3 dashboard.

![AWS Console – navigate to S3](./images/s3-static-website-hosting-01.png)

---

### Step 2 — Create an S3 Bucket

#### 2a — Click Create bucket

In the S3 dashboard, click **Create bucket** to begin the bucket creation wizard.

![S3 Dashboard – click Create bucket](./images/s3-static-website-hosting-02.png)

#### 2b — Enter a unique bucket name

Enter a **globally unique bucket name**. Bucket names must be unique across all AWS accounts worldwide and must follow DNS naming conventions (lowercase letters, numbers, and hyphens only).

![Bucket creation wizard – enter unique bucket name](./images/s3-static-website-hosting-03.png)

#### 2c — Uncheck "Block all public access"

Scroll down to the **Block Public Access settings** section and **uncheck "Block all public access"**. For static website hosting to work, your bucket must allow public read access to its objects.

> ⚠️ **Important:** Unchecking this setting means anyone with the URL can access files in this bucket. Only use this for content you intend to make publicly available.

![Uncheck Block all public access](./images/s3-static-website-hosting-04.png)

#### 2d — Acknowledge the warning and create the bucket

Check the acknowledgment box confirming you understand the bucket will be public, then click **Create bucket** at the bottom of the page.

![Acknowledge and click Create bucket](./images/s3-static-website-hosting-05.png)

---

### Step 3 — Upload Website Files

#### 3a — Open the bucket

The bucket is created successfully. Click on the **bucket name** to open it and view its contents.

![Bucket created successfully – click on bucket name](./images/s3-static-website-hosting-06.png)

#### 3b — Click Upload

Inside the bucket, click the **Upload** button to open the file upload wizard.

![Inside bucket – click Upload](./images/s3-static-website-hosting-07.png)

#### 3c — Add files

Click **Add files** or **Add folder** and select the static website files from your local machine (HTML, CSS, JavaScript, images, etc.).

![Upload wizard – add files](./images/s3-static-website-hosting-08.png)

#### 3d — Upload the files

After selecting your files, scroll down and click **Upload** to transfer them to the S3 bucket.

![Click Upload to upload files](./images/s3-static-website-hosting-09.png)

---

### Step 4 — Enable Static Website Hosting

#### 4a — Navigate to Properties tab

Click on the **Properties** tab at the top of the bucket page.

![Click Properties tab](./images/s3-static-website-hosting-10.png)

#### 4b — Find Static website hosting section

Scroll down to the **Static website hosting** section at the bottom of the Properties page.

![Scroll to Static website hosting](./images/s3-static-website-hosting-11.png)

#### 4c — Enable static website hosting

Click **Edit**, then select **Enable**. Choose **Host a static website** as the hosting type, and enter `index.html` as the **Index document** (the default page visitors see when they access your site).

![Enable static website hosting and set index document](./images/s3-static-website-hosting-12.png)

#### 4d — Save changes

Scroll down and click **Save changes** to apply the static website hosting configuration.

![Save changes](./images/s3-static-website-hosting-13.png)

---

### Step 5 — Configure Bucket Policy

#### 5a — Navigate to Permissions and edit bucket policy

Click the **Permissions** tab, scroll down to **Bucket policy**, and click **Edit**.

![Permissions tab – edit bucket policy](./images/s3-static-website-hosting-14.png)

#### 5b — Add a statement or use Policy generator

Click **Add statement** or **Policy generator** to create a new bucket policy. The policy generator helps you build the JSON policy without writing it manually.

![Click Add statement or Policy generator](./images/s3-static-website-hosting-15.png)

---

### Step 6 — Generate and Apply the Bucket Policy

#### 6a — Open AWS Policy Generator

If using the AWS Policy Generator, you'll see a form. Configure it as follows to allow public read access to all objects in the bucket.

![AWS Policy Generator interface](./images/s3-static-website-hosting-17.png)

**Policy Settings:**

| Field | Value |
|---|---|
| **Effect** | Allow |
| **Principal** | `*` (anyone) |
| **Actions** | `GetObject` |
| **ARN** | `arn:aws:s3:::your-bucket-name/*` (replace with your bucket name and add `/*` at the end) |

#### 6b — Add statement and generate policy

After entering the settings above, click **Add Statement**, then click **Generate Policy**.

![Add Statement button](./images/s3-static-website-hosting-18.png)

#### 6c — Copy the generated policy

The policy generator will output a JSON policy. Click **Copy** to copy the entire policy to your clipboard.

![Copy the generated policy](./images/s3-static-website-hosting-19.png)

**Sample Bucket Policy:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```

> **Note:** Replace `your-bucket-name` with your actual bucket name.

#### 6d — Paste the policy and save changes

Return to the bucket policy editor, paste the policy JSON, and click **Save changes**.

![Paste policy in bucket policy editor](./images/s3-static-website-hosting-20.png)

#### 6e — Bucket policy created successfully

You'll see a confirmation that the bucket policy has been successfully applied.

![Bucket policy successfully created](./images/s3-static-website-hosting-21.png)

---

### Step 7 — Access Your Website

#### 7a — Return to Properties tab

Click the **Properties** tab again.

![Properties tab](./images/s3-static-website-hosting-22.png)

#### 7b — Copy the bucket website endpoint

Scroll down to the **Static website hosting** section and copy the **Bucket website endpoint** URL.

![Copy bucket website endpoint](./images/s3-static-website-hosting-23.png)

#### 7c — Open the website in your browser

Paste the endpoint URL into your browser's address bar and press Enter. Your static website is now live and publicly accessible! 🎉

![Website successfully hosted on S3](./images/s3-static-website-hosting-24.png)

---

### Step 8 — Clean Up Resources (Empty the Bucket)

#### 8a — Empty the bucket

To delete a bucket, you must first empty it. Select the bucket (or open it) and click **Empty**.

![Select bucket and click Empty](./images/s3-static-website-hosting-25.png)

#### 8b — Confirm deletion of objects

Type `permanently delete` in the confirmation field and click **Delete objects**.

![Type permanently delete and confirm](./images/s3-static-website-hosting-26.png)

---

### Step 9 — Delete the S3 Bucket

#### 9a — Select the bucket and click Delete

After emptying the bucket, select it from the S3 dashboard and click **Delete**.

![Select bucket and click Delete](./images/s3-static-website-hosting-27.png)

#### 9b — Confirm bucket deletion

Type the **bucket name** exactly as shown to confirm permanent deletion, then click **Delete bucket**.

![Type bucket name to confirm deletion](./images/s3-static-website-hosting-28.png)

#### 9c — Bucket deleted successfully

The bucket and all its configurations are now permanently deleted.

![Bucket successfully deleted](./images/s3-static-website-hosting-29.png)

---

## Key Points to Remember

| Point | Details |
|---|---|
| **Bucket names must be globally unique** | No two buckets can have the same name across all AWS accounts worldwide |
| **Public access is required** | Static website hosting requires public read access via bucket policy |
| **Bucket policy syntax** | Must allow `s3:GetObject` action for `Principal: "*"` on `Resource: "arn:aws:s3:::bucket-name/*"` |
| **Index document** | Always specify `index.html` or your custom default page |
| **Endpoint URL format** | `http://<bucket-name>.s3-website-<region>.amazonaws.com` |
| **HTTPS not supported by default** | Use Amazon CloudFront for HTTPS and custom domains |
| **Cost efficiency** | Free tier includes 5GB storage, 20,000 GET requests, and 2,000 PUT requests per month (first 12 months) |
| **Always clean up** | Delete buckets and objects when no longer needed to avoid charges |

---

## Use Cases

- 📄 Personal websites and blogs
- 🚀 Single-page applications (SPAs)
- 📚 Documentation sites
- 🎨 Portfolio websites
- 📱 Landing pages
- 🧪 Prototype hosting and demos

---

## Additional Resources

- [AWS S3 Static Website Hosting Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)
- [S3 Pricing](https://aws.amazon.com/s3/pricing/)
- [Using CloudFront with S3 for HTTPS](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web.html)
