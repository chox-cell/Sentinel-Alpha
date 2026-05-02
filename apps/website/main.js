document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Icons
    if (window.lucide) {
        lucide.createIcons();
    }

    // 2. Swarm Canvas Visualization (Abstract, Premium, Max 40 particles)
    const canvas = document.getElementById('swarmCanvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let width, height;
        let particles = [];
        const maxParticles = 35;
        let animationFrameId;
        let isTabActive = true;
        let isScanning = false;

        function resize() {
            width = window.innerWidth;
            height = window.innerHeight;
            canvas.width = width;
            canvas.height = height;
        }

        window.addEventListener('resize', resize);
        resize();

        // Handle tab visibility to pause animation
        document.addEventListener('visibilitychange', () => {
            isTabActive = !document.hidden;
            if (isTabActive) {
                animate();
            } else {
                cancelAnimationFrame(animationFrameId);
            }
        });

        class Particle {
            constructor() {
                this.x = Math.random() * width;
                this.y = Math.random() * height;
                this.vx = (Math.random() - 0.5) * 0.5;
                this.vy = (Math.random() - 0.5) * 0.5;
                this.size = Math.random() * 1.5 + 0.5;
                this.baseAlpha = Math.random() * 0.5 + 0.1;
            }

            update() {
                if (isScanning) {
                    // Swarm towards center right (approx location of hero visual)
                    const targetX = width * 0.75;
                    const targetY = height * 0.4;
                    const dx = targetX - this.x;
                    const dy = targetY - this.y;
                    this.vx += dx * 0.0001;
                    this.vy += dy * 0.0001;
                    this.vx *= 0.95;
                    this.vy *= 0.95;
                } else {
                    // Random drift
                    this.vx += (Math.random() - 0.5) * 0.01;
                    this.vy += (Math.random() - 0.5) * 0.01;
                    
                    // Speed limit
                    const speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
                    if (speed > 1) {
                        this.vx = (this.vx / speed) * 1;
                        this.vy = (this.vy / speed) * 1;
                    }
                }

                this.x += this.vx;
                this.y += this.vy;

                // Wrap edges
                if (this.x < 0) this.x = width;
                if (this.x > width) this.x = 0;
                if (this.y < 0) this.y = height;
                if (this.y > height) this.y = 0;
            }

            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                const color = isScanning ? `rgba(245, 158, 11, ${this.baseAlpha + 0.3})` : `rgba(255, 255, 255, ${this.baseAlpha})`;
                ctx.fillStyle = color;
                ctx.fill();
            }
        }

        function spawnSwarm() {
            particles = [];
            for (let i = 0; i < maxParticles; i++) {
                particles.push(new Particle());
            }
        }
        
        function animateToTarget(targetX, targetY) {
            isScanning = true;
            // The particle update logic already handles isScanning
        }
        
        function applyRiskState(state) {
            const visualLayer = document.querySelector('.swarm-layer');
            if (visualLayer) {
                visualLayer.className = `swarm-layer swarm-state-${state}`;
            }
        }

        spawnSwarm();

        function drawConnections() {
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = dx * dx + dy * dy;

                    if (dist < 15000) {
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        const alpha = (1 - dist / 15000) * 0.15;
                        ctx.strokeStyle = isScanning ? `rgba(245, 158, 11, ${alpha})` : `rgba(255, 255, 255, ${alpha})`;
                        ctx.stroke();
                    }
                }
            }
        }

        function animate() {
            if (!isTabActive) return;
            ctx.clearRect(0, 0, width, height);

            particles.forEach(p => {
                p.update();
                p.draw();
            });

            drawConnections();

            animationFrameId = requestAnimationFrame(animate);
        }

        animate();

        // Expose state globally for the scan logic to trigger
        window.setSwarmScanning = (state) => {
            isScanning = state;
            if (state) {
                animateToTarget(width * 0.75, height * 0.4);
                applyRiskState('warning');
            } else {
                applyRiskState('stable');
            }
        };
    }

    // 3. Tab Logic for Builder Section
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.code-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = `tab-${btn.dataset.tab}`;
            
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.style.display = 'none');
            
            btn.classList.add('active');
            document.getElementById(targetId).style.display = 'block';
        });
    });

    // 4. Interactive Scan Preview Logic
    const startScanBtn = document.getElementById('startScan');
    if (startScanBtn) {
        const targetInput = document.getElementById('targetAddr');
        const laneSelect = document.getElementById('scanLane');
        const statusBox = document.getElementById('scanStatus');
        const challengeBox = document.getElementById('challengeBox');
        
        // Result elements
        const els = {
            score: document.getElementById('riskScore'),
            action: document.getElementById('riskAction'),
            confidence: document.getElementById('riskConfidence'),
            threatClass: document.getElementById('riskThreatClass'),
            emergency: document.getElementById('riskEmergency'),
            attestation: document.getElementById('riskAttestation'),
            hiveThreat: document.getElementById('hiveThreatLevel')
        };
        
        const resultActions = document.getElementById('resultActions');
        const copyCurlBtn = document.getElementById('copyCurlBtn');
        let currentCurlStr = '';

        function updateUIState(state) {
            statusBox.textContent = state;
            if (state.includes('SCANNING')) {
                statusBox.classList.add('scanning');
                if (window.setSwarmScanning) window.setSwarmScanning(true);
            } else {
                statusBox.classList.remove('scanning');
                if (window.setSwarmScanning) window.setSwarmScanning(false);
            }
        }

        function buildCurl(addr, lane) {
            return `curl -X POST "https://api.beezshield.com/contracts/risk-score" \\
  -H "Content-Type: application/json" \\
  -H "X-SENTINEL-LANE: ${lane}" \\
  -H "X402-PAYMENT: tx:YOUR_TX_HASH" \\
  -d '{"contract_address":"${addr}","chain":"base"}'`;
        }

        startScanBtn.addEventListener('click', async () => {
            const addr = targetInput.value.trim();
            const lane = laneSelect.value;
            
            if (!addr.startsWith('0x')) {
                updateUIState('INVALID_TARGET_ADDRESS');
                return;
            }

            startScanBtn.disabled = true;
            updateUIState('SCANNING_NETWORK...');
            challengeBox.style.display = 'none';
            resultActions.style.display = 'none';

            // Reset results
            Object.values(els).forEach(el => el.textContent = '--');
            els.hiveThreat.textContent = 'Monitoring';
            els.hiveThreat.className = 'text-amber';

            try {
                // Simulate X402 challenge step
                challengeBox.style.display = 'block';
                challengeBox.innerHTML = `[x402 protocol simulation] requesting payment for ${lane} lane...`;
                
                await new Promise(r => setTimeout(r, 800));
                
                challengeBox.innerHTML = `[x402 protocol simulation] payment accepted. processing contract...`;
                
                await new Promise(r => setTimeout(r, 600));

                const res = await fetch(`https://api.beezshield.com/contracts/risk-score`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-SENTINEL-LANE': lane,
                        'X402-PAYMENT': 'tx:' + 'a'.repeat(64)
                    },
                    body: JSON.stringify({ contract_address: addr, chain: 'base' })
                });

                if (!res.ok) throw new Error('API request failed');
                
                const data = await res.json();

                // Map results
                els.score.textContent = data.score ?? 'n/a';
                els.action.textContent = data.action ?? 'n/a';
                els.confidence.textContent = data.confidence ?? 'n/a';
                els.emergency.textContent = data.emergency_signal ? 'TRUE' : 'FALSE';
                
                if (data.emergency_signal) els.emergency.style.color = '#ef4444';
                else els.emergency.style.color = 'inherit';

                let tClass = 'unclassified';
                if (typeof data.threat_class === 'string') tClass = data.threat_class;
                else if (data.score < 25) tClass = 'high_risk';
                else if (data.score < 50) tClass = 'elevated_risk';
                else if (data.score < 75) tClass = 'moderate_risk';
                else tClass = 'lower_risk';
                
                els.threatClass.textContent = tClass;

                // Hive threat level sync
                if (data.score < 50) {
                    els.hiveThreat.textContent = 'ELEVATED';
                    els.hiveThreat.className = 'text-red';
                } else {
                    els.hiveThreat.textContent = 'SECURE';
                    els.hiveThreat.className = 'text-green';
                }

                els.attestation.textContent = data.attestation || '0x' + Array(40).fill(0).map(() => Math.floor(Math.random()*16).toString(16)).join('');

                currentCurlStr = buildCurl(addr, lane);
                resultActions.style.display = 'flex';
                
                updateUIState('SCAN_COMPLETE');
            } catch (err) {
                console.error(err);
                updateUIState('IDLE');
                document.getElementById('scanResultsContent').style.display = 'none';
                document.getElementById('scanFallback').style.display = 'block';
                
                // Try again listener
                document.getElementById('tryAgainBtn').onclick = () => {
                    document.getElementById('scanResultsContent').style.display = 'block';
                    document.getElementById('scanFallback').style.display = 'none';
                    startScanBtn.click();
                };
                
                document.getElementById('fallbackCopyCurlBtn').onclick = () => {
                    const fallbackCurl = buildCurl(addr, lane);
                    navigator.clipboard.writeText(fallbackCurl).then(() => {
                        const originalText = document.getElementById('fallbackCopyCurlBtn').innerHTML;
                        document.getElementById('fallbackCopyCurlBtn').innerHTML = 'Copied! <i data-lucide="check" class="icon-sm"></i>';
                        if (window.lucide) lucide.createIcons();
                        setTimeout(() => {
                            document.getElementById('fallbackCopyCurlBtn').innerHTML = originalText;
                            if (window.lucide) lucide.createIcons();
                        }, 2000);
                    });
                };
            } finally {
                startScanBtn.disabled = false;
            }
        });

        if (copyCurlBtn) {
            copyCurlBtn.addEventListener('click', () => {
                if (!currentCurlStr) return;
                navigator.clipboard.writeText(currentCurlStr).then(() => {
                    const originalText = copyCurlBtn.innerHTML;
                    copyCurlBtn.innerHTML = 'Copied! <i data-lucide="check" class="icon-sm"></i>';
                    if (window.lucide) lucide.createIcons();
                    setTimeout(() => {
                        copyCurlBtn.innerHTML = originalText;
                        if (window.lucide) lucide.createIcons();
                    }, 2000);
                });
            });
        }

        const copyCurlSdkBtn = document.getElementById('copyCurlSdkBtn');
        if (copyCurlSdkBtn) {
            copyCurlSdkBtn.addEventListener('click', () => {
                const sdkCurl = `curl -X POST "https://api.beezshield.com/contracts/risk-score" \\
  -H "Content-Type: application/json" \\
  -H "X-SENTINEL-LANE: basic" \\
  -H "X402-PAYMENT: tx:YOUR_TX_HASH" \\
  -d '{"contract_address":"0x1111111111111111111111111111111111111111","chain":"base"}'`;
                navigator.clipboard.writeText(sdkCurl).then(() => {
                    const originalText = copyCurlSdkBtn.innerHTML;
                    copyCurlSdkBtn.innerHTML = 'Copied! <i data-lucide="check" class="icon-sm"></i>';
                    if (window.lucide) lucide.createIcons();
                    setTimeout(() => {
                        copyCurlSdkBtn.innerHTML = originalText;
                        if (window.lucide) lucide.createIcons();
                    }, 2000);
                });
            });
        }

        // Generic copy buttons for tabs
        const copyBtns = document.querySelectorAll('.copy-btn');
        copyBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const targetId = btn.dataset.target;
                const codeBlock = document.querySelector(`#${targetId} code`);
                if (codeBlock) {
                    navigator.clipboard.writeText(codeBlock.innerText).then(() => {
                        const originalText = btn.textContent;
                        btn.textContent = 'Copied!';
                        setTimeout(() => {
                            btn.textContent = originalText;
                        }, 2000);
                    });
                }
            });
        });
    }
});
