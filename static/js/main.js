function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const likesQuestionsList = document.getElementsByClassName('like-questions-list');
const likesAnswerList = document.getElementsByClassName('like-answer-list');
const correctAnswersList = document.getElementsByClassName('correct-answer-list')

for (let item of likesQuestionsList) {
    const DislikeBtn = item.children[0].children[0];
    const Counter = item.children[1];
    const LikeBtn = item.children[2].children[0];

    DislikeBtn.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('item_id', item.dataset.id);
        formData.append('rate_type', 'dislike');
        formData.append('item_type', 'question');
        const request = new Request('/rate/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                Counter.innerHTML = data.count;
                if (data.count < 0)
                    Counter.style.color = "red";
                else
                    Counter.style.color = "green";

                if (data.action == 'add') {
                    DislikeBtn.classList.remove('my-btn-dislike');
                    DislikeBtn.classList.add('my-btn-dislike');
                } else {
                    DislikeBtn.classList.remove('my-btn-dislike');
                    DislikeBtn.classList.add('my-btn-dislike');
                }

                LikeBtn.classList.remove('my-btn-like');
                LikeBtn.classList.add('my-btn-like');
            })
    });

    LikeBtn.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('item_id', item.dataset.id);
        formData.append('rate_type', 'like');
        formData.append('item_type', 'question');
        const request = new Request('/rate/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                Counter.innerHTML = data.count;
                if (data.count >= 0)
                    Counter.style.color = "green";
                else
                    Counter.style.color = "red";

                if (data.action == 'add') {
                    LikeBtn.classList.remove('my-btn-like');
                    LikeBtn.classList.add('my-btn-like');
                } else {
                    LikeBtn.classList.remove('my-btn-like');
                    LikeBtn.classList.add('my-btn-like');
                }

                DislikeBtn.classList.remove('my-btn-dislike');
                DislikeBtn.classList.add('my-btn-dislike');
            })
    });
}

for (let item of likesAnswerList) {
    const DislikeBtn = item.children[0].children[0];
    const Counter = item.children[1];
    const LikeBtn = item.children[2].children[0];

    DislikeBtn.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('item_id', item.dataset.id);
        formData.append('rate_type', 'dislike');
        formData.append('item_type', 'answer');
        const request = new Request('/rate/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                Counter.innerHTML = data.count;
                if (data.count < 0)
                    Counter.style.color = "red";
                else
                    Counter.style.color = "green";

                if (data.action == 'add') {
                    DislikeBtn.classList.remove('my-btn-dislike');
                    DislikeBtn.classList.add('my-btn-dislike');
                } else {
                    DislikeBtn.classList.remove('my-btn-dislike');
                    DislikeBtn.classList.add('my-btn-dislike');
                }

                LikeBtn.classList.remove('my-btn-like');
                LikeBtn.classList.add('my-btn-like');
            })
    });

    LikeBtn.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('item_id', item.dataset.id);
        formData.append('rate_type', 'like');
        formData.append('item_type', 'answer');
        const request = new Request('/rate/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                Counter.innerHTML = data.count;
                if (data.count >= 0)
                    Counter.style.color = "green";
                else
                    Counter.style.color = "red";

                if (data.action == 'add') {
                    LikeBtn.classList.remove('my-btn-like');
                    LikeBtn.classList.add('my-btn-like');
                } else {
                    LikeBtn.classList.remove('my-btn-like');
                    LikeBtn.classList.add('my-btn-like');
                }

                DislikeBtn.classList.remove('my-btn-dislike');
                DislikeBtn.classList.add('my-btn-dislike');
            })
    });
}

for (let item of correctAnswersList) {
    const IsCorrectBtn = item.children[0].children[0];

    IsCorrectBtn.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('item_id', item.dataset.id);
        formData.append('correctness', 'true');

        const request = new Request('/correct/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                if (data.is_correct == 'true') {
                    IsCorrectBtn.checked = true;
                } else if (data.is_correct == 'false') {
                    IsCorrectBtn.checked = false;
                } else {
                    IsCorrectBtn.checked = false;
                }
            })
    });
}