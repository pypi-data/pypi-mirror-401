---
description: Automate the process of checking, committing, and pushing code to GitHub.
---

// turbo-all

1. Check the status of the repository to see what files have changed.
```bash
git status
```

2. Run the linter to ensure code quality.
```bash
cd apps/web && npm run lint
```

3. Add all changes to the staging area.
```bash
git add .
```

4. Commit the changes.
> [!IMPORTANT]
> You should provide a meaningful commit message describing your changes.
```bash
git commit -m "Update: [Describe your changes here]"
```

5. Push the changes to the `main` branch.
> [!NOTE]
> If you are working on a feature, you might want to push to a new branch instead: `git checkout -b feature/my-feature && git push -u origin feature/my-feature`
```bash
git push origin main
```

6. (Optional) If you pushed to a new branch, open a Pull Request on GitHub.
> [!TIP]
> Visit https://github.com/Seifollahi/audiointelligence/pulls to create your PR.

7. Verify Deployment.
> [!IMPORTANT]
> You must check the status of the GitHub Action run to ensure the deployment succeeded. Iteratively fix any issues if the deployment fails.
```bash
gh run list --branch develop --limit 1
# To watch the progress:
# gh run watch [RUN_ID]
```
