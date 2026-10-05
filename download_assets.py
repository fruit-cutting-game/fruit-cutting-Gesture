import os
import urllib.request

def download_assets():
    os.makedirs('assets', exist_ok=True)

    # Direct public PNG image URLs (with transparent backgrounds)
    assets = {
        'assets/watermelon.png': 'https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f349.png',
        'assets/apple.png':      'https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f34e.png',
        'assets/orange.png':     'https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f34a.png',
        'assets/banana.png':     'https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f34c.png',
        'assets/bomb.png':       'https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f4a3.png'
    }

    print("Downloading fruit assets...")
    for path, url in assets.items():
        if not os.path.exists(path):
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(path, 'wb') as out_file:
                out_file.write(response.read())
            print(f"Downloaded: {path}")
        else:
            print(f"Already exists: {path}")

if __name__ == "__main__":
    download_assets()