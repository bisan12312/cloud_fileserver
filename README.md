# DepthNote marketing site

## Deploying the site to GitHub Pages

1. **Commit your changes locally**  
   Make sure any updates (such as the new logo) are committed to the branch you want to publish.
2. **Push the branch to GitHub**  
   ```bash
   git push origin main
   ```
   Replace `main` with another branch name if needed.
3. **Enable GitHub Pages**  
   In your repository on GitHub, go to **Settings → Pages**.
4. **Configure the source**  
   Under "Build and deployment", choose **Deploy from a branch**, select the branch you pushed (e.g., `main`) and the `/ (root)` folder.
5. **Save and wait for the build**  
   Click **Save** and wait for the Pages build to finish. GitHub will display the live URL once deployment succeeds.
6. **Verify the live site**  
   Visit the URL GitHub provides to confirm that the latest changes are visible.

If you are using GitHub Actions or another workflow, make sure it completes successfully so the new assets are published.
