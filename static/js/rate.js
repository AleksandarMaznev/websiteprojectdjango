const rate = (rating, book_id) => {
    fetch(`/library/book/${book_id}/${rating}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(rest => {
        window.location.reload();
    })
}