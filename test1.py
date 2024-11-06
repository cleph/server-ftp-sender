from ftplib import FTP
from tqdm import tqdm
import os


def connect_ftp(host, username, password):
    ftp = FTP(host)
    ftp.login(user=username, passwd=password)
    return ftp


def download_file(ftp, filename, local_file):
    with open(local_file, 'wb') as f:
        total_size = ftp.size(filename)
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Downloading {filename}") as pbar:
            def callback(data):
                f.write(data)
                pbar.update(len(data))

            ftp.retrbinary(f'RETR {filename}', callback)


def upload_file(ftp, local_file, filename):
    total_size = os.path.getsize(local_file)
    with open(local_file, 'rb') as f:
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Uploading {filename}") as pbar:
            def callback(data):
                ftp.storbinary(f'STOR {filename}', f, 1024, callback=lambda sent: pbar.update(len(sent)))


def transfer_files(src_host, src_user, src_pass, dest_host, dest_user, dest_pass):
    # اتصال به سرور مبدا و مقصد
    src_ftp = connect_ftp(src_host, src_user, src_pass)
    dest_ftp = connect_ftp(dest_host, dest_user, dest_pass)

    # دریافت لیست فایل‌های سرور مبدا
    files = src_ftp.nlst()

    for filename in files:
        local_file = f"temp_{filename}"

        # دانلود فایل از سرور مبدا
        download_file(src_ftp, filename, local_file)

        # آپلود فایل به سرور مقصد
        upload_file(dest_ftp, local_file, filename)

        # حذف فایل موقت محلی
        os.remove(local_file)

    # قطع ارتباط از سرورها
    src_ftp.quit()
    dest_ftp.quit()


# اطلاعات ورود به سرورها
src_host = 'ftp.source-server.com'
src_user = 'source_username'
src_pass = 'source_password'

dest_host = 'ftp.destination-server.com'
dest_user = 'destination_username'
dest_pass = 'destination_password'

# انتقال فایل‌ها
transfer_files(src_host, src_user, src_pass, dest_host, dest_user, dest_pass)
