# Per-book latexmk config. All real settings live in tools/latexmkrc.shared
# at the repo root; this file just sources them. To set up a new book,
# copy this file verbatim into the new book directory -- no edits needed.

my $repo_root_stub = `git rev-parse --show-toplevel 2>/dev/null`;
chomp $repo_root_stub;
if ($repo_root_stub ne '' && -f "$repo_root_stub/tools/latexmkrc.shared") {
    do "$repo_root_stub/tools/latexmkrc.shared";
}
