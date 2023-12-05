// This JS function is called when the user clicks on the "Delete Note" button. It deletes the note with the given noteId, and redirects the user to the journal.html page.
function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId }),
    }).then((res) => {
        if (!res.ok) {
            throw new Error('Network response was not ok');
        }
        return res.json();
    }).then((data) => {
        if (data.redirect) {
            window.location.href = data.redirect;
        } else {
            console.log('Note deleted, but no redirect URL provided.');
        }
    }).catch((error) => {
        console.error('Error during note deletion:', error);
    });
}
