// === FILE: app/static/js/dashboard.js ===

// Global variables
let selectedFile = null;
let deleteFileId = null;

// ========================================
// UPLOAD FUNCTIONALITY
// ========================================

// Open upload modal
document.getElementById('open-upload-modal').addEventListener('click', function() {
    const modal = document.getElementById('upload-modal');
    modal.classList.remove('hidden');
    modal.classList.add('flex', 'modal-enter');
    resetUploadModal();
});

// Close upload modal
document.getElementById('cancel-upload').addEventListener('click', function() {
    closeUploadModal();
});

// Close upload modal with X button
document.getElementById('close-upload-modal').addEventListener('click', function() {
    closeUploadModal();
});

function closeUploadModal() {
    const modal = document.getElementById('upload-modal');
    modal.classList.add('modal-exit');
    setTimeout(() => {
        modal.classList.add('hidden');
        modal.classList.remove('flex', 'modal-enter', 'modal-exit');
    }, 200);
}

// Reset upload modal
function resetUploadModal() {
    selectedFile = null;
    document.getElementById('file-input').value = '';
    document.getElementById('selected-file').classList.add('hidden');
    document.getElementById('progress-container').classList.add('hidden');
    document.getElementById('upload-error').classList.add('hidden');
    document.getElementById('progress-bar').style.width = '0%';
    document.getElementById('upload-btn').disabled = true;
}

// Drop zone click
document.getElementById('drop-zone').addEventListener('click', function() {
    document.getElementById('file-input').click();
});

