const assert = require('assert');
const path = require('path');
const jusu = require(path.resolve(__dirname, '..', 'jusu.js'));

function test_h_structure() {
  const v = jusu.h('div', { id: 'x' }, 'hello', jusu.h('span', null, 'inner'));
  assert.strictEqual(v.tag, 'div');
  assert.strictEqual(v.props.id, 'x');
  assert.strictEqual(v.children.length, 2);
}

function test_renderToString_basic() {
  const v = jusu.h('div', { id: 'root', className: 'r' }, 'A & B', jusu.h('img', { src: 'a.png' }));
  const s = jusu.renderToString(v);
  // basic checks
  assert.ok(s.indexOf('<div') === 0);
  assert.ok(s.indexOf('A &amp; B') !== -1);
  assert.ok(s.indexOf('<img') !== -1);
}

function test_function_component() {
  function Comp(props) {
    return jusu.h('p', null, 'comp:' + (props.name || 'x'));
  }
  const v = jusu.h(Comp, { name: 'Bob' });
  const s = jusu.renderToString(v);
  assert.strictEqual(s, '<p>comp:Bob</p>');
}

function run() {
  console.log('Running JS port tests...');
  test_h_structure();
  test_renderToString_basic();
  test_function_component();
  console.log('All JS tests passed.');
}

run();
