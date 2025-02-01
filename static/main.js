
// Tab switching
function switchTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));

    const activeTab = document.querySelector(`.tab:nth-child(${tab === 'github' ? '1' : '2'})`);
    const activePanel = document.querySelector(`#${tab}-panel`);

    activeTab.classList.add('active');
    activePanel.classList.add('active');
}

// Copy to clipboard functionality
async function copyToClipboard(elementId) {
    const text = document.getElementById(elementId).textContent;
    const copyBtn = document.querySelector(`#${elementId}`).nextElementSibling;

    try {
        await navigator.clipboard.writeText(text);
        copyBtn.textContent = 'Copied!';
        copyBtn.classList.add('copied');

        setTimeout(() => {
            copyBtn.textContent = 'Copy link';
            copyBtn.classList.remove('copied');
        }, 2000);
    } catch (err) {
        alert('Copy failed, please copy manually.');
    }
}

// File input handling
const fileInput = document.getElementById('file-input');
const fileLabel = document.getElementById('file-label');

fileInput.addEventListener('change', (e) => {
    const fileName = e.target.files[0]?.name || '拖拽文件到这里或点击上传';
    fileLabel.textContent = fileName;
});

// Drag and drop handling
const dropZone = document.querySelector('.file-upload-label');

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#000';
    dropZone.style.background = '#f8f8f8';
});

dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#ccc';
    dropZone.style.background = 'white';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#ccc';
    dropZone.style.background = 'white';

    const files = e.dataTransfer.files;
    if (files.length) {
        fileInput.files = files;
        fileLabel.textContent = files[0].name;
    }
});

// GitHub form submission
async function handleGithubSubmit(e) {
    e.preventDefault();
    const input = document.getElementById('github-link');
    const loading = document.getElementById('github-loading');
    const result = document.getElementById('github-result');
    const resultLink = document.getElementById('github-result-link');

    loading.classList.add('show');
    result.classList.remove('show');

    try {
        // Replace this with your actual API endpoint
        const response = await fetch('/api/convert-github', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: input.value }),
        });

        if (!response.ok) throw new Error('Failed to convert link');

        const data = await response.json();
        resultLink.href = data.convertedUrl;
        resultLink.textContent = data.convertedUrl;
        result.classList.add('show');
    } catch (error) {
        resultLink.textContent = "Your link is invalid.";
        result.classList.add('show');
    } finally {
        loading.classList.remove('show');
    }
}

// File form submission
async function handleFileSubmit(e) {
    e.preventDefault();
    const input = document.getElementById('file-input');
    const loading = document.getElementById('file-loading');
    const result = document.getElementById('file-result');
    const resultLink = document.getElementById('file-result-link');

    if (!input.files[0]) return;

    loading.classList.add('show');
    result.classList.remove('show');

    try {
        const formData = new FormData();
        const vipCode = document.getElementById('vip-code').value || '';
        // save vip code to local storage
        if (vipCode !== '') {
            localStorage.setItem('vipCode', vipCode);
        }
        formData.append('vipCode', vipCode);
        formData.append('file', input.files[0]);

        // Replace this with your actual API endpoint
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) throw new Error('Failed to upload file');

        const data = await response.json();
        resultLink.href = data.fileUrl;
        resultLink.textContent = data.fileUrl;
        result.classList.add('show');

        // Reset file input
        input.value = '';
        fileLabel.textContent = 'Drag and drop files here or click to upload.';
    } catch (error) {
        resultLink.textContent = "Upload failed.";
        result.classList.add('show');
    } finally {
        loading.classList.remove('show');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const savedVipCode = localStorage.getItem('vipCode');
    if (savedVipCode) {
        document.getElementById('vip-code').value = savedVipCode;
    }
});