const { validate } = require('./lib/validator.cjs');
const fs = require('fs');
const path = require('path');

const good = JSON.parse(fs.readFileSync(path.join(__dirname, 'examples', 'simple-ast.json'), 'utf8'));
console.log('Valid AST ->', validate(good));

const bad = JSON.parse(JSON.stringify(good));
bad.content = bad.content.filter(c => c.type !== 'title');
console.log('No-title AST ->', validate(bad));
