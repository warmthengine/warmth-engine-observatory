(function() {
    'use strict';

    let methodologyMap = null;
    let annotationActive = false;
    let toastShown = false;
    let termsIndex = []; // sorted by term length descending (longest match first)

    // Inject toast styles once
    (function injectStyles() {
        const style = document.createElement('style');
        style.textContent = [
            '.weo-ref-toast{',
            'position:fixed;bottom:5rem;left:50%;transform:translateX(-50%) translateY(8px);',
            'background:rgba(15,23,42,0.92);border:1px solid #334155;',
            'color:#94A3B8;font-size:0.78rem;font-family:"Geist",sans-serif;',
            'padding:0.45rem 0.9rem;border-radius:6px;white-space:nowrap;',
            'opacity:0;transition:opacity 200ms ease,transform 200ms ease;',
            'pointer-events:none;z-index:2000;',
            '}',
            '.weo-ref-toast.weo-ref-toast-visible{opacity:1;transform:translateX(-50%) translateY(0);}',
            '@media(max-width:768px){.weo-ref-toast{display:none;}}'
        ].join('');
        document.head.appendChild(style);
    })();

    async function loadMap() {
        try {
            const resp = await fetch('/data/weo-methodology-map.json');
            const data = await resp.json();
            methodologyMap = data;
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

    function showToast(msg) {
        const toast = document.createElement('div');
        toast.className = 'weo-ref-toast';
        toast.textContent = msg;
        document.body.appendChild(toast);
        requestAnimationFrame(function() {
            toast.classList.add('weo-ref-toast-visible');
        });
        setTimeout(function() {
            toast.classList.remove('weo-ref-toast-visible');
            setTimeout(function() { toast.remove(); }, 250);
        }, 3000);
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
            if (!toastShown) {
                toastShown = true;
                showToast('Methodology references active — click dotted terms to view definitions');
            }
        } else {
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
