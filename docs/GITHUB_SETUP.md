# GitHub Setup

## Option A – GitHub Desktop

1. Create an empty GitHub repository called `Junos7Journal`.
2. Open GitHub Desktop.
3. Choose **File > Clone Repository** and clone `Junos7Journal`.
4. Extract this framework ZIP.
5. Copy everything inside `Junos7Journal_framework_v0_1/` into your cloned repo folder.
6. In GitHub Desktop, review the changed files.
7. Commit with the message:

```text
Initial project framework
```

8. Click **Push origin**.

## Option B – Command Line

```bash
git clone https://github.com/YOUR-USERNAME/Junos7Journal.git
cd Junos7Journal

# copy the extracted framework files into this folder

git add .
git commit -m "Initial project framework"
git push
```

## Enable GitHub Pages

1. Go to the repository on GitHub.
2. Open **Settings > Pages**.
3. Source: **Deploy from a branch**.
4. Branch: `main`.
5. Folder: `/website` if available.

If `/website` is not available, copy the website files into a `/docs` folder and publish from `/docs`.
