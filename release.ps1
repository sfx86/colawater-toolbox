param (
    $version
)

$git_dir = "$(git rev-parse --show-toplevel)"
$pyproject = "${git_dir}/pyproject.toml"
$changelog = "${git_dir}/CHANGELOG.md"
$history = "${git_dir}/HISTORY.md"

# check if pyproject path exists
If (-Not (Test-Path ${pyproject} -PathType Leaf)) {
    throw [System.IO.FileNotFoundException] "Provided pyproject.toml does not exist: '${pyproject}'"
}
# check for git-cliff
If (-Not (git cliff --version)) {
    throw [System.Management.Automation.CommandNotFoundException] "git-cliff not found. Make sure the virtual environment is activated."
}
# ensure version input & correct format
While (${version} -notmatch '^v[0-9]+\.[0-9]+\.[0-9]+$') {
    $version = Read-Host -Prompt "Enter a version tag (vX.Y.Z)"  
}

# update version in pyproject.toml
$msg = "# managed by ./release.ps1"
(Get-Content ${pyproject}) -replace ("^version = .*$", "version = `"${version}`" ${msg}") | Set-Content ${pyproject}

# write changelog
git cliff --tag "${version}" --unreleased --strip header --config ${pyproject} > ${changelog}
git cliff --tag "${version}" --config ${pyproject} > ${history}

# commit changes & tag
# (git add -A) -and (git commit -m "chore(release): prepare for $version")
# git tag "${version}"


Write-Host "All done :)"
Write-Host "Now ``git push`` and ``git push --tags"