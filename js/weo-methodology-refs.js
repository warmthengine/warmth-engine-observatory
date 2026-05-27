(function() {
    'use strict';

    let methodologyMap = null;
    let annotationActive = false;
    let termsIndex = []; // sorted by term length descending (longest match first)

    async function loadMap() {
        try {
            const resp = await fetch('/data/weo-methodology-map.json');
            const data = await resp.json();
            methodologyMap = data;
            // Flatten all terms + variants, sort longest first to prevent partial matches
            termsIndex = [];
            for (const entry of data.mappings) {
                const allTerms = [entry.term, ...(entry.variants || [])];
                for (const t of allTerms) {
                    termsIndex.push({
                        term: t,
                        anchor: entry.anchor,
                        context: entry.context,
                        regex: new RegExp('\\b' + escapeRegex(t) + '\\b', 'gi')
                    });
                }
            }
            // Sort longest first to prevent "T1" matching inside "T1 (Cross-Bloc)"
            termsIndex.sort((a, b) => b.term.length - a.term.length);
        } catch (e) {
            console.warn('WEO: methodology map unavailable');
        }
    }

    function escapeRegex(str) {
        return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    function annotateNode(root) {
        if (!methodologyMap || !annotationActive) return;

        const walker = document.createTreeWalker(
            root, NodeFilter.SHOW_TEXT, {
                acceptNode: function(node) {
                    const parent = node.parentElement;
                    if (!parent) return NodeFilter.FILTER_REJECT;
                    if (parent.closest('.weo-ref, a, script, style, nav, .weo-toc, .weo-pub-header'))
                        return NodeFilter.FILTER_REJECT;
                    return NodeFilter.FILTER_ACCEPT;
                }
            }
        );

        const textNodes = [];
        while (walker.nextNode()) textNodes.push(walker.currentNode);

        for (const textNode of textNodes) {
            const text = textNode.textContent;
            if (text.trim().length < 2) continue;

            for (const entry of termsIndex) {
                entry.regex.lastIndex = 0;
                if (entry.regex.test(text)) {
                    const frag = document.createDocumentFragment();
                    let lastIndex = 0;
                    entry.regex.lastIndex = 0;
                    let match;
                    while ((match = entry.regex.exec(text)) !== null) {
                        if (match.index > lastIndex) {
                            frag.appendChild(document.createTextNode(
                                text.slice(lastIndex, match.index)
                            ));
                        }
                        const span = document.createElement('span');
                        span.className = 'weo-ref';
                        span.dataset.weoRef = entry.anchor;
                        span.dataset.weoContext = entry.context;
                        span.textContent = match[0];
                        // Capture anchor in closure
                        (function(anchor) {
                            span.addEventListener('click', function() {
                                window.open(
                                    '/research/methodology/manual/#' + anchor,
                                    '_blank'
                                );
                            });
                        })(entry.anchor);
                        frag.appendChild(span);
                        lastIndex = entry.regex.lastIndex;
                    }
                    if (lastIndex < text.length) {
                        frag.appendChild(document.createTextNode(
                            text.slice(lastIndex)
                        ));
                    }
                    textNode.parentNode.replaceChild(frag, textNode);
                    break; // One match per text node to avoid conflicts
                }
            }
        }
    }

    function toggleAnnotations() {
        annotationActive = !annotationActive;
        document.body.classList.toggle('weo-refs-active', annotationActive);

        const btn = document.getElementById('weoRefToggle');
        if (btn) {
            btn.classList.toggle('active', annotationActive);
            btn.title = annotationActive
                ? 'Methodology references active — click dotted terms'
                : 'Toggle methodology cross-references';
        }

        if (annotationActive) {
            annotateNode(document.querySelector('main') || document.body);
        } else {
            // Unwrap all .weo-ref spans
            document.querySelectorAll('.weo-ref').forEach(function(span) {
                const text = document.createTextNode(span.textContent);
                span.parentNode.replaceChild(text, span);
            });
        }
    }

    function observeDynamic() {
        const observer = new MutationObserver(function(mutations) {
            if (!annotationActive) return;
            mutations.forEach(function(m) {
                m.addedNodes.forEach(function(n) {
                    if (n.nodeType === 1) annotateNode(n);
                });
            });
        });
        observer.observe(document.body, { childList: true, subtree: true });
    }

    loadMap().then(function() {
        observeDynamic();
    });

    window.WEO_REFS = { toggle: toggleAnnotations };
})();
