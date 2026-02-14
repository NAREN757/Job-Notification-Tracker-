
$path = "C:\Users\naren\.gemini\antigravity\scratch\preview.html"
$content = Get-Content -Path $path -Raw

# Start marker for replacement
$startMarker = "window.shipProject = () => {"
$startIdx = $content.IndexOf($startMarker)

if ($startIdx -eq -1) {
    Write-Error "Could not find start marker: window.shipProject..."
    exit 1
}

# End marker – we look for the next distinct function start to be safe
$endMarker = "window.updatePreference ="
$endIdx = $content.IndexOf($endMarker, $startIdx)

# If not found, maybe look for `window.toggleSave =` which is after `updatePreferenceInput`?
# In the file, `window.updatePreference =` comes after `copySubmission`.
if ($endIdx -eq -1) {
    Write-Error "Could not find end marker: window.updatePreference..."
    exit 1
}

# The content to replace spans from $startIdx up to $endIdx (excluding endIdx but including trailing space/newlines)
# We want to replace everything there with our new code + some padding

$newCode = @"
window.shipProject = () => {
                const s = window.state.submission;
                const t = window.state.testStatus;
                const allTestsPassed = Object.values(t).every(v => v === true);

                if (!allTestsPassed) {
                    alert('⚠️ Verification Failed: Please complete all items in the Test Checklist.');
                    navigate('test');
                    return;
                }

                if (!s.lovableLink || !s.githubLink || !s.deployLink) {
                    alert('⚠️ Missing Links: Please provide all 3 required links.');
                    return;
                }

                // URL Validation (Simple)
                const isValidUrl = (string) => {
                    try { return Boolean(new URL(string)); } catch (e) { return false; }
                };

                if (!isValidUrl(s.lovableLink) || !isValidUrl(s.githubLink) || !isValidUrl(s.deployLink)) {
                    alert('⚠️ Invalid URL: Please ensure all links are valid URLs (http/https).');
                    return;
                }

                window.state.submission.shipped = true;
                if (!window.state.submission.shippedAt) {
                    window.state.submission.shippedAt = new Date().toISOString();
                }
                localStorage.setItem('jobTrackerSubmission', JSON.stringify(window.state.submission));

                // Calm confirmation
                const toast = document.createElement('div');
                toast.className = 'toast';
                toast.style.background = '#2e7d32'; // Green
                toast.innerHTML = `<span>✅</span> Project 1 Shipped Successfully.`;
                document.getElementById('app-root').appendChild(toast);
                setTimeout(() => toast.remove(), 4000);

                render();
            };

            window.copySubmission = () => {
                const s = window.state.submission;
                const text = `
Job Notification Tracker — Final Submission

Lovable Project:
${s.lovableLink}

GitHub Repository:
${s.githubLink}

Live Deployment:
${s.deployLink}

Core Features:
- Intelligent match scoring
- Daily digest simulation
- Status tracking
- Test checklist enforced
`.trim();

                navigator.clipboard.writeText(text).then(() => {
                    alert('📋 Final Submission copied to clipboard.');
                });
            };

            // --- ACTIONS ---
            
"@

# Construct new content safely
# Start part: 0 to startIdx
# + newCode
# + End part: from endIdx to end

$newContent = $content.Substring(0, $startIdx) + $newCode + $content.Substring($endIdx)

$newContent | Set-Content -Path $path -NoNewline
Write-Host "Replaced shipProject and copySubmission successfully."
