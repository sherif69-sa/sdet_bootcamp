document$.subscribe(() => {
  if (typeof mermaid !== 'undefined') {
    mermaid.initialize({
      startOnLoad: true,
      theme: document.body.getAttribute('data-md-color-scheme') === 'slate' ? 'dark' : 'default',
      securityLevel: 'loose'
    });
    mermaid.run({ querySelector: '.mermaid' });
  }
});
