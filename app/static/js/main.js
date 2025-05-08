// Initialize GSAP animations
document.addEventListener('DOMContentLoaded', function() {
    // Parallax effect
    const parallaxElements = document.querySelectorAll('.parallax-bg');

    parallaxElements.forEach(element => {
        const depth = element.getAttribute('data-depth');
        gsap.to(element, {
            yPercent: 15 * depth,
            ease: "none",
            scrollTrigger: {
                trigger: element.parentElement,
                start: "top bottom",
                end: "bottom top",
                scrub: true
            }
        });
    });

    // Load sample models
    //    loadSampleModels();

    // Scroll animations
    gsap.utils.toArray(".fade-in").forEach((section, i) => {
        gsap.from(section, {
            opacity: 0,
            y: 50,
            duration: 1,
            scrollTrigger: {
                trigger: section,
                start: "top 80%",
                toggleActions: "play none none none"
            }
        });
    });
});

// Load sample models for the homepage
//function loadSampleModels() {
//    const sampleModels = [
//        {
//            id: 1,
//            name: "Stable Diffusion 2.1",
//            image: "https://via.placeholder.com/400x300/6c5ce7/ffffff?text=SD+2.1",
//            downloads: "12.5k",
//            rating: 4.8,
//            safety: "safe",
//            date: "2023-05-15"
//        },
//        {
//            id: 2,
//            name: "Anime Diffusion",
//            image: "https://via.placeholder.com/400x300/a29bfe/ffffff?text=Anime+Diffusion",
//            downloads: "8.2k",
//            rating: 4.6,
//            safety: "safe",
//            date: "2023-06-22"
//        },
//        {
//            id: 3,
//            name: "Cyberpunk Style",
//            image: "https://via.placeholder.com/400x300/0984e3/ffffff?text=Cyberpunk",
//            downloads: "5.7k",
//            rating: 4.5,
//            safety: "mature",
//            date: "2023-07-10"
//        }
//    ];
//
//    const container = document.getElementById('model-cards');
//
//    sampleModels.forEach(model => {
//        const safetyClass = model.safety === 'safe' ? 'bg-success' : 'bg-warning';
//        const safetyText = model.safety === 'safe' ? 'Safe' : 'Mature';
//
//        const card = document.createElement('div');
//        card.className = 'col-md-4 mb-4';
//        card.innerHTML = `
//            <div class="card model-card h-100" data-aos="fade-up">
//                <span class="badge ${safetyClass} model-badge">${safetyText}</span>
//                <img src="${model.image}" class="card-img-top model-img" alt="${model.name}">
//                <div class="card-body">
//                    <h5 class="card-title">${model.name}</h5>
//                    <div class="d-flex justify-content-between align-items-center mb-2">
//                        <small class="text-muted"><i class="fas fa-download me-1"></i> ${model.downloads}</small>
//                        <div class="rating">
//                            <i class="fas fa-star text-warning"></i> ${model.rating}
//                        </div>
//                    </div>
//                    <div class="d-grid">
//                        <a href="#" class="btn btn-sm btn-outline-primary">Download</a>
//                    </div>
//                </div>
//                <div class="card-footer bg-transparent">
//                    <small class="text-muted">Uploaded on ${model.date}</small>
//                </div>
//            </div>
//        `;
//
//        container.appendChild(card);
//    });
//
//    // Animate model cards sequentially
//    gsap.utils.toArray(".model-card").forEach((card, i) => {
//        gsap.from(card, {
//            opacity: 0,
//            y: 30,
//            duration: 0.5,
//            delay: i * 0.1,
//            scrollTrigger: {
//                trigger: card,
//                start: "top 80%",
//                toggleActions: "play none none none"
//            }
//        });
//    });
//}

// 导航栏滚动效果
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// 登录/注册模态框切换
document.addEventListener('DOMContentLoaded', function() {
    // 获取模态框实例
    const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
    const registerModal = new bootstrap.Modal(document.getElementById('registerModal'));

    // 从登录切换到注册
    document.querySelectorAll('[data-bs-target="#registerModal"]').forEach(btn => {
        btn.addEventListener('click', function() {
            if (loginModal) {
                loginModal.hide();
            }
            if (registerModal) {
                registerModal.show();
            }
        });
    });

    // 从注册切换到登录
    document.querySelectorAll('[data-bs-target="#loginModal"]').forEach(btn => {
        btn.addEventListener('click', function() {
            if (registerModal) {
                registerModal.hide();
            }
            if (loginModal) {
                loginModal.show();
            }
        });
    });
});