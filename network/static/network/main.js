function toggleLiked(postId) {
  const likesCount = Array.from(
    document.querySelectorAll('.likes-count')
  ).filter((likesCount) => likesCount.id === postId)[0];
  console.log();

  const userId = JSON.parse(document.getElementById('user-id').textContent);

  const likeButtons = Array.from(
    document.querySelectorAll(`.like-button > i.fa`)
  );

  const likeButton = likeButtons.filter(
    (likeButton) => likeButton.id === postId
  )[0];

  fetch(`/post/${postId}`, {
    method: 'PUT',
    body: JSON.stringify({
      userId,
      postId,
    }),
  })
    .then(() => {
      if (likeButton.classList.contains('fa-heart-o')) {
        likeButton.classList.remove('fa-heart-o');
        likeButton.classList.add('fa-heart');
        likesCount.innerHTML = parseInt(likesCount.textContent) + 1;
      } else {
        likeButton.classList.add('fa-heart-o');
        likeButton.classList.remove('fa-heart');
        likesCount.innerHTML = parseInt(likesCount.textContent) - 1;
      }
    })
    .catch((error) => {
      console.log('Error:', error);
    });
}

function editPost(postId) {
  const editButton = getElement(postId, '.edit-button');
  const postContainer = getElement(postId, '.post-container');

  const isParagraphEnabled =
    postContainer.querySelector('p') !== null &&
    typeof postContainer.querySelector('p') !== 'undefined';

  toggleButton(editButton);

  if (editButton.innerHTML === 'Save' && isParagraphEnabled) {
    openTextArea(postId, postContainer);
  } else {
    openParagraph(postId, postContainer);
  }
}

function getElement(postId, className) {
  const elementNodeList = Array.from(document.querySelectorAll(className));
  const element = elementNodeList.filter((element) => element.id === postId)[0];
  return element;
}

function toggleButton(editButton) {
  if (editButton.innerText === 'Edit') {
    editButton.classList.remove('red');
    editButton.classList.add('green');
    editButton.innerText = 'Save';
  } else {
    editButton.classList.remove('green');
    editButton.classList.add('red');
    editButton.innerText = 'Edit';
  }
}

function openTextArea(postId, postContainer) {
  const postBody = getElement(postId, '.post-body');
  const textAreaEl = document.createElement('textarea');
  postContainer.removeChild(postBody);
  textAreaEl.id = postId;
  textAreaEl.innerText = postBody.innerText;
  postContainer.appendChild(textAreaEl);
}

function openParagraph(postId, postContainer) {
  const classNames = ['card-text', 'post-body'];
  const paragraphEl = document.createElement('p');
  paragraphEl.classList.add(...classNames);

  const textAreaEl = getElement(postId, 'textarea');
  postContainer.removeChild(textAreaEl);

  paragraphEl.id = postId;
  paragraphEl.innerText = textAreaEl.value;
  postContainer.appendChild(paragraphEl);

  fetch(`/post/${postId}`, {
    method: 'PUT',
    body: JSON.stringify({
      body: textAreaEl.value,
    }),
  }).catch((error) => {
    console.log('Error:', error);
  });
}
