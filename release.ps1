$git_dir = "$(git rev-parse --show-toplevel)"
$pyproject = "${git_dir}/pyproject.toml"

Write-Host "Suggested version tag: $(Get-Date -UFormat "%y.%W").0"
$version = Read-Host -Prompt "Enter a version tag (0Y.0W.MICRO)"  

# update version in pyproject.toml
$msg = "# managed by ./release.ps1"
(Get-Content ${pyproject}) -replace ("^version = .*$", "version = `"${version}`" ${msg}") | Set-Content ${pyproject}

# commit changes & tag
git add -A
git commit -m "chore(release): prepare for $version"
git tag "${version}"

Write-Host "All done :)"
Write-Host "Now ``git push`` and ``git push --tags"