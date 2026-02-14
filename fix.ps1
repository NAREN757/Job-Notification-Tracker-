
$path = 'C:\Users\naren\.gemini\antigravity\scratch\preview.html'
Write-Host "Reading $path"
$l = [System.IO.File]::ReadAllLines($path)
Write-Host "Line count: $($l.Count)"

$countKeep1 = 2818
$skipEnd = 2959
$keep3Start = 2963

if ($l.Count -lt 3000) {
    Write-Error "File seems too short! Count: $($l.Count)"
    exit 1
}

# Keep lines 0..2817 (1..2818)
$part1 = $l[0..($countKeep1-1)]

# Keep lines 2960..2961 (2961..2962) - indices
$part2 = $l[($skipEnd+1)..($skipEnd+2)]

# Keep lines 2963..End (2964..End) - indices
$part3 = $l[$keep3Start..($l.Count-1)]

$newContent = $part1 + $part2 + $part3
Write-Host "New count: $($newContent.Count)"

[System.IO.File]::WriteAllLines($path, $newContent)
Write-Host "Done"
