const profileForm = document.getElementById("profileForm");
const darkenBg = document.getElementById("darkenBg");
document.getElementById("getProfile").addEventListener("click", () => {
    darkenBg.classList.remove('hidden');
    darkenBg.style.opacity = '0.5';
    profileForm.classList.remove('hidden');
    setTimeout(() => {
        profileForm.style.opacity = '1';
        profileForm.style.transform = 'scale(1)';
    }, 10);
});

document.getElementById("closeForm").addEventListener("click", () => {
    profileForm.style.opacity = '0';
    profileForm.style.transform = 'scale(0.1)';
    darkenBg.style.opacity = '0';
    setTimeout(() => {
        profileForm.classList.add('hidden');
        darkenBg.classList.add('hidden');
    }, 400);
});