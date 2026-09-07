const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const oldPattern = /loading="lazy"\s+decoding="async"\s+width="160"\s+height="80"\s+onerror="this\.onerror=null;\s*this\.style\.display='none';"/g;
const replacement = 'loading="eager" decoding="sync" width="160" height="80" onerror="this.onerror=null; if(this.closest(\'.brand-item\')) this.closest(\'.brand-item\').style.display=\'none\';"';

const matches = html.match(oldPattern);
console.log('Matches found:', matches ? matches.length : 0);

html = html.replace(oldPattern, replacement);
fs.writeFileSync('index.html', html, 'utf8');
console.log('index.html updated successfully');
