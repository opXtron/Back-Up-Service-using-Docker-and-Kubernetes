Creating a Backup service that periodically backup the contents of a folder to **Google Drive using Docker and Kubernets**.

**TechStack used:** Docker, Kubernets, Google-Drive-api,Python Libraries

**Week-1:**
Contains Dockerfile & backup script that performs google-drive-authentication and fetches top-10 most recently used files from Google Drive.

**Week-2:**
Implemented Backup service using Kubernets Cronjob and PVC. A file/folder can be uploaded to drive, maintaining its single copy in drive, thus,eliminating redundancy.
Appropriate message shown to user if file/folder aldready exists in drive.
