const mobilemenubtn = document.getElementById('mobile-menu-btn') as HTMLBodyElement;
if (mobilemenubtn) {
    const mobilemenu = document.getElementById('mobile-menu') as HTMLBodyElement;
    mobilemenubtn.addEventListener('click', () => {
        // remove hidden
        mobilemenu.classList.remove('hidden');
        // add fixed
        mobilemenu.classList.add('fixed');
    });
    if (mobilemenu) {
        const mobilemenubtnclose = document.getElementById('mobile-menu-btn-close') as HTMLBodyElement;
        mobilemenubtnclose.addEventListener('click', () => {
            // remove fixed
            mobilemenu.classList.remove('fixed');
            // add hidden
            mobilemenu.classList.add('hidden');
        });
    }
}
