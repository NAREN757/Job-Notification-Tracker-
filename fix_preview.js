const fs = require('fs');
const path = 'C:\\Users\\naren\\.gemini\\antigravity\\scratch\\preview.html';
const content = fs.readFileSync(path, 'utf8').split(/\r?\n/);

// Keep indices:
// 0 to 2817 (lines 1-2818)
// 2960 to 2961 (lines 2961-2962)
// 2963 to End (lines 2964-End)

const newLines = [
    ...content.slice(0, 2818),
    ...content.slice(2960, 2962),
    ...content.slice(2963)
];

fs.writeFileSync(path, newLines.join('\n'));
console.log('Fixed preview.html');