// File input change
document.getElementById('file-input').addEventListener('change', function(e) {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

// Drag and drop handlers
const dropZone = document.getElementById('drop-zone');

dropZone.addEventListener('dragover', function(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', function(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', function(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('drag-over');
    
    if (e.dataTransfer.files.length > 0) {
        handleFileSelect(e.dataTransfer.files[0]);
    }
});

// Handle file selection
function handleFileSelect(file) {
    // Check file size (100MB max)
    const maxSize = 100 * 1024 * 1024; // 100MB
    if (file.size > maxSize) {
        showUploadError('File size exceeds 100MB limit');
        return;
    }
    
    selectedFile = file;
    document.getElementById('selected-file-name').textContent = file.name;
    document.getElementById('selected-file').classList.remove('hidden');
    document.getElementById('upload-btn').disabled = false;
    document.getElementById('upload-error').classList.add('hidden');
}

// Show upload error
function showUploadError(message) {
    const errorDiv = document.getElementById('upload-error');
    const errorText = document.getElementById('upload-error-text');
    if (errorText) {
        errorText.textContent = message;
    } else {
        errorDiv.textContent = message;
    }
    errorDiv.classList.remove('hidden');
}

// Upload button click
document.getElementById('upload-btn').addEventListener('click', function() {
    if (!selectedFile) {
        showUploadError('Please select a file');
        return;
    }
    
    uploadFile(selectedFile);
});

// Upload file function
function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    // Show progress bar
    document.getElementById('progress-container').classList.remove('hidden');
    document.getElementById('upload-btn').disabled = true;
    document.getElementById('cancel-upload').disabled = true;
    
    // Use XMLHttpRequest for progress tracking
    const xhr = new XMLHttpRequest();
    
    // Progress handler
    xhr.upload.addEventListener('progress', function(e) {
        if (e.lengthComputable) {
            const percentage = (e.loaded / e.total) * 100;
            const roundedPercent = Math.round(percentage);
            document.getElementById('progress-bar').style.width = percentage + '%';
            document.getElementById('progress-text').textContent = `Uploading...`;
            const progressPercent = document.getElementById('progress-percent');
            if (progressPercent) {
                progressPercent.textContent = roundedPercent + '%';
            }
        }
    });
    
    // Load handler (upload complete)
    xhr.addEventListener('load', function() {
        if (xhr.status === 200) {
            try {
                const response = JSON.parse(xhr.responseText);
                if (response.success) {
                    // Success - reload page to show new file
                    window.location.reload();
                } else {
                    showUploadError(response.message || 'Upload failed');
                    document.getElementById('upload-btn').disabled = false;
                    document.getElementById('cancel-upload').disabled = false;
                }
            } catch (e) {
                showUploadError('Upload failed');
                document.getElementById('upload-btn').disabled = false;
                document.getElementById('cancel-upload').disabled = false;
            }
        } else {
            showUploadError('Upload failed. Please try again.');
            document.getElementById('upload-btn').disabled = false;
            document.getElementById('cancel-upload').disabled = false;
        }
    });
    
    // Error handler
    xhr.addEventListener('error', function() {
        showUploadError('Network error. Please try again.');
        document.getElementById('upload-btn').disabled = false;
        document.getElementById('cancel-upload').disabled = false;
    });
    
    // Send request
    xhr.open('POST', '/files/upload');
    xhr.send(formData);
}

// ========================================
// DELETE FUNCTIONALITY
// ========================================

function confirmDelete(fileId, fileName) {
    deleteFileId = fileId;
    document.getElementById('delete-file-name').textContent = fileName;
    
    const modal = document.getElementById('delete-modal');
    modal.classList.remove('hidden');
    modal.classList.add('flex', 'modal-enter');
}

// Cancel delete
document.getElementById('cancel-delete').addEventListener('click', function() {
    closeDeleteModal();
});

function closeDeleteModal() {
    const modal = document.getElementById('delete-modal');
    modal.classList.add('modal-exit');
    setTimeout(() => {
        modal.classList.add('hidden');
        modal.classList.remove('flex', 'modal-enter', 'modal-exit');
        deleteFileId = null;
    }, 200);
}

// Confirm delete
document.getElementById('confirm-delete-btn').addEventListener('click', function() {
    if (!deleteFileId) return;
    
    const btn = this;
    btn.classList.add('btn-loading');
    btn.disabled = true;
    
    fetch(`/files/delete/${deleteFileId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove file card from DOM
            const fileCard = document.querySelector(`.file-card[data-file-id="${deleteFileId}"]`);
            if (fileCard) {
                fileCard.style.opacity = '0';
                fileCard.style.transform = 'scale(0.9)';
                setTimeout(() => {
                    fileCard.remove();
                    
                    // Check if no files left
                    const filesGrid = document.getElementById('files-grid');
                    if (filesGrid && filesGrid.children.length === 0) {
                        window.location.reload();
                    }
                }, 300);
            }
            
            closeDeleteModal();
            showFlashMessage('File deleted successfully', 'success');
        } else {
            showFlashMessage(data.message || 'Failed to delete file', 'error');
            btn.classList.remove('btn-loading');
            btn.disabled = false;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showFlashMessage('Failed to delete file', 'error');
        btn.classList.remove('btn-loading');
        btn.disabled = false;
    });
});

// ========================================
// SHARE FUNCTIONALITY
// ========================================

function shareFile(fileId) {
    fetch(`/files/share/${fileId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('share-url').value = data.share_url;
            
            const modal = document.getElementById('share-modal');
            modal.classList.remove('hidden');
            modal.classList.add('flex', 'modal-enter');
        } else {
            showFlashMessage(data.message || 'Failed to generate share link', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showFlashMessage('Failed to generate share link', 'error');
    });
}

// Close share modal
document.getElementById('close-share-modal').addEventListener('click', function() {
    closeShareModal();
});

function closeShareModal() {
    const modal = document.getElementById('share-modal');
    modal.classList.add('modal-exit');
    setTimeout(() => {
        modal.classList.add('hidden');
        modal.classList.remove('flex', 'modal-enter', 'modal-exit');
        document.getElementById('copy-feedback').classList.add('hidden');
    }, 200);
}

// Copy link button
document.getElementById('copy-link-btn').addEventListener('click', function() {
    const shareUrl = document.getElementById('share-url');
    shareUrl.select();
    shareUrl.setSelectionRange(0, 99999); // For mobile devices
    
    // Copy to clipboard
    navigator.clipboard.writeText(shareUrl.value)
        .then(() => {
            const feedback = document.getElementById('copy-feedback');
            feedback.classList.remove('hidden');
            
            // Hide after 2 seconds
            setTimeout(() => {
                feedback.classList.add('hidden');
            }, 2000);
        })
        .catch(err => {
            console.error('Failed to copy:', err);
            showFlashMessage('Failed to copy link', 'error');
        });
});

// ========================================
// PREVIEW FUNCTIONALITY
// ========================================

function previewFile(fileId) {
    fetch(`/files/preview/${fileId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success && data.preview_url) {
                window.open(data.preview_url, '_blank');
            } else {
                showFlashMessage('Preview not available', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showFlashMessage('Failed to generate preview', 'error');
        });
}

// ========================================
// HELPER FUNCTIONS
// ========================================

function showFlashMessage(message, category) {
    const flashContainer = document.getElementById('flash-messages') || createFlashContainer();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `flash-message px-6 py-3 rounded-lg shadow-lg text-white`;
    
    if (category === 'success') {
        messageDiv.classList.add('bg-[#22c55e]');
    } else if (category === 'error') {
        messageDiv.classList.add('bg-[#ef4444]');
    } else {
        messageDiv.classList.add('bg-[#6366f1]');
    }
    
    messageDiv.textContent = message;
    flashContainer.appendChild(messageDiv);
    
    // Auto-dismiss after 4 seconds
    setTimeout(() => {
        messageDiv.style.opacity = '0';
        messageDiv.style.transform = 'translateX(100%)';
        messageDiv.style.transition = 'all 0.3s ease-out';
        setTimeout(() => {
            messageDiv.remove();
        }, 300);
    }, 4000);
}

function createFlashContainer() {
    const container = document.createElement('div');
    container.id = 'flash-messages';
    container.className = 'fixed top-4 right-4 z-50 space-y-2';
    document.body.appendChild(container);
    return container;
}

// ========================================
// INITIALIZATION
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard loaded');
});
