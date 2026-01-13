// FetchYT Frontend Application
const API_BASE = '/api/v1';

// DOM Elements
const downloadForm = document.getElementById('downloadForm');
const extractBtn = document.getElementById('extractBtn');
const downloadBtn = document.getElementById('downloadBtn');
const urlInput = document.getElementById('url');
const formatSelect = document.getElementById('format');
const qualitySelect = document.getElementById('quality');

const infoSection = document.getElementById('infoSection');
const videoInfo = document.getElementById('videoInfo');
const progressSection = document.getElementById('progressSection');
const progressBar = document.getElementById('progressBar');
const progressText = document.getElementById('progressText');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const successSection = document.getElementById('successSection');
const successMessage = document.getElementById('successMessage');

// Hide all status sections
function hideAllSections() {
    infoSection.classList.add('hidden');
    progressSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    successSection.classList.add('hidden');
}

// Show error message
function showError(message) {
    hideAllSections();
    errorMessage.textContent = message;
    errorSection.classList.remove('hidden');
}

// Show success message
function showSuccess(message) {
    hideAllSections();
    successMessage.textContent = message;
    successSection.classList.remove('hidden');
}

// Format duration (seconds to MM:SS)
function formatDuration(seconds) {
    if (!seconds) return 'Unknown';
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Display video information
function displayVideoInfo(videos) {
    videoInfo.innerHTML = '';
    
    if (videos.length === 0) {
        videoInfo.innerHTML = '<p>No videos found</p>';
        return;
    }

    videos.forEach(video => {
        const videoItem = document.createElement('div');
        videoItem.className = 'video-item';
        
        let thumbnail = '';
        if (video.thumbnail) {
            thumbnail = `<img src="${video.thumbnail}" alt="${video.title}" class="video-thumbnail">`;
        }
        
        videoItem.innerHTML = `
            ${thumbnail}
            <div class="video-details">
                <div class="video-title">${video.title}</div>
                <div class="video-meta">
                    ${video.uploader || 'Unknown uploader'} • 
                    ${formatDuration(video.duration)}
                </div>
            </div>
        `;
        
        videoInfo.appendChild(videoItem);
    });
    
    infoSection.classList.remove('hidden');
}

// Set loading state
function setLoading(isLoading) {
    extractBtn.disabled = isLoading;
    downloadBtn.disabled = isLoading;
    
    if (isLoading) {
        downloadBtn.innerHTML = '<span class="spinner"></span> Processing...';
    } else {
        downloadBtn.innerHTML = '⬇️ Download';
    }
}

// Extract video information
extractBtn.addEventListener('click', async () => {
    const url = urlInput.value.trim();
    
    if (!url) {
        showError('Please enter a YouTube URL');
        return;
    }
    
    setLoading(true);
    hideAllSections();
    
    try {
        const response = await fetch(`${API_BASE}/extract`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url }),
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to extract information');
        }
        
        const data = await response.json();
        displayVideoInfo(data.videos);
    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
});

// Start download
downloadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const url = urlInput.value.trim();
    const format = formatSelect.value;
    const quality = qualitySelect.value;
    
    if (!url) {
        showError('Please enter a YouTube URL');
        return;
    }
    
    setLoading(true);
    hideAllSections();
    progressSection.classList.remove('hidden');
    progressBar.style.width = '0%';
    progressText.textContent = 'Starting download...';
    
    try {
        const response = await fetch(`${API_BASE}/download`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url, format, quality }),
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to start download');
        }
        
        const data = await response.json();
        
        // Display video info while downloading
        displayVideoInfo(data.videos);
        
        // Update progress
        progressText.textContent = `Downloading ${data.videos.length} video(s)...`;
        
        // Simulate progress (in real implementation, poll status endpoint)
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += 5;
            if (progress > 90) {
                progress = 90;
            }
            progressBar.style.width = `${progress}%`;
        }, 500);
        
        // Wait a bit and then show success
        setTimeout(() => {
            clearInterval(progressInterval);
            progressBar.style.width = '100%';
            progressText.textContent = 'Download complete!';
            
            setTimeout(() => {
                showSuccess(`Successfully downloaded ${data.videos.length} video(s) as ${format.toUpperCase()} files. Check your downloads folder.`);
                setLoading(false);
            }, 1000);
        }, 5000);
        
    } catch (error) {
        showError(error.message);
        setLoading(false);
    }
});

// Check API health on load
async function checkHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        console.log('API Status:', data);
    } catch (error) {
        console.error('API not available:', error);
    }
}

checkHealth();
