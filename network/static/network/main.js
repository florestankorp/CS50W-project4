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
