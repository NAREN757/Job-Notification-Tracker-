
import os
import codecs

path = r'C:\Users\naren\.gemini\antigravity\scratch\preview.html'

with codecs.open(path, 'r', 'utf-8') as f:
    content = f.read()

# Define the old block to replace (using a unique substring approach to be safer)
# We will identify the start of shipProject and the end of copySubmission
# shipProject starts around "window.shipProject = () => {"
# copySubmission ends around "alert('📋 Final Submission copied to clipboard.');\n                });\n            };"

start_marker = "window.shipProject = () => {"
end_marker = "alert('📋 Final Submission copied to clipboard.');"
end_marker_suffix = "});\n            };"

start_idx = content.find(start_marker)

if start_idx == -1:
    print("Error: Could not find start marker")
    exit(1)

# Find the end of the block (after copySubmission)
end_idx = content.find(end_marker, start_idx)

if end_idx == -1:
    print("Error: Could not find end marker")
    exit(1)

# Find the specific closing braces after the alert
final_end_idx = content.find(end_marker_suffix, end_idx)
if final_end_idx == -1:
    # Try finding just "};" if the specific indent is wrong
    final_end_idx = content.find("};", end_idx) + 2
    # This is risky, let's look for the next "window.updatePreference" or similar?
    # Actually, let's just look for "window.updatePreference =" ?
    next_func_idx = content.find("window.updatePreference =", end_idx)
    if next_func_idx != -1:
        # Go back to the closing brace before it
        final_end_idx = content.rfind("};", 0, next_func_idx) + 2
    else:
        print("Error: Could not find next function marker")
        exit(1)
else:
    final_end_idx += len(end_marker_suffix)


new_code = """window.shipProject = () => {
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
            };"""

new_content = content[:start_idx] + new_code + "\n\n            // --- ACTIONS ---" + content[content.find("window.updatePreference =", final_end_idx):].replace("window.updatePreference =", "", 1)
# Wait, simply cutting out the old block and inserting new is safer if we know boundaries.
# I will just replace from start_idx to final_end_idx with new_code

# To stay safe, let's retry finding the "window.updatePreference =" which is definitely after copySubmission
next_marker = "window.updatePreference ="
next_idx = content.find(next_marker, start_idx)

if next_idx == -1:
    print("Error: Could not find next marker")
    exit(1)

# Find the last "};" before next_marker. That should be the end of copySubmission.
block_end = content.rfind("};", start_idx, next_idx) + 2

# Check if we have what looks like the right content
old_block = content[start_idx:block_end]
# print("Replacing block:\n", old_block) 

new_full_content = content[:start_idx] + new_code + "\n\n            " + content[next_idx:]
# Note: I'm removing the space between copySubmission end and updatePreference start and injecting new_code + spacing

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(new_full_content)

print("Updated preview.html logic successfully")
