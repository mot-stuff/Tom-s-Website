document.querySelectorAll('.pricing-panel').forEach(panel => {
    panel.addEventListener('click', () => {
        alert(`You selected the ${panel.querySelector('h3').innerText} plan.`);
    });
});

const scriptList = document.getElementById('script-list');
const scrollLeftButton = document.getElementById('scroll-left');
const scrollRightButton = document.getElementById('scroll-right');

if (scrollLeftButton) {
    scrollLeftButton.addEventListener('click', () => {
        scriptList.scrollBy({
            left: -300,
            behavior: 'smooth'
        });
    });
}

if (scrollRightButton) {
    scrollRightButton.addEventListener('click', () => {
        scriptList.scrollBy({
            left: 300,
            behavior: 'smooth'
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const tagFilter = document.getElementById('tagFilter');

    tagFilter.addEventListener('change', () => {
        const selectedTag = tagFilter.value;
        document.querySelectorAll('.script-card').forEach(card => {
            card.style.display = (selectedTag === "All" || card.dataset.tag === selectedTag)
                ? "flex" : "none";
        });
    });

    // Start polling for live stats updates - thanks chat gpt for teaching me this simple trick
    setInterval(refreshLiveStats, 30000); // Poll every 10 seconds

    // Start polling for slots/status updates
    setInterval(refreshSlotsStatus, 21600000); // Poll every 6 hrs
});

function refreshLiveStats() {
    fetch('/api/live_stats')
        .then(response => response.json())
        .then(data => {
            document.getElementById('xp-gained').innerText = data.xp_gained;
            document.getElementById('hours-botted').innerText = data.hours_botted;
        })
        .catch(error => console.error('Error fetching live stats:', error));
}

function refreshSlotsStatus() {
    fetch('/api/slots_status')
        .then(response => response.json())
        .then(data => {
            const slotsCounter = document.querySelector('.slots-counter');
            if (data.available_slots === 'maintenance') {
                slotsCounter.innerHTML = '<p class="text-lg font-bold">Currently down for maintenance</p>';
                slotsCounter.classList.add('maintenance');
                slotsCounter.classList.remove('bg-red-100', 'text-red-800', 'bg-green-100', 'text-green-800');
            } else if (data.available_slots <= 100) {
                slotsCounter.innerHTML = `<p class="text-lg font-bold">${data.available_slots}/100 slots full | Status: SAFE</p>`;
                slotsCounter.classList.add('bg-green-100', 'text-green-800');
                slotsCounter.classList.remove('maintenance', 'bg-red-100', 'text-red-800');
            } else {
                slotsCounter.innerHTML = '<p class="text-lg font-bold">Slots are full. Please check back later or use a referral to bypass.</p>';
                slotsCounter.classList.add('bg-red-100', 'text-red-800');
                slotsCounter.classList.remove('maintenance', 'bg-green-100', 'text-green-800');
            }
        })
        .catch(error => console.error('Error fetching slots/status:', error));
}

function toggleSection(element) {
    const header = element.closest('.section-header');
    const content = header.nextElementSibling;
    const button = header.querySelector('.toggle-button');
    if (content.style.display === 'none' || content.style.display === '') {
        content.style.display = 'block';
        button.textContent = '-';
    } else {
        content.style.display = 'none';
        button.textContent = '+';
    }
}
