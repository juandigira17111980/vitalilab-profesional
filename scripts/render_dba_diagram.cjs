// Optional documentation tool: npm package @viz-js/viz, no application dependency.
const fs = require('node:fs');
const path = require('node:path');
const { instance } = require('@viz-js/viz');

async function main() {
  const folder = path.resolve(__dirname, '../docs/dba');
  const viz = await instance();
  const svg = viz.renderString(fs.readFileSync(path.join(folder, 'modelo_completo.dot'), 'utf8'), {
    format: 'svg', engine: 'dot'
  });
  fs.writeFileSync(path.join(folder, 'modelo_completo.svg'), svg);
  process.stdout.write('Generated complete entity-relationship diagram.\n');
}
main().catch(error => { process.stderr.write(error.message + '\n'); process.exitCode = 1; });
