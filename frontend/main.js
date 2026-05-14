document.addEventListener('DOMContentLoaded', () => {
    const btnConnect = document.getElementById('btn-connect');
    const statusIndicator = document.getElementById('connection-status');
    const statusText = document.getElementById('connection-text');
    
    const selects = ['iso', 'aperture', 'shutterspeed', 'whitebalance'];
    const selectElements = {};
    selects.forEach(id => {
        selectElements[id] = document.getElementById(id);
    });

    const btnApply = document.getElementById('btn-apply');
    const btnCapture = document.getElementById('btn-capture');
    const liveView = document.getElementById('live-view');
    const latestCapture = document.getElementById('latest-capture');
    const placeholderText = document.querySelector('.placeholder-text');

    let connected = false;

    // Check status on load
    checkStatus();

    btnConnect.addEventListener('click', async () => {
        btnConnect.disabled = true;
        try {
            const res = await fetch('/api/connect', { method: 'POST' });
            if (res.ok) {
                await checkStatus();
            } else {
                alert('Failed to connect to camera.');
            }
        } catch (e) {
            console.error(e);
            alert('Error connecting.');
        } finally {
            btnConnect.disabled = false;
        }
    });

    btnApply.addEventListener('click', async () => {
        const payload = {};
        selects.forEach(id => {
            if (selectElements[id].value) {
                payload[id] = selectElements[id].value;
            }
        });

        btnApply.disabled = true;
        try {
            const res = await fetch('/api/config', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (res.ok) {
                alert('Settings applied successfully');
                await loadConfig();
            }
        } catch (e) {
            console.error(e);
        } finally {
            btnApply.disabled = false;
        }
    });

    btnCapture.addEventListener('click', async () => {
        btnCapture.disabled = true;
        try {
            const res = await fetch('/api/capture', { method: 'POST' });
            if (res.ok) {
                const data = await res.json();
                latestCapture.src = `/api/images/${data.file}?t=${new Date().getTime()}`;
                latestCapture.style.display = 'block';
                placeholderText.style.display = 'none';
            } else {
                const errData = await res.json();
                alert('Failed to capture: ' + errData.detail);
            }
        } catch (e) {
            console.error(e);
            alert('Failed to capture image');
        } finally {
            btnCapture.disabled = false;
        }
    });

    async function checkStatus() {
        try {
            const res = await fetch('/api/status');
            const data = await res.json();
            connected = data.connected;
            updateUIState();
            if (connected) {
                await loadConfig();
                startLiveView();
            }
        } catch (e) {
            console.error(e);
        }
    }

    function updateUIState() {
        if (connected) {
            statusIndicator.classList.add('connected');
            statusText.textContent = 'Connected';
            selects.forEach(id => selectElements[id].disabled = false);
            btnApply.disabled = false;
            btnCapture.disabled = false;
        } else {
            statusIndicator.classList.remove('connected');
            statusText.textContent = 'Disconnected';
            selects.forEach(id => selectElements[id].disabled = true);
            btnApply.disabled = true;
            btnCapture.disabled = true;
            liveView.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
        }
    }

    async function loadConfig() {
        try {
            const res = await fetch('/api/config');
            const data = await res.json();
            
            selects.forEach(id => {
                if (data[id]) {
                    const sel = selectElements[id];
                    sel.innerHTML = '';
                    data[id].choices.forEach(choice => {
                        const opt = document.createElement('option');
                        opt.value = choice;
                        opt.textContent = choice;
                        if (choice === data[id].value) {
                            opt.selected = true;
                        }
                        sel.appendChild(opt);
                    });
                }
            });
        } catch (e) {
            console.error(e);
        }
    }

    function startLiveView() {
        liveView.src = `/api/liveview?t=${new Date().getTime()}`;
    }
});
