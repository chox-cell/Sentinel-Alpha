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

    // Hive Background Interactivity
    const hiveGrid = document.getElementById('hiveGrid');
    const hiveGlow = document.getElementById('hiveGlow');
    const body = document.body;

    window.addEventListener('mousemove', (e) => {
        const x = e.clientX;
        const y = e.clientY;
        
        // Update Glow Position
        body.style.setProperty('--mouse-x', `${x}px`);
        body.style.setProperty('--mouse-y', `${y}px`);
        
        // Grid Parallax
        const moveX = (x - window.innerWidth / 2) / 50;
        const moveY = (y - window.innerHeight / 2) / 50;
        hiveGrid.style.transform = `perspective(1000px) rotateX(45deg) translate(${moveX}px, ${moveY}px)`;
    });

    // Forensic Lab Simulator Logic
    const runSimBtn = document.getElementById('runSimulation');
    const simOutput = document.getElementById('simOutput');
    const simAddress = document.getElementById('simAddress');

    const logToSim = (text, type = 'info') => {
        const line = document.createElement('div');
        line.style.marginBottom = '0.4rem';
        line.style.opacity = '0';
        line.style.transform = 'translateY(5px)';
        line.style.transition = 'all 0.2s ease';
        
        const timestamp = new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
        
        let prefix = '[INFO]';
        let color = 'var(--text-secondary)';
        
        if (type === 'success') { prefix = '[PASS]'; color = '#10b981'; }
        if (type === 'error') { prefix = '[ALRT]'; color = '#ef4444'; }
        if (type === 'warning') { prefix = '[WARN]'; color = 'var(--accent)'; }
        if (type === 'system') { prefix = '[SYS ]'; color = '#3b82f6'; }

        line.innerHTML = `<span style="color: #666; font-weight: bold;">${timestamp}</span> <span style="color: ${color}; font-weight: bold; margin-left: 0.5rem;">${prefix}</span> <span style="color: ${color}; margin-left: 0.5rem;">${text}</span>`;
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
            alert('SECURITY_ERROR: INVALID_TARGET');
            return;
        }

        runSimBtn.disabled = true;
        runSimBtn.textContent = 'SCANNING...';
        simOutput.innerHTML = '';
        
        logToSim(`ESTABLISHING_SECURE_TUNNEL_TO_NODE_01...`, 'system');
        await new Promise(r => setTimeout(r, 600));
        
        logToSim(`TARGET_IDENTIFIED: ${address}`);
        logToSim(`EXTRACTING_BYTECODE_FOR_DECOMPILATION...`);
        await new Promise(r => setTimeout(r, 1000));
        
        logToSim(`DETECTING_DYNAMIC_DELEGATECALLS...`, 'warning');
        await new Promise(r => setTimeout(r, 1200));
        
        logToSim(`CROSS_REFERENCING_TRUST_GRAPH...`, 'warning');
        await new Promise(r => setTimeout(r, 1000));

        const isMalicious = address.toLowerCase().includes('666') || address.toLowerCase().includes('bad') || address.toLowerCase().includes('hack');
        
        if (isMalicious) {
            logToSim(`CRITICAL_THREAT: MALICIOUS_LOGIC_BLOCK_FOUND`, 'error');
            logToSim(`RISK_SCORE: 94/100`, 'error');
            logToSim(`RECOMMENDATION: DO_NOT_EXECUTE`, 'error');
        } else {
            logToSim(`INTEGRITY_CHECK_SUCCESSFUL`, 'success');
            logToSim(`RISK_SCORE: 11/100`, 'success');
            logToSim(`RECOMMENDATION: PROCEED_SAFE`, 'success');
        }

        runSimBtn.disabled = false;
        runSimBtn.textContent = 'Initialize_Scan';
    });

    // Current Year
    const yearEl = document.getElementById('year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();
});
