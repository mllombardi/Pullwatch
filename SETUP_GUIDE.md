# GitHub PR Status Dashboard

Automatically display pull request status across multiple repositories in your README.

## Features

- 🆓 **Completely free** - Uses GitHub's public API with no authentication required
- 🤖 **Automated updates** - GitHub Actions updates the dashboard hourly
- 📊 **Multi-repo support** - Track PRs across multiple repositories
- 🎨 **Clean visualization** - Status emojis and formatted tables

## Setup

### 1. Configure Your Repositories

Edit `update_readme.py` and modify the `REPOS` list:

```python
REPOS = [
    "mllombardi/lombardi-py-forge",
    "mllombardi/lombardi-node-forge",
    "mllombardi/lombardi-hcl-forge",
]
```

### 2. Add Files to Your Repository

Copy these files to your repository:
- `update_readme.py` - The Python script
- `.github/workflows/update-dashboard.yml` - GitHub Actions workflow
- `requirements.txt` - Python dependencies

### 3. Enable GitHub Actions

1. Go to your repository Settings
2. Navigate to Actions → General
3. Under "Workflow permissions", select "Read and write permissions"
4. Click Save

### 4. Run Manually (Optional)

You can trigger the workflow manually:
1. Go to Actions tab
2. Select "Update PR Dashboard"
3. Click "Run workflow"

## How It Works

The script:
1. Fetches open PRs from each configured repository
2. Generates a markdown table with PR details
3. Updates README.md with the latest data
4. GitHub Actions commits the changes automatically

## API Rate Limits

GitHub's public API allows:
- **60 requests per hour** without authentication
- Each repo = 1 request
- With 3 repos and hourly updates = 72 requests/day (well within limits)

### Optional: Use Authentication for Higher Limits

For private repos or higher rate limits (5,000/hour), add a GitHub token:

1. Create a personal access token (Settings → Developer settings → Personal access tokens)
2. Add it as a repository secret named `GH_TOKEN`
3. Modify the script to use authentication:

```python
headers = {"Authorization": f"token {os.environ.get('GITHUB_TOKEN')}"}
response = requests.get(url, params=params, headers=headers)
```

4. Update the workflow to pass the token:

```yaml
- name: Update README
  env:
    GITHUB_TOKEN: ${{ secrets.GH_TOKEN }}
  run: |
    python update_readme.py
```

## Customization

### Change Update Frequency

Edit `.github/workflows/update-dashboard.yml`:

```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
    # - cron: '0 0 * * *'   # Daily at midnight
```

### Modify Status Logic

Edit the `format_pr_table()` function in `update_readme.py` to customize status emojis or add more metadata.

### Filter PRs

Add filters to `get_pull_requests()`:

```python
params = {
    "state": "open",
    "per_page": 10,
    "sort": "updated",
    "direction": "desc"
}
```

## Troubleshooting

**README not updating?**
- Check Actions tab for error logs
- Ensure workflow permissions are set correctly
- Verify repository names in REPOS list

**Rate limit exceeded?**
- Reduce update frequency
- Add authentication token
- Reduce number of repositories

## License

MIT License - feel free to use and modify!