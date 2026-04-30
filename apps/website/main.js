document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide Icons
    lucide.createIcons();

    // Theme Toggle Logic
    const themeToggle = document.getElementById('themeToggle');
    const html = document.documentElement;
    
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
    
    if (savedTheme) {
        html.setAttribute('data-theme', savedTheme);
    } else if (systemPrefersLight) {
        html.setAttribute('data-theme', 'light');
    }
    
    themeToggle.addEventListener('click', () => {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });

    // Mouse Coordination Tracking (Hero Section)
    const heroVisual = document.getElementById('heroVisual');
    const coordDisplay = document.getElementById('mouseCoord');
    const radarUI = document.getElementById('radarUI');

    if (heroVisual) {
        heroVisual.addEventListener('mousemove', (e) => {
            const rect = heroVisual.getBoundingClientRect();
            const x = Math.floor(e.clientX - rect.left);
            const y = Math.floor(e.clientY - rect.top);
            
            coordDisplay.textContent = `X:${x.toString().padStart(3, '0')} Y:${y.toString().padStart(3, '0')}`;
            
            // Subtle parallax for radar
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const moveX = (x - centerX) / 20;
            const moveY = (y - centerY) / 20;
            radarUI.style.transform = `translate(${moveX}px, ${moveY}px)`;
        });
        
        heroVisual.addEventListener('mouseleave', () => {
            radarUI.style.transform = `translate(0, 0)`;
        });
    }

    // Live Metrics Counter Animation
    const animateValue = (id, start, end, duration) => {
        const obj = document.getElementById(id);
        if (!obj) return;
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const value = Math.floor(progress * (end - start) + start);
            obj.textContent = value.toLocaleString();
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    };

    animateValue('countScans', 1280000, 1284930, 2000);
    animateValue('countThreats', 12000, 12402, 2000);

    // Forensic Lab Simulator Logic
    const runSimBtn = document.getElementById('runSimulation');
    const simOutput = document.getElementById('simOutput');
    const simAddress = document.getElementById('simAddress');
    const simStatus = document.getElementById('simStatus');

    const logToSim = (text, type = 'info') => {
        const line = document.createElement('div');
        line.style.marginBottom = '0.4rem';
        line.style.opacity = '0';
        line.style.transform = 'translateY(5px)';
        line.style.transition = 'all 0.2s ease';
        
        const timestamp = new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
        
        let prefix = '[INFO]';
        let color = 'var(--text-secondary)';
        
        if (type === 'success') { prefix = '[PASS]'; color = 'var(--accent-green)'; }
        if (type === 'error') { prefix = '[ALRT]'; color = 'var(--accent-red)'; }
        if (type === 'warning') { prefix = '[WARN]'; color = 'var(--accent)'; }
        if (type === 'system') { prefix = '[SYS ]'; color = 'var(--accent-blue)'; }

        line.innerHTML = `<span style="color: #444; font-weight: bold;">${timestamp}</span> <span style="color: ${color}; font-weight: bold; margin-left: 0.5rem;">${prefix}</span> <span style="color: ${color}; margin-left: 0.5rem;">${text}</span>`;
        simOutput.appendChild(line);
        
        setTimeout(() => {
            line.style.opacity = '1';
            line.style.transform = 'translateY(0)';
        }, 10);

        simOutput.scrollTop = simOutput.scrollHeight;
    };

    runSimBtn.addEventListener('click', async () => {
        const address = simAddress.value.trim();
        if (!address.startsWith('0x')) {
            alert('SECURITY_ERROR: INVALID_INPUT_TARGET');
            return;
        }

        runSimBtn.disabled = true;
        simStatus.textContent = 'ANALYSING...';
        simStatus.style.color = 'var(--accent)';
        simOutput.innerHTML = '';
        
        logToSim(`ESTABLISHING_SECURE_CONNECTION...`, 'system');
        await new Promise(r => setTimeout(r, 600));
        
        logToSim(`TARGET_IDENTIFIED: ${address}`);
        logToSim(`EXTRACTING_CONTRACT_BYTECODE...`);
        await new Promise(r => setTimeout(r, 1000));
        
        logToSim(`RUNNING_PATTERN_RECOGNITION_ALGORITHM...`);
        await new Promise(r => setTimeout(r, 800));
        
        logToSim(`SCANNING_FOR_MALICIOUS_DELEGATECALLS...`, 'warning');
        await new Promise(r => setTimeout(r, 1200));
        
        logToSim(`VERIFYING_ERC8004_IDENTITY_CONFORMANCE...`, 'warning');
        await new Promise(r => setTimeout(r, 1000));

        const isMalicious = address.toLowerCase().includes('666') || address.toLowerCase().includes('bad') || address.toLowerCase().includes('hack');
        
        if (isMalicious) {
            logToSim(`THREAT_DETECTED: SUSPICIOUS_LOGIC_FOUND`, 'error');
            logToSim(`SECURITY_RATING: CRITICAL_RISK`, 'error');
            logToSim(`RECOMMENDATION: ABORT_EXECUTION`, 'error');
            simStatus.textContent = 'THREAT_FOUND';
            simStatus.style.color = 'var(--accent-red)';
        } else {
            logToSim(`INTEGRITY_CHECK_COMPLETE`, 'success');
            logToSim(`SECURITY_RATING: LOW_RISK`, 'success');
            logToSim(`RECOMMENDATION: SAFE_TO_PROCEED`, 'success');
            simStatus.textContent = 'SECURE';
            simStatus.style.color = 'var(--accent-green)';
        }

        runSimBtn.disabled = false;
    });

    // Scroll Reveal
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal-active');
            }
        });
    }, observerOptions);

    const revealElements = [
        '.hero-content', '.hero-visual', '.bento-item', 
        '.investigation-node', '.simulator-ui'
    ];

    revealElements.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'all 0.6s var(--ease)';
            observer.observe(el);
        });
    });

    window.addEventListener('scroll', () => {
        document.querySelectorAll('.reveal-active').forEach(el => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        });
    });

    // System Time and Current Year
    const updateTime = () => {
        const sysTime = document.getElementById('sysTime');
        if (sysTime) {
            sysTime.textContent = new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
        }
    };
    setInterval(updateTime, 1000);
    updateTime();

    document.getElementById('year').textContent = new Date().getFullYear();
});
