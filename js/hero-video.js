// Hero Video with Fallback
document.addEventListener('DOMContentLoaded', function() {
    const video = document.querySelector('.hero-video');
    
    if (!video) return;
    
    // Load video with fallback handling
    function loadVideo() {
        // Set preload to auto to start loading
        video.preload = 'auto';
        
        // Load the video source
        const source = video.querySelector('source');
        if (source && source.src) {
            video.load();
            
            // Play the video once loaded
            video.addEventListener('loadeddata', function() {
                video.play().catch(function(error) {
                    console.log('Video autoplay failed, showing poster image:', error);
                });
            });
            
            // Handle video errors - fallback to poster image
            video.addEventListener('error', function() {
                console.log('Video failed to load, using poster image');
            });
        }
    }
    
    // Load video on page load
    loadVideo();
    
    // Intersection Observer for better performance
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                // Video is visible, ensure it's loaded
                if (video.preload === 'none') {
                    loadVideo();
                }
            }
        });
    }, {
        threshold: 0.1
    });
    
    observer.observe(video);
}); 