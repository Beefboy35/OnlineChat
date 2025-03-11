
    const createChatButton = document.getElementById("createChat");
    const createChatForm = document.getElementById("createChatForm");

    // Открытие формы создания чата
    createChatButton.addEventListener("click", () => {
        darkenBg.classList.remove("hidden");
        createChatForm.classList.remove("hidden");
    });

    // Закрытие формы создания чата
    document.getElementById("closeForm").addEventListener("click", () => {
        createChatForm.style.opacity = '0';
        createChatForm.style.transform = 'scale(0.1)';
        darkenBg.style.opacity = '0';
        setTimeout(() => {
            createChatForm.classList.add('hidden');
            darkenBg.classList.add('hidden');
        }, 400);
    });
