// Minimal full-port of JUSU helpers for the web (CommonJS)
// Exports: h, render, renderToString

function h(tag, props) {
  var children = [].slice.call(arguments, 2);
  return { tag: tag, props: props || {}, children: children };
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderToString(vnode) {
  if (vnode === null || vnode === undefined) return '';
  if (typeof vnode === 'string' || typeof vnode === 'number') return escapeHtml(vnode);
  if (typeof vnode.tag === 'function') {
    var comp = vnode.tag;
    var rendered = comp(Object.assign({}, vnode.props || {}, { children: vnode.children }));
    return renderToString(rendered);
  }
  var tag = vnode.tag || 'div';
  var props = vnode.props || {};
  var attr = '';
  Object.keys(props).forEach(function (k) {
    var val = props[k];
    if (k === 'className') k = 'class';
    if (val === true) {
      attr += ' ' + k;
    } else if (val === false || val == null) {
      // skip
    } else {
      attr += ' ' + k + '="' + escapeHtml(val) + '"';
    }
  });
  var children = (vnode.children || []).map(renderToString).join('');
  if (isVoidElement(tag)) return '<' + tag + attr + ' />';
  return '<' + tag + attr + '>' + children + '</' + tag + '>';
}

function isVoidElement(tag) {
  return /^(area|base|br|col|embed|hr|img|input|link|meta|param|source|track|wbr)$/i.test(tag);
}

function render(vnode, container) {
  // Browser DOM mount if document and container element available
  if (typeof document !== 'undefined' && container && container.appendChild) {
    var root = toDOM(vnode);
    container.innerHTML = '';
    container.appendChild(root);
    return container;
  }
  // If container is a string path or not DOM, return HTML string
  return renderToString(vnode);
}

function toDOM(vnode) {
  if (vnode === null || vnode === undefined) return document.createTextNode('');
  if (typeof vnode === 'string' || typeof vnode === 'number') return document.createTextNode(String(vnode));
  if (typeof vnode.tag === 'function') {
    var comp = vnode.tag;
    var rendered = comp(Object.assign({}, vnode.props || {}, { children: vnode.children }));
    return toDOM(rendered);
  }
  var el = document.createElement(vnode.tag || 'div');
  var props = vnode.props || {};
  Object.keys(props).forEach(function (k) {
    var val = props[k];
    if (k === 'className') el.setAttribute('class', val);
    else if (k === 'style' && typeof val === 'object') {
      Object.keys(val).forEach(function (s) { el.style[s] = val[s]; });
    } else if (val === true) el.setAttribute(k, '');
    else if (val != null) el.setAttribute(k, val);
  });
  (vnode.children || []).forEach(function (c) { el.appendChild(toDOM(c)); });
  return el;
}

// Simple component helper to create function components
function createComponent(fn) { return fn; }

function toggleClass(el, cls) { el.classList.toggle(cls); }
module.exports = { h: h, render: render, renderToString: renderToString, createComponent: createComponent, toggleClass: toggleClass };
