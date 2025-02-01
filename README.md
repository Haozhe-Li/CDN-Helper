# CDN Helper
[![icons](https://skillicons.dev/icons?i=flask,py,html,vercel)](#)

CDN File Helper is a web application that allows users to easily upload files to Cloudflare R2 and convert GitHub URLs to jsDelivr URLs. This project is built using Flask and integrates with Cloudflare R2 for file storage.

## Use it online: [cdnhelp.haozheli.com](https://cdnhelp.haozheli.com)

[![Website Screenshot](https://cdn.haozheli.com/website_screenshot.webp)](https://cdnhelp.haozheli.com)

## Features

- **GitHub Link Converter**: Convert GitHub file URLs to jsDelivr URLs for fast and reliable CDN delivery.
- **File Uploader**: Upload files to Cloudflare R2 and get a public URL for easy sharing.
- **VIP Code Support**: Use a VIP code to upload files to a premium bucket with fewer restrictions.

## Installation

1. Clone the repository:
    ```sh
    git https://github.com/Haozhe-Li/CDN-Helper.git
    cd cdn-helper
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a [.env](http://_vscodecontentref_/6) file in the root directory and add your Cloudflare R2 credentials:
    ```env
    VIP_CODE="your_vip_code"
    CF_API_URL="your_cloudflare_api_url"
    CF_API_KEY_ID="your_cloudflare_api_key_id"
    CF_API_KEY_SECRET="your_cloudflare_api_key_secret"
    CF_VIP_BUCKET="your_vip_bucket_name"
    CF_FREE_BUCKET="your_free_bucket_name"
    ```

## Usage

1. Run the Flask application:
    ```sh
    python app.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`.

3. Use the web interface to convert GitHub URLs to jsDelivr URLs or upload files to Cloudflare R2.

## Deployment
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FHaozhe-Li%2FCDN-Helper&env=VIP_CODE,CF_API_URL,CF_API_KEY_ID,CF_API_KEY_SECRET,CF_VIP_BUCKET,CF_FREE_BUCKET)

This project is configured to be deployed on Vercel. The [vercel.json](http://_vscodecontentref_/7) file specifies the build and routing configuration.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- Inspired by the blog post ["使用Python掌握上传文件到Cloudflare R2：全面指南"](https://www.desinerd.com/zh-cn/p/mastering-file-uploads-cloudflare-r2-python-comprehensive-guide/) by 迪潘卡的博客.