document.addEventListener("DOMContentLoaded", () => {
    const usersList = document.getElementById("usersList");
    const usersDropdown = document.getElementById("usersDropdown");
    const selectedUsers = document.getElementById("selectedUsers");
    const searchUsers = document.getElementById("searchUsers");

    // Функция для загрузки пользователей
    async function loadUsers() {
        const response = await fetch("/all_users/");
        const users = await response.json();
        return users;
    }

    // Функция для отображения пользователей в dropdown
    function displayUsers(users) {
        usersDropdown.innerHTML = users.map(user => `
            <div class="p-2 hover:bg-gray-100 cursor-pointer" data-user-id="${user.id}">
                ${user.name}
            </div>
        `).join("");
    }

    // Функция для добавления выбранного пользователя
    function addSelectedUser(user) {
        const userElement = document.createElement("div");
        userElement.className = "flex items-center bg-blue-100 text-blue-800 px-2 py-1 rounded";
        userElement.innerHTML = `
            ${user.name}
            <span class="ml-2 cursor-pointer" onclick="removeSelectedUser(${user.id})">×</span>
        `;
        userElement.dataset.userId = user.id;
        selectedUsers.appendChild(userElement);
    }

    // Функция для удаления выбранного пользователя
    window.removeSelectedUser = function(userId) {
        const userElement = document.querySelector(`#selectedUsers div[data-user-id="${userId}"]`);
        if (userElement) {
            userElement.remove();
        }
    }

    // Обработчик клика на usersList для отображения dropdown
    usersList.addEventListener("click", async () => {
        const users = await loadUsers();
        displayUsers(users);
        usersDropdown.classList.remove("hidden");
    });

    // Обработчик клика на пользователя в dropdown
    usersDropdown.addEventListener("click", (e) => {
        if (e.target.dataset.userId) {
            const userId = e.target.dataset.userId;
            const userName = e.target.textContent;
            addSelectedUser({ id: userId, name: userName });
            usersDropdown.classList.add("hidden");
        }
    });

    // Обработчик ввода в поле поиска
    searchUsers.addEventListener("input", async (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const users = await loadUsers();
        const filteredUsers = users.filter(user => user.name.toLowerCase().includes(searchTerm));
        displayUsers(filteredUsers);
    });

    // Закрытие dropdown при клике вне его
    document.addEventListener("click", (e) => {
        if (!usersList.contains(e.target)) {
            usersDropdown.classList.add("hidden");
        }
    });
});


const createChatForm = document.getElementById("createChatForm")
const darkenBg = document.getElementById("darkenBg");
createChat = document.getElementById("createChat")
createChat.addEventListener("click", () => {
       darkenBg.classList.remove("hidden")
       darkenBg.style.opacity = '0.5'
       setTimeout(() => {
            createChatForm.classList.add("hidden");
            darkenBg.classList.add("hidden");
       }, 400)
})

document.getElementById("closeForm").addEventListener("click", () => {
    profileForm.style.opacity = '0';
    profileForm.style.transform = 'scale(0.1)';
    darkenBg.style.opacity = '0';
    setTimeout(() => {
        profileForm.classList.add('hidden');
        darkenBg.classList.add('hidden');
    }, 400);
});

