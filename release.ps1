$git_dir = "$(git rev-parse --show-toplevel)"
$pyproject = "${git_dir}/pyproject.toml"
$changelog = "${git_dir}/CHANGELOG.md"
$history = "${git_dir}/HISTORY.md"

Write-Host "Suggested version tag: $(Get-Date -UFormat "%y.%W").0"
$version = Read-Host -Prompt "Enter a version tag (0Y.0W.MICRO)"  

# update version in pyproject.toml
$msg = "# managed by ./release.ps1"
(Get-Content ${pyproject}) -replace ("^version = .*$", "version = `"${version}`" ${msg}") | Set-Content ${pyproject}

# write changelog
git cliff --tag "${version}" --unreleased --strip header --config ${pyproject} > ${changelog}
git cliff --tag "${version}" --config ${pyproject} > ${history}

# commit changes & tag
git add -A
git commit -m "chore(release): prepare for $version"
git tag "${version}"

Write-Host "All done :)"
Write-Host "Now ``git push`` and ``git push --tags"